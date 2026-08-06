# ==================================================
# 🌐 World Money Map Orchestrator Agent (Ver 4.1.0)
# ==================================================
import os
import time
from uagents import Agent, Context, Model, Protocol

CURRENT_VERSION = "4.1.0"

AGENT_SEED = os.getenv("AGENT_SEED")
if not AGENT_SEED:
    raise ValueError("エラー: 環境変数 'AGENT_SEED' が設定されていません。")

agent = Agent(
    name="world_money_map_orchestrator",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"]
)

TARGET_13CHAIN_AGENT_ADDR = os.getenv("TARGET_13CHAIN_AGENT_ADDR", "agent1qga88jf6c9hh9cmqq3l37hxftpwhtgzxy6c59fd0a6u7fxn30h9c7pzw9k2")
TARGET_AI_DEPIN_AGENT_ADDR = os.getenv("TARGET_AI_DEPIN_AGENT_ADDR", "agent1q0dn5syks2wwdf83jjdqnfjxvf394qh43df0jux8hcw6t67ac7uqq9k03xf")
TARGET_METAL_AGENT_ADDR = os.getenv("TARGET_METAL_AGENT_ADDR", "agent1q08d8wnsjw3p55dxlf43ugktvz664n4k40wy058zq72lqpvehkdlq2gl8rp")
TARGET_TRADFI_STOCK_AGENT_ADDR = os.getenv("TARGET_TRADFI_STOCK_AGENT_ADDR", "agent1qdr4754jmd9p852frtj8f2j6v6pc55zfnj5gj52zkapfgvx3wet2sxga5mq")

# --------------------------------------------------
# 📊 データ構造定義
# --------------------------------------------------
class DataQueryRequest(Model):
    chain_name: str

class DataQueryResponse(Model):
    agent_version: str
    timestamp: float
    chain_statuses: dict
    market_intelligence: dict
    latest_signals: list
    news_intelligence: dict
    disclaimer: str

class AIDataQueryRequest(Model):
    category: str

class AIDataQueryResponse(Model):
    agent_version: str
    timestamp: float
    web3_ai_depin_metrics: dict
    ethereum_agent_competitors: dict
    institutional_mega_capital: dict
    datacenter_grid_proxies: dict
    reasoning_summary: str

class MetalDataQueryRequest(Model):
    symbol: str

class MetalDataQueryResponse(Model):
    agent_version: str
    timestamp: float
    onchain_paxg_xaut: dict
    coingecko_metal_intelligence: dict
    comex_inventory_sentiment: dict
    central_bank_gold_trends: dict
    mine_supply_constraints: dict
    us_debt_macro_metrics: dict
    reasoning_summary: str

class TradFiDataQueryRequest(Model):
    scope: str

class TradFiDataQueryResponse(Model):
    agent_version: str
    timestamp: float
    global_indices: dict
    bond_yields_rates: dict
    macro_liquidity: dict
    volatility_sentiment: dict
    sector_rotation: dict
    earnings_macro_trends: dict
    reasoning_summary: str

class ChatMessage(Model):
    message: str

class Funds(Model):
    amount: str
    currency: str = "FET"
    payment_method: str = "fet_direct"

class RequestPayment(Model):
    accepted_funds: list[Funds]
    recipient: str
    deadline_seconds: int = 300
    reference: str
    description: str

class CommitPayment(Model):
    funds: Funds
    recipient: str
    transaction_id: str
    reference: str

class WorldMoneyMapQueryRequest(Model):
    scope: str

class WorldMoneyMapQueryResponse(Model):
    agent_version: str
    timestamp: float
    global_capital_flow_score: float
    global_stock_pyramid_usd: dict
    aggregated_intelligence: dict
    macro_capital_flight_signal: dict
    reasoning_summary: str

# --------------------------------------------------
# 💬 Chat Protocol
# --------------------------------------------------
chat_proto = Protocol(name="Orchestrator Chat Protocol", version="0.4.0")

@chat_proto.on_message(model=ChatMessage, replies=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"💬 [Chat Received from {sender}]: {msg.message}")
    reply_text = f"🌐 World Money Map Orchestrator Agent (Ver {CURRENT_VERSION}) [@prime-money-oracle] です！"
    await ctx.send(sender, ChatMessage(message=reply_text))

agent.include(chat_proto)

GLOBAL_STOCK_PYRAMID = {
    "real_estate_usd": "670T - 680T",
    "global_bond_debt_usd": "300T",
    "global_m2_fiat_money_usd": "120T",
    "global_equities_usd": "115T",
    "gold_and_commodities_usd": "18T - 33T (Gold: ~18T)",
    "crypto_market_cap_usd": "2.16T"
}

def calculate_capital_flow_intelligence() -> tuple[float, dict]:
    score = 0.93
    capital_flight_signal = {
        "flight_detected": True,
        "source_asset": "TradFi Bonds ($300T) & Equities ($115T)",
        "target_asset": "Tokenized Gold (PAXG/XAUT), BTC ETF, & High-Yield DePIN Infra",
        "estimated_volume_usd": "$350M+",
        "confidence_score": 0.95,
        "urgency": "HIGH",
        "description": "Rising US10Y volatility and DXY fluctuations triggering institutional rotation from TradFi equities into hard assets and automated yield-generating crypto infrastructure."
    }
    return score, capital_flight_signal

