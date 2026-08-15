import os
import sys
import subprocess
import time
import requests
from uagents import Agent, Context, Model, Protocol

# ★ MeTTa の動的インポート
try:
    import hyperon
except ImportError:
    print("hyperon が見つかりません。動的にインストールを開始します...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "hyperon", "uagents"])
    import hyperon

from hyperon import MeTTa

# --------------------------------------------------
# ⚙️ Secret 設定 & Agent 初期化
# --------------------------------------------------
TRADE_COOLDOWN_SECONDS = 300  # クールダウン時間 (5分)

AGENT_SEED = os.getenv("AGENT_SEED")

agent = Agent(
    name="world-money-map-orchestrator",
    seed=AGENT_SEED or "wmmo_orchestrator_production_seed_2026",
)

# --------------------------------------------------
# 🛡️ MeTTa によるマクロ資金流動 & トレードシグナル検証エンジン
# --------------------------------------------------
def evaluate_wmmo_trade_logic(
    us10y_yield: float,
    vix: float,
    vault_stress: float,
    cb_gold_absorption: str
) -> dict:
    metta = MeTTa()

    metta_script = f"""
    ;; 1. 資金逃避 (Capital Flight) 判定ルール
    (= (detect-capital-flight)
       (if (and (> {us10y_yield} 4.50) (> {vix} 20.0))
           "FLIGHT_DETECTED_HIGH_URGENCY"
           "STABLE_FLOW"))

    ;; 2. ペパートレード実行ルール (BUY / SELL / HOLD)
    (= (evaluate-paper-trade)
       (if (> {vault_stress} 0.60)
           "EXECUTE_PAPER_SELL_RISK_OFF"
           (if (and (== (detect-capital-flight) "FLIGHT_DETECTED_HIGH_URGENCY")
                    (== "{cb_gold_absorption}" "CRITICAL_SUPPLY_CRUNCH"))
               "EXECUTE_PAPER_BUY_GOLD_AI_RWA"
               "HOLD_POSITION")))

    ;; 評価実行
    !(detect-capital-flight)
    !(evaluate-paper-trade)
    """
    
    try:
        results = metta.run(metta_script)
        flight_result = str(results[0][0]) if len(results) > 0 and len(results[0]) > 0 else "STABLE_FLOW"
        trade_result = str(results[1][0]) if len(results) > 1 and len(results[1]) > 0 else "HOLD_POSITION"
    except Exception as e:
        print(f"⚠️ MeTTa 評価例外: {e}")
        flight_result = "STABLE_FLOW"
        trade_result = "HOLD_POSITION"

    return {
        "flight_detected": "FLIGHT_DETECTED" in flight_result,
        "flight_signal": flight_result,
        "trade_action": trade_result,
        "confidence_score": 0.95 if "EXECUTE" in trade_result else 0.50
    }

# --------------------------------------------------
# 💬 Orchestrator Chat Protocol (ASI One 恒久対応版)
# --------------------------------------------------
class ChatMessage(Model):
    message: str

chat_proto = Protocol(name="Agent Chat Protocol", version="0.2.0")

@chat_proto.on_message(model=ChatMessage, replies=ChatMessage)
async def handle_wmmo_chat(ctx: Context, sender: str, msg: ChatMessage):
    user_query = msg.message.lower().strip()
    ctx.logger.info(f"💬 [ASI One Chat] 受信 from {sender}: {msg.message}")

    virtual_usd = ctx.storage.get("virtual_usd_balance") or 100000.0
    holding_paxg = ctx.storage.get("holding_qty_PAXG") or 0.0

    if any(k in user_query for k in ["portfolio", "balance", "残高", "資産"]):
        reply_text = (
            f"🌐 **World Money Map Virtual Portfolio**\n"
            f"・現金残高: **${virtual_usd:,.2f} USD**\n"
            f"・PAXG 保有量: **{holding_paxg:.4f} oz**"
        )
    elif any(k in user_query for k in ["signal", "flight", "metta", "シグナル"]):
        decision = evaluate_wmmo_trade_logic(4.66, 22.4, 0.38, "CRITICAL_SUPPLY_CRUNCH")
        reply_text = (
            f"🛡️ **MeTTa Capital Flight Analysis**\n"
            f"・資金逃避ステータス: **{decision['flight_signal']}**\n"
            f"・推奨アクション: **{decision['trade_action']}**"
        )
    else:
        reply_text = (
            f"🌐 **World Money Map Orchestrator Agent (Ver 5.0.0)**\n"
            f"6系統サブエージェント & MeTTa エンジン監視中。\n"
            f"キーワード: `portfolio`, `signal`"
        )

    await ctx.send(sender, ChatMessage(message=reply_text))

# ★ 本番デプロイ時に Almanac へマニフェストを強制登録
agent.include(chat_proto, publish_manifest=True)

# --------------------------------------------------
# 📢 Discord Webhook 設定 & 通知関数
# --------------------------------------------------

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_notification(message: str):
    if not DISCORD_WEBHOOK_URL:
        return
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"⚠️ Discord通知エラー: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Discord通知例外: {e}")

