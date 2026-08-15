import os
import sys
import subprocess
import time
import requests
from uagents import Agent, Context, Model, Protocol

# --------------------------------------------------
# 📢 Discord Webhook 設定 & 通知関数（デバッグ強化版）
# --------------------------------------------------
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_notification(ctx: Context, message: str):
    if not DISCORD_WEBHOOK_URL:
        ctx.logger.warning("⚠️ Discord Webhook URL が設定されていません。")
        return
    
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        # Discordの成功ステータスは 200 または 204
        if response.status_code in [200, 204]:
            ctx.logger.info("✅ Discordへ通知を正常に送信しました！")
        else:
            ctx.logger.error(f"⚠️ Discord通知エラー: ステータスコード {response.status_code}, 応答: {response.text}")
    except Exception as e:
        ctx.logger.error(f"⚠️ Discord通知例外発生: {e}")

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
        
        # ▼ Discord通知を呼び出し（ctxを渡してログに残るようにする）
        send_discord_notification(
            ctx,
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
        
        # ▼ Discord通知を呼び出し
        send_discord_notification(
            ctx,
            f"📉 **[PAPER TRADE NOTIFICATION]**\n"
            f"🔴 **[PAPER SELL EXECUTED]**\n"
            f"• 資産: {asset}\n"
            f"• 損益(PnL): ${pnl:+,.2f}\n"
            f"• 新残高: ${new_usd:,.2f}"
        )
        return True

    return False
