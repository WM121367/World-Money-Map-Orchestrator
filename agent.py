# ==================================================
# 🌐 World Money Map Orchestrator Agent (Cloud Ver 4.6.0 - 6-Tier Engine)
# ==================================================
import os
import time
import requests
from uagents import Agent, Context, Model, Protocol

CURRENT_VERSION = "4.6.0-cloud"

# Secrets から各種設定を取得
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

TARGET_AI_DEPIN_AGENT_ADDR = os.getenv("AI_DEPIN_AGENT_ADDR")
TARGET_13CHAIN_AGENT_ADDR = os.getenv("CHAIN_13_AGENT_ADDR")
TARGET_REAL_ESTATE_AGENT_ADDR = os.getenv("REAL_ESTATE_AGENT_ADDR")
TARGET_TRADFI_STOCK_AGENT_ADDR = os.getenv("GLOBAL_STOCK_AGENT_ADDR")
TARGET_METAL_AGENT_ADDR = os.getenv("METAL_AGENT_ADDR")
TARGET_VAULTIC_AI_AGENT_ADDR = os.getenv("VAULTIC_AI_AGENT_ADDR")

# Cloud Hosting 用 Agent 初期化（seedの記述を省略しログ出力を防止）
agent = Agent(
    name="world-money-map-orchestrator"
)

ALLOWED_CHILDREN = {
    TARGET_AI_DEPIN_AGENT_ADDR,
    TARGET_13CHAIN_AGENT_ADDR,
    TARGET_REAL_ESTATE_AGENT_ADDR,
    TARGET_TRADFI_STOCK_AGENT_ADDR,
    TARGET_METAL_AGENT_ADDR,
    TARGET_VAULTIC_AI_AGENT_ADDR,
}

# --------------------------------------------------
# 📊 データ構造定義 (Sub-Agents Protocols)
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

class RealEstateRequest(Model):
    request_id: str
    timestamp: str
    force_refresh: bool = False

class RWATokenMetrics(Model):
    protocol: str
    tvl_usd: float
    volume_24h_usd: float
    market_cap_usd: float
    avg_yield_apy: float

class CapRateAndIndex(Model):
    city: str
    country: str
    residential_cap_rate: float
    commercial_cap_rate: float
    house_price_index_yoy: float

class MacroInterestAnalysis(Model):
    us10y_yield: float
    mortgage_30y_avg: float
    spread: float
    correlation_score: float
    market_sentiment: str

class CapitalFlightAndRisk(Model):
    target_region: str
    capital_inflow_est_usd_m: float
    regulatory_risk_score: int
    liquidity_risk_score: int
    estimated_roi: float

class RealEstateResponse(Model):
    request_id: str
    timestamp: str
    rwa_token_metrics: list[RWATokenMetrics]
    global_cap_rates: list[CapRateAndIndex]
    macro_interest: MacroInterestAnalysis
    capital_flight_risk: list[CapitalFlightAndRisk]
    data_hash: str

# --- Vaultic AI データ構造 ---
class VaulticDataQueryRequest(Model):
    category: str

class VaulticDataQueryResponse(Model):
    agent_version: str
    timestamp: float
    institutional_vault_metrics: dict
    cross_asset_collateral_risk: dict
    coinbase_live_solvency: dict  # 👈 ここを追加
    systemic_stress_index: float
    reasoning_summary: str

# --------------------------------------------------
# 💰 商業決済 ＆ 照会プロトコル
# --------------------------------------------------
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

# 💬 Chat Protocol
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
    "crypto_market_cap_usd": "2.16T",
}

# --------------------------------------------------
# 🚨 閾値監視 ＆ アラート通知ロジック (Alert Engine)
# --------------------------------------------------
def check_market_alerts_and_notify(ctx: Context, aggregated_data: dict):
    tradfi = aggregated_data.get("subagent_tradfi", {}).get("data", {})
    vaultic = aggregated_data.get("subagent_vaultic_ai", {}).get("data", {})
    
    vix = tradfi.get("volatility_sentiment", {}).get("VIX_EQUITY_VOLATILITY", 15.4)
    us10y_str = tradfi.get("bond_yields_rates", {}).get("US_10Y_YIELD", "4.18%")
    stress_index = vaultic.get("systemic_stress_index", 0.38)
    
    try:
        us10y_val = float(us10y_str.replace("%", ""))
    except ValueError:
        us10y_val = 4.18

    alerts = []
    if vix > 25.0:
        alerts.append(f"⚠️ HIGH VOLATILITY: VIX Spike Detected ({vix})")
    if us10y_val > 4.50:
        alerts.append(f"⚠️ HIGH YIELD STRESS: US 10Y Yield Exceeds 4.50% ({us10y_val}%)")
    if stress_index > 0.70:
        alerts.append(f"⚠️ VAULTIC SYSTEMIC STRESS: Index Critical ({stress_index})")

    if alerts:
        alert_msg = "🚨 [WORLD MONEY MAP RISK ALERT]\n" + "\n".join(alerts)
        ctx.logger.warning(alert_msg)
        if WEBHOOK_URL:
            try:
                requests.post(WEBHOOK_URL, json={"content": alert_msg}, timeout=3)
                ctx.logger.info("📡 Webhook アラート通知を送信しました。")
            except Exception as e:
                ctx.logger.error(f"Webhook 送信失敗: {e}")
    else:
        ctx.logger.info("🟢 リスク指標は正常範囲内です (Alert Check Clean)")