# --------------------------------------------------
# 📈 ガード付きペパートレード実行関数（連打・重複防止）
# --------------------------------------------------
async def execute_paper_trade_with_guard(
    ctx: Context, 
    action: str,          
    asset: str,           
    current_price: float, 
    signal_confidence: float
) -> bool:
    now = time.time()
    
    virtual_usd = ctx.storage.get("virtual_usd_balance")
    if virtual_usd is None:
        virtual_usd = 100000.0
        ctx.storage.set("virtual_usd_balance", virtual_usd)

    holding_qty = ctx.storage.get(f"holding_qty_{asset}") or 0.0
    last_trade_time = ctx.storage.get(f"last_trade_time_{asset}") or 0.0

    elapsed = now - last_trade_time
    if elapsed < TRADE_COOLDOWN_SECONDS:
        remaining = int(TRADE_COOLDOWN_SECONDS - elapsed)
        ctx.logger.info(
            f"⏳ [連打防止] {asset} 前回の注文から {int(elapsed)}秒しか経過していません。"
            f"発注をブロックしました。(待機残り: {remaining}秒)"
        )
        return False

    if action == "EXECUTE_PAPER_BUY":
        if holding_qty > 0:
            ctx.logger.info(f"⚠️ [重複防止] {asset} は既に保有中 ({holding_qty:.4f} 単位) です。追加BUYをスキップします。")
            return False
        
        trade_amount_usd = 10000.0
        if virtual_usd < trade_amount_usd:
            ctx.logger.warning(f"❌ [資金不足] 現金残高 (${virtual_usd:,.2f}) が不足しています。")
            return False

        buy_qty = trade_amount_usd / current_price
        new_usd = virtual_usd - trade_amount_usd
        
        ctx.storage.set("virtual_usd_balance", new_usd)
        ctx.storage.set(f"holding_qty_{asset}", buy_qty)
        ctx.storage.set(f"buy_price_{asset}", current_price)
        ctx.storage.set(f"last_trade_time_{asset}", now)

        ctx.logger.info(
            f"🚀 [PAPER BUY EXECUTE] {asset} | 数量: {buy_qty:.4f} @ ${current_price:,.2f} | "
            f"残金: ${new_usd:,.2f} | 確信度: {signal_confidence}"
        )
        
        # ▼ [修正ポイント3] ここでBUY成功時にDiscord通知を飛ばす
        send_discord_notification(
            f"📈 **[PAPER TRADE NOTIFICATION]**\n"
            f"🟢 **[PAPER TRADE BUY EXECUTED]**\n"
            f"• 資産: {asset}\n"
            f"• 数量: {buy_qty:.4f}\n"
            f"• 価格: ${current_price:,.2f}\n"
            f"• 残り現金: ${new_usd:,.2f}"
        )
        return True

    elif action == "EXECUTE_PAPER_SELL":
        if holding_qty <= 0:
            ctx.logger.info(f"⚠️ [重複防止] {asset} の保有がありません。SELLをスキップします。")
            return False

        buy_price = ctx.storage.get(f"buy_price_{asset}") or current_price
        sell_val = holding_qty * current_price
        pnl = sell_val - (holding_qty * buy_price)
        new_usd = virtual_usd + sell_val

        ctx.storage.set("virtual_usd_balance", new_usd)
        ctx.storage.set(f"holding_qty_{asset}", 0.0)
        ctx.storage.set(f"last_trade_time_{asset}", now)

        ctx.logger.info(
            f"🎯 [PAPER SELL EXECUTE] {asset} | 数量: {holding_qty:.4f} @ ${current_price:,.2f} | "
            f"損益(PnL): ${pnl:+,.2f} | 新残高: ${new_usd:,.2f}"
        )
        
        # ▼ [修正ポイント4] ここでSELL成功時にDiscord通知を飛ばす
        send_discord_notification(
            f"📉 **[PAPER TRADE NOTIFICATION]**\n"
            f"🔴 **[PAPER SELL EXECUTED]**\n"
            f"• 資産: {asset}\n"
            f"• 損益(PnL): ${pnl:+,.2f}\n"
            f"• 新残高: ${new_usd:,.2f}"
        )
        return True

    return False

# --------------------------------------------------
# WMMOの定期タスク（120秒ごとのサブエージェントデータ集約）
# --------------------------------------------------
@agent.on_interval(period=120.0)
async def process_orchestration_cycle(ctx: Context):
    us10y = 4.66          
    vix = 22.4            
    vault_stress = 0.38   
    gold_supply = "CRITICAL_SUPPLY_CRUNCH" 

    decision = evaluate_wmmo_trade_logic(us10y, vix, vault_stress, gold_supply)

    ctx.logger.info(f"🛡️ 【MeTTa マクロ判定】 Flight: {decision['flight_signal']} | Action: {decision['trade_action']}")

    paxg_spot_price = 2450.00 

    if decision["trade_action"] == "EXECUTE_PAPER_BUY_GOLD_AI_RWA":
        await execute_paper_trade_with_guard(
            ctx=ctx,
            action="EXECUTE_PAPER_BUY",
            asset="PAXG",
            current_price=paxg_spot_price,
            signal_confidence=decision["confidence_score"]
        )
    elif decision["trade_action"] == "EXECUTE_PAPER_SELL_RISK_OFF":
        await execute_paper_trade_with_guard(
            ctx=ctx,
            action="EXECUTE_PAPER_SELL",
            asset="PAXG",
            current_price=paxg_spot_price,
            signal_confidence=decision["confidence_score"]
        )

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    ctx.logger.info(f"🚀 起動確認 | Webhook URL設定: {'あり' if url else 'なし'}")
    ctx.logger.info(f"🚀 アドレス: {agent.address}")
