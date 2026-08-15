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
AGENT_SEED = os.getenv("AGENT_SEED")

agent = Agent(
    name="world-money-map-orchestrator",
    seed=AGENT_SEED or "wmmo_orchestrator_production_seed_2026",
)

# --------------------------------------------------
# 📊 データ構造定義 (Models)
# --------------------------------------------------
class ChatMessage(Model):
    message: str

class TradeSignal(Model):
    action: str
    asset: str
    price: float
    confidence: float

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
# 💬 Orchestrator Chat Protocol
# --------------------------------------------------
chat_proto = Protocol(name="Agent Chat Protocol", version="0.2.0")

@chat_proto.on_message(model=ChatMessage, replies=ChatMessage)
async def handle_wmmo_chat(ctx: Context, sender: str, msg: ChatMessage):
    user_query = msg.message.lower().strip()
    ctx.logger.info(f"💬 [ASI One Chat] 受信 from {sender}: {msg.message}")

    if any(k in user_query for k in ["signal", "flight", "metta", "シグナル"]):
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
            f"キーワード: `signal`"
        )

    await ctx.send(sender, ChatMessage(message=reply_text))

agent.include(chat_proto, publish_manifest=True)

# --------------------------------------------------
# 📢 Discord Webhook 通知関数 (マクロアラート用)
# --------------------------------------------------
def send_discord_notification(ctx: Context, message: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url or "discord.com" not in webhook_url:
        ctx.logger.warning("⚠️ 有効な Discord Webhook URL が設定されていません。")
        return
    
    payload = {
        "content": message,
        "username": "World Money Map Orchestrator"
    }
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        ctx.logger.error(f"⚠️ Discord通知例外発生: {e}")

# --------------------------------------------------
# WMMOの定期タスク（120秒ごとのマクロ判定 & Vaultic AIへの指令送信）
# --------------------------------------------------
@agent.on_interval(period=120.0)
async def process_orchestration_cycle(ctx: Context):
    us10y = 4.66          
    vix = 22.4            
    vault_stress = 0.38   
    gold_supply = "CRITICAL_SUPPLY_CRUNCH" 

    decision = evaluate_wmmo_trade_logic(us10y, vix, vault_stress, gold_supply)
    ctx.logger.info(f"🛡️ 【MeTTa マクロ判定】 Flight: {decision['flight_signal']} | Action: {decision['trade_action']}")

    vaultic_addr = os.getenv("VAULTIC_AI_AGENT_ADDR")
    if not vaultic_addr:
        ctx.logger.warning("⚠️ VAULTIC_AI_AGENT_ADDR が設定されていません。")
        return

    # 判定結果に応じたトレード指令を Vaultic AI へ送信
    if "EXECUTE_PAPER_BUY" in decision["trade_action"]:
        await ctx.send(
            vaultic_addr, 
            TradeSignal(action="BUY", asset="PAXG", price=2450.00, confidence=decision["confidence_score"])
        )
        ctx.logger.info("🚀 [WMMO] Vaultic AI へ BUY 命令を送信しました。")
        send_discord_notification(ctx, f"🌐 **[WMMO MACRO ALERT]**\n🟢 資金逃避シグナル検知。Vaultic AI へ **BUY (PAXG)** 命令を送信しました。")

    elif "EXECUTE_PAPER_SELL" in decision["trade_action"]:
        await ctx.send(
            vaultic_addr, 
            TradeSignal(action="SELL", asset="PAXG", price=2450.00, confidence=decision["confidence_score"])
        )
        ctx.logger.info("📉 [WMMO] Vaultic AI へ SELL 命令を送信しました。")
        send_discord_notification(ctx, f"🌐 **[WMMO MACRO ALERT]**\n🔴 リスクオフシグナル検知。Vaultic AI へ **SELL (PAXG)** 命令を送信しました。")

# 起動時のハンドラ
@agent.on_event("startup")
async def startup_handler(ctx: Context):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    addr = os.getenv("VAULTIC_AI_AGENT_ADDR")
    ctx.logger.info(f"🚀 起動確認 | Webhook: {'あり' if url else 'なし'} | Vaultic連携先: {'設定済み' if addr else '未設定'}")
    ctx.logger.info(f"🚀 WMMO アドレス: {agent.address}")

if __name__ == "__main__":
    agent.run()