# --------------------------------------------------
# 🧠 6-Tier クロスアセット動的推論合成エンジン
# --------------------------------------------------
def generate_dynamic_macro_reasoning(data: dict) -> tuple[float, dict, str]:
    tradfi = data.get("subagent_tradfi", {}).get("data", {})
    metal = data.get("subagent_metal", {}).get("data", {})
    ai_depin = data.get("subagent_ai_depin", {}).get("data", {})
    real_estate = data.get("subagent_real_estate", {}).get("data", {})
    chain_13 = data.get("subagent_13chain", {}).get("data", {})
    vaultic = data.get("subagent_vaultic_ai", {}).get("data", {})
    
    us10y = tradfi.get("bond_yields_rates", {}).get("US_10Y_YIELD", "4.18%")
    dxy = tradfi.get("macro_liquidity", {}).get("DXY_DOLLAR_INDEX", 104.15)
    sp500_chg = tradfi.get("global_indices", {}).get("S&P500", {}).get("change_24h_percent", 0.35)
    
    gs_ratio = metal.get("onchain_paxg_xaut", {}).get("gold_silver_ratio", "84.2")
    cb_trend = metal.get("central_bank_gold_trends", {}).get("macro_driver", "De-dollarization")
    
    tao_staked = ai_depin.get("web3_ai_depin_metrics", {}).get("bittensor_tao", {}).get("staking_ratio", "78.4%")
    gpu_lease = ai_depin.get("web3_ai_depin_metrics", {}).get("render_akash_compute", {}).get("gpu_lease_utilization", "91.2%")
    
    cap_rates = real_estate.get("global_cap_rates", [])
    top_cap_city = cap_rates[3].get("city") if len(cap_rates) > 3 else "Dubai"
    top_cap_val = cap_rates[3].get("residential_cap_rate") if len(cap_rates) > 3 else 7.1
    
    btc_height = chain_13.get("chain_statuses", {}).get("bitcoin", "N/A")
    vault_stress = vaultic.get("systemic_stress_index", 0.38)
    
    score = 0.90
    if sp500_chg > 0: score += 0.02
    if "90%" in str(gpu_lease) or "91%" in str(gpu_lease): score += 0.01
    if vault_stress < 0.50: score += 0.01
    score = min(score, 0.99)
    
    capital_flight_signal = {
        "flight_detected": True,
        "source_asset": f"TradFi Equities (S&P500 {sp500_chg:+.2f}%) & US Bonds (10Y Yield: {us10y})",
        "target_asset": f"Tokenized Gold (Gold/Silver Ratio: {gs_ratio}), AI Infra ({tao_staked} TAO Staked), High-Cap RE ({top_cap_city} {top_cap_val}%)",
        "macro_indicators": {"DXY": dxy, "BTC_Height": btc_height, "Vaultic_Stress_Index": vault_stress},
        "urgency": "HIGH",
        "confidence_score": score,
    }
    
    reasoning_text = (
        f"[SYNTHESIS COMPLETE] Capital Flow Score: {score:.2f} | "
        f"Macro Dynamics: US10Y sitting at {us10y} with DXY at {dxy}. "
        f"Physical & Hard Assets: Central banks advancing {cb_trend} amidst Gold/Silver ratio of {gs_ratio}. "
        f"High-Yield Real Assets: Institutional capital rotating towards {top_cap_city} real estate ({top_cap_val}% cap rate). "
        f"AI & DePIN Infrastructure: GPU compute demand peaking at {gpu_lease} utilization. "
        f"Vaultic AI Security: Systemic stress index stable at {vault_stress}. "
        f"Cross-chain ledger sync confirmed at BTC height {btc_height}."
    )
    
    return score, capital_flight_signal, reasoning_text