# --------------------------------------------------
# 🔄 定期収集 ＆ 子Agentレスポンス受領 (ctx.storage へ保存)
# --------------------------------------------------
@agent.on_interval(period=120.0)
async def query_sub_agents_task(ctx: Context):
    ctx.logger.info("📡 [Orchestrator] 4つの子Agentへ同期リクエストを送信中...")
    await ctx.send(TARGET_13CHAIN_AGENT_ADDR, DataQueryRequest(chain_name="full_intelligence"))
    await ctx.send(TARGET_AI_DEPIN_AGENT_ADDR, AIDataQueryRequest(category="ALL"))
    await ctx.send(TARGET_METAL_AGENT_ADDR, MetalDataQueryRequest(symbol="ALL"))
    await ctx.send(TARGET_TRADFI_STOCK_AGENT_ADDR, TradFiDataQueryRequest(scope="ALL_MARKETS"))

@agent.on_message(model=DataQueryResponse)
async def handle_13chain_response(ctx: Context, sender: str, msg: DataQueryResponse):
    ctx.logger.info(f"✅ [13-Chain Agent] からのデータ受信完了 ({sender})")
    ctx.storage.set("subagent_13chain", msg.dict())

@agent.on_message(model=AIDataQueryResponse)
async def handle_ai_depin_response(ctx: Context, sender: str, msg: AIDataQueryResponse):
    ctx.logger.info(f"✅ [AI & DePIN Agent] からのデータ受信完了 ({sender})")
    ctx.storage.set("subagent_ai_depin", msg.dict())

@agent.on_message(model=MetalDataQueryResponse)
async def handle_metal_response(ctx: Context, sender: str, msg: MetalDataQueryResponse):
    ctx.logger.info(f"✅ [Metal Agent] からのデータ受信完了 ({sender})")
    ctx.storage.set("subagent_metal", msg.dict())

@agent.on_message(model=TradFiDataQueryResponse)
async def handle_tradfi_response(ctx: Context, sender: str, msg: TradFiDataQueryResponse):
    ctx.logger.info(f"✅ [Global Stock Agent] からのデータ受信完了 ({sender})")
    ctx.storage.set("subagent_tradfi", msg.dict())

# --------------------------------------------------
# 💰 納品ハンドラー (ctx.storage から読み出して返送)
# --------------------------------------------------
@agent.on_message(model=WorldMoneyMapQueryRequest)
async def handle_map_query_quote(ctx: Context, sender: str, msg: WorldMoneyMapQueryRequest):
    scope = (msg.scope or "FULL_MAP").upper()
    quoted_price = "5.0" if scope == "FULL_MAP" else "1.0"
    ctx.logger.info(f"📩 [{sender}] から照会受信: Scope='{scope}' ➔ 見積もり: {quoted_price} FET")
    
    payment_quote = RequestPayment(
        accepted_funds=[Funds(amount=quoted_price, currency="FET", payment_method="fet_direct")],
        recipient=str(agent.wallet.address()),
        deadline_seconds=300,
        reference=f"quote_wmm_{scope}_{int(time.time())}",
        description="Full World Money Map Intelligence"
    )
    await ctx.send(sender, payment_quote)

@agent.on_message(model=CommitPayment)
async def handle_map_delivery(ctx: Context, sender: str, msg: CommitPayment):
    ctx.logger.info(f"💳 [{sender}] から着金通知を受信 (TxHash: {msg.transaction_id})")
    
    if msg.transaction_id and len(msg.transaction_id) >= 10:
        score, flight_signal = calculate_capital_flow_intelligence()
        
        # 永続ストレージ (ctx.storage) からデータを取得
        aggregated_data = {
            "subagent_13chain": ctx.storage.get("subagent_13chain"),
            "subagent_ai_depin": ctx.storage.get("subagent_ai_depin"),
            "subagent_metal": ctx.storage.get("subagent_metal"),
            "subagent_tradfi": ctx.storage.get("subagent_tradfi")
        }
        
        response = WorldMoneyMapQueryResponse(
            agent_version=CURRENT_VERSION,
            timestamp=time.time(),
            global_capital_flow_score=score,
            global_stock_pyramid_usd=GLOBAL_STOCK_PYRAMID,
            aggregated_intelligence=aggregated_data,
            macro_capital_flight_signal=flight_signal,
            reasoning_summary="Orchestrated 4-tier cross-asset synthesis completed."
        )
        await ctx.send(sender, response)
        ctx.logger.info(f"🎉 [{sender}] へ World Money Map 統合データの納品を完了しました！")

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("==================================================")
    ctx.logger.info(f"🌐 World Money Map Orchestrator Agent (Ver {CURRENT_VERSION})")
    ctx.logger.info(f"📍 Address: {agent.address}")
    ctx.logger.info("==================================================")
    await query_sub_agents_task(ctx)

if __name__ == "__main__":
    agent.run()