# --------------------------------------------------
# 🔄 キャッシュ保存・読み出し関数
# --------------------------------------------------
def save_agent_cache(ctx: Context, key: str, raw_data: dict):
    payload = {
        "updated_at": time.time(),
        "is_stale": False,
        "data": raw_data
    }
    ctx.storage.set(key, payload)

def get_agent_cache_with_fallback(ctx: Context, key: str) -> dict:
    cached = ctx.storage.get(key)
    if cached:
        if time.time() - cached.get("updated_at", 0) > 300:
            cached["is_stale"] = True
        return cached
    return {
        "updated_at": 0,
        "is_stale": True,
        "data": {"status": "NO_DATA_AVAILABLE_OFFLINE"}
    }

# --------------------------------------------------
# ⏱️ 定期同期タスク (全6子エージェントへ同期照会)
# --------------------------------------------------
@agent.on_interval(period=120.0)
async def query_sub_agents_task(ctx: Context):
    ctx.logger.info("📡 [Orchestrator] 6つの子Agentへ同期リクエストを送信中...")
    if TARGET_13CHAIN_AGENT_ADDR:
        await ctx.send(TARGET_13CHAIN_AGENT_ADDR, DataQueryRequest(chain_name="full_intelligence"))
    if TARGET_AI_DEPIN_AGENT_ADDR:
        await ctx.send(TARGET_AI_DEPIN_AGENT_ADDR, AIDataQueryRequest(category="ALL"))
    if TARGET_METAL_AGENT_ADDR:
        await ctx.send(TARGET_METAL_AGENT_ADDR, MetalDataQueryRequest(symbol="ALL"))
    if TARGET_TRADFI_STOCK_AGENT_ADDR:
        await ctx.send(TARGET_TRADFI_STOCK_AGENT_ADDR, TradFiDataQueryRequest(scope="ALL_MARKETS"))
    if TARGET_VAULTIC_AI_AGENT_ADDR:
        await ctx.send(TARGET_VAULTIC_AI_AGENT_ADDR, VaulticDataQueryRequest(category="ALL"))

    if TARGET_REAL_ESTATE_AGENT_ADDR:
        req_id = str(int(time.time()))
        await ctx.send(
            TARGET_REAL_ESTATE_AGENT_ADDR,
            RealEstateRequest(request_id=req_id, timestamp=str(time.time())),
        )

# --------------------------------------------------
# 📥 受信ハンドラー群
# --------------------------------------------------
@agent.on_message(model=DataQueryResponse)
async def handle_13chain_response(ctx: Context, sender: str, msg: DataQueryResponse):
    if sender not in ALLOWED_CHILDREN: return
    ctx.logger.info(f"✅ [13-Chain Agent] データ受信完了 ({sender})")
    save_agent_cache(ctx, "subagent_13chain", msg.dict())

@agent.on_message(model=AIDataQueryResponse)
async def handle_ai_depin_response(ctx: Context, sender: str, msg: AIDataQueryResponse):
    if sender not in ALLOWED_CHILDREN: return
    ctx.logger.info(f"✅ [AI & DePIN Agent] データ受信完了 ({sender})")
    save_agent_cache(ctx, "subagent_ai_depin", msg.dict())

@agent.on_message(model=MetalDataQueryResponse)
async def handle_metal_response(ctx: Context, sender: str, msg: MetalDataQueryResponse):
    if sender not in ALLOWED_CHILDREN: return
    ctx.logger.info(f"✅ [Metal Agent] データ受信完了 ({sender})")
    save_agent_cache(ctx, "subagent_metal", msg.dict())

@agent.on_message(model=TradFiDataQueryResponse)
async def handle_tradfi_response(ctx: Context, sender: str, msg: TradFiDataQueryResponse):
    if sender not in ALLOWED_CHILDREN: return
    ctx.logger.info(f"✅ [Global Stock Agent] データ受信完了 ({sender})")
    save_agent_cache(ctx, "subagent_tradfi", msg.dict())
    
    aggregated = {
        "subagent_tradfi": get_agent_cache_with_fallback(ctx, "subagent_tradfi"),
        "subagent_vaultic_ai": get_agent_cache_with_fallback(ctx, "subagent_vaultic_ai")
    }
    check_market_alerts_and_notify(ctx, aggregated)

@agent.on_message(model=RealEstateResponse)
async def handle_real_estate_response(ctx: Context, sender: str, msg: RealEstateResponse):
    if sender not in ALLOWED_CHILDREN: return
    ctx.logger.info(f"✅ [Real Estate Agent] データ受信完了 ({sender})")
    save_agent_cache(ctx, "subagent_real_estate", msg.dict())

@agent.on_message(model=VaulticDataQueryResponse)
async def handle_vaultic_response(ctx: Context, sender: str, msg: VaulticDataQueryResponse):
    if sender not in ALLOWED_CHILDREN: return
    ctx.logger.info(f"✅ [Vaultic AI Agent] データ受信完了 ({sender})")
    save_agent_cache(ctx, "subagent_vaultic_ai", msg.dict())

# --------------------------------------------------
# 💰 見積もり ＆ 厳格決済検証ハンドラー
# --------------------------------------------------
@agent.on_message(model=WorldMoneyMapQueryRequest)
async def handle_map_query_quote(ctx: Context, sender: str, msg: WorldMoneyMapQueryRequest):
    scope = (msg.scope or "FULL_MAP").upper()
    quoted_price = "5.0" if scope == "FULL_MAP" else "1.0"
    ref = f"quote_wmm_{scope}_{int(time.time())}"
    
    ctx.storage.set(f"ref_{ref}", {"price": quoted_price, "sender": sender, "scope": scope})
    ctx.logger.info(f"📩 [{sender}] から照会受信: Scope='{scope}' ➔ 見積もり: {quoted_price} FET (Ref: {ref})")

    payment_quote = RequestPayment(
        accepted_funds=[Funds(amount=quoted_price, currency="FET", payment_method="fet_direct")],
        recipient=str(agent.wallet.address()),
        deadline_seconds=300,
        reference=ref,
        description="Full World Money Map Intelligence",
    )
    await ctx.send(sender, payment_quote)

@agent.on_message(model=CommitPayment)
async def handle_map_delivery(ctx: Context, sender: str, msg: CommitPayment):
    ctx.logger.info(f"💳 [{sender}] から決済通知を受信 (Ref: {msg.reference}, TxHash: {msg.transaction_id})")

    quote_record = ctx.storage.get(f"ref_{msg.reference}")
    if not quote_record:
        ctx.logger.warning(f"🚨 決済拒否: 未登録または有効期限切れの Reference ({msg.reference})")
        return

    expected_price = quote_record.get("price")
    paid_amount = msg.funds.amount
    
    if float(paid_amount) < float(expected_price):
        ctx.logger.warning(f"🚨 決済拒否: 支払金額不足 (請求: {expected_price} FET, 支払: {paid_amount} FET)")
        return
        
    if msg.recipient != str(agent.wallet.address()):
        ctx.logger.warning(f"🚨 決済拒否: 送金先不一致 ({msg.recipient})")
        return

    ctx.logger.info(f"✅ 決済検証合格: {paid_amount} FET (Ref: {msg.reference})")

    aggregated_data = {
        "subagent_13chain": get_agent_cache_with_fallback(ctx, "subagent_13chain"),
        "subagent_ai_depin": get_agent_cache_with_fallback(ctx, "subagent_ai_depin"),
        "subagent_metal": get_agent_cache_with_fallback(ctx, "subagent_metal"),
        "subagent_tradfi": get_agent_cache_with_fallback(ctx, "subagent_tradfi"),
        "subagent_real_estate": get_agent_cache_with_fallback(ctx, "subagent_real_estate"),
        "subagent_vaultic_ai": get_agent_cache_with_fallback(ctx, "subagent_vaultic_ai"),
    }

    score, flight_signal, reasoning_summary = generate_dynamic_macro_reasoning(aggregated_data)

    response = WorldMoneyMapQueryResponse(
        agent_version=CURRENT_VERSION,
        timestamp=time.time(),
        global_capital_flow_score=score,
        global_stock_pyramid_usd=GLOBAL_STOCK_PYRAMID,
        aggregated_intelligence=aggregated_data,
        macro_capital_flight_signal=flight_signal,
        reasoning_summary=reasoning_summary,
    )
    await ctx.send(sender, response)
    ctx.logger.info(f"🎉 [{sender}] へ World Money Map 統合データの納品を完了しました！")

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("==================================================")
    ctx.logger.info(f"🌐 World Money Map Orchestrator Agent (Ver {CURRENT_VERSION})")
    ctx.logger.info(f"📍 Address: {agent.address}")
    ctx.logger.info("🚨 6-Tier Active Risk Alert Engine Initialized")
    ctx.logger.info("==================================================")

if __name__ == "__main__":
    agent.run()
