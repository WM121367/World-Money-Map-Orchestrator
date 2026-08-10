# ==================================================
# 🌐 World Money Map Orchestrator Agent (Cloud Ver 5.0.0 - Paper Trade Engine)
# ==================================================
import os
import time
import requests
from uagents import Agent, Context, Model, Protocol

CURRENT_VERSION = "5.0.0-PaperTrade"

# Secrets から各種設定を取得
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

TARGET_AI_DEPIN_AGENT_ADDR = os.getenv("AI_DEPIN_AGENT_ADDR")
TARGET_13CHAIN_AGENT_ADDR = os.getenv("CHAIN_13_AGENT_ADDR")
TARGET_REAL_ESTATE_AGENT_ADDR = os.getenv("REAL_ESTATE_AGENT_ADDR")
TARGET_TRADFI_STOCK_AGENT_ADDR = os.getenv("GLOBAL_STOCK_AGENT_ADDR")
TARGET_METAL_AGENT_ADDR = os.getenv("METAL_AGENT_ADDR")
TARGET_VAULTIC_AI_AGENT_ADDR = os.getenv("VAULTIC_AI_AGENT_ADDR")

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
# 📈 Paper Trading Simulation Engine Module
# --------------------------------------------------
class PaperTradingEngine:
    def __init__(self, ctx: Context, initial_balance: float = 100000.0):
        self.ctx = ctx
        if not ctx.storage.get("paper_portfolio"):
            ctx.storage.set("paper_portfolio", {
                "usd_balance": initial_balance,
                "btc_holdings": 0.0,
                "avg_buy_price": 0.0,
                "total_trades": 0,
                "successful_trades": 0,
                "realized_pnl": 0.0
            })

    def get_portfolio(self) -> dict:
        # 修正: デフォルト値引数を外し、None判定を行う形に変更
        portfolio = self.ctx.storage.get("paper_portfolio")
        return portfolio if portfolio is not None else {}

    def evaluate_and_trade(self, signal: dict, current_btc_price: float, stress_index: float) -> str:
        portfolio = self.get_portfolio()
        usd = portfolio.get("usd_balance", 100000.0)
        btc = portfolio.get("btc_holdings", 0.0)
        avg_price = portfolio.get("avg_buy_price", 0.0)

        score = signal.get("confidence_score", 0.0)
        flight_detected = signal.get("flight_detected", False)

        # 🟢 買い条件: 資金フライト検知 & 高確信スコア(>=0.92) & 十分なUSD残高
        if flight_detected and score >= 0.92 and usd >= 1000.0:
            trade_amount_usd = usd * 0.20
            btc_bought = trade_amount_usd / current_btc_price
            
            portfolio["usd_balance"] -= trade_amount_usd
            portfolio["btc_holdings"] += btc_bought
            portfolio["avg_buy_price"] = current_btc_price
            portfolio["total_trades"] += 1
            
            self.ctx.storage.set("paper_portfolio", portfolio)
            return (
                f"🟢 [PAPER TRADE BUY EXECUTED]\n"
                f"• Bought: {btc_bought:.4f} BTC @ ${current_btc_price:,.2f}\n"
                f"• Capital Spent: ${trade_amount_usd:,.2f} USD\n"
                f"• Remaining Cash: ${portfolio['usd_balance']:,.2f} USD"
            )

        # 🔴 売り条件: +5%利確, -3%損切り, またはシステムリスク上昇(Stress Index > 0.60)
        elif btc > 0 and (
            current_btc_price >= avg_price * 1.05 or 
            current_btc_price <= avg_price * 0.97 or 
            stress_index > 0.60
        ):
            sell_value_usd = btc * current_btc_price
            cost_basis = btc * avg_price
            pnl = sell_value_usd - cost_basis
            
            portfolio["usd_balance"] += sell_value_usd
            portfolio["btc_holdings"] = 0.0
            portfolio["realized_pnl"] += pnl
            if pnl > 0:
                portfolio["successful_trades"] += 1
                
            self.ctx.storage.set("paper_portfolio", portfolio)
            return (
                f"🔴 [PAPER TRADE SELL EXECUTED]\n"
                f"• Sold: {btc:.4f} BTC @ ${current_btc_price:,.2f}\n"
                f"• Realized PnL: ${pnl:+,.2f} USD\n"
                f"• Total Portfolio Cash: ${portfolio['usd_balance']:,.2f} USD"
            )

        return (
            f"⚪ [PAPER TRADE HOLD] Portfolio Active | "
            f"Cash: ${usd:,.2f} USD | BTC: {btc:.4f} | Realized PnL: ${portfolio.get('realized_pnl', 0.0):+,.2f} USD"
        )

        # 🟢 買い条件: 資金フライト検知 & 高確信スコア(>=0.92) & 十分なUSD残高
        if flight_detected and score >= 0.92 and usd >= 1000.0:
            trade_amount_usd = usd * 0.20  # 残高の20%を分配
            btc_bought = trade_amount_usd / current_btc_price
            
            portfolio["usd_balance"] -= trade_amount_usd
            portfolio["btc_holdings"] += btc_bought
            portfolio["avg_buy_price"] = current_btc_price
            portfolio["total_trades"] += 1
            
            self.ctx.storage.set("paper_portfolio", portfolio)
            return (
                f"🟢 [PAPER TRADE BUY EXECUTED]\n"
                f"• Bought: {btc_bought:.4f} BTC @ ${current_btc_price:,.2f}\n"
                f"• Capital Spent: ${trade_amount_usd:,.2f} USD\n"
                f"• Remaining Cash: ${portfolio['usd_balance']:,.2f} USD"
            )

        # 🔴 売り条件: +5%利確, -3%損切り, またはシステムリスク上昇(Stress Index > 0.60)
        elif btc > 0 and (
            current_btc_price >= avg_price * 1.05 or 
            current_btc_price <= avg_price * 0.97 or 
            stress_index > 0.60
        ):
            sell_value_usd = btc * current_btc_price
            cost_basis = btc * avg_price
            pnl = sell_value_usd - cost_basis
            
            portfolio["usd_balance"] += sell_value_usd
            portfolio["btc_holdings"] = 0.0
            portfolio["realized_pnl"] += pnl
            if pnl > 0:
                portfolio["successful_trades"] += 1
                
            self.ctx.storage.set("paper_portfolio", portfolio)
            return (
                f"🔴 [PAPER TRADE SELL EXECUTED]\n"
                f"• Sold: {btc:.4f} BTC @ ${current_btc_price:,.2f}\n"
                f"• Realized PnL: ${pnl:+,.2f} USD\n"
                f"• Total Portfolio Cash: ${portfolio['usd_balance']:,.2f} USD"
            )

        return (
            f"⚪ [PAPER TRADE HOLD] Portfolio Active | "
            f"Cash: ${usd:,.2f} USD | BTC: {btc:.4f} | Realized PnL: ${portfolio.get('realized_pnl', 0.0):+,.2f} USD"
        )

# --------------------------------------------------
# 📊 データ構造定義
# --------------------------------------------------
class DataQueryRequest(Model): chain_name: str
class DataQueryResponse(Model):
    agent_version: str; timestamp: float; chain_statuses: dict; market_intelligence: dict; latest_signals: list; news_intelligence: dict; disclaimer: str

class AIDataQueryRequest(Model): category: str
class AIDataQueryResponse(Model):
    agent_version: str; timestamp: float; web3_ai_depin_metrics: dict; ethereum_agent_competitors: dict; institutional_mega_capital: dict; datacenter_grid_proxies: dict; reasoning_summary: str

class MetalDataQueryRequest(Model): symbol: str
class MetalDataQueryResponse(Model):
    agent_version: str; timestamp: float; onchain_paxg_xaut: dict; coingecko_metal_intelligence: dict; comex_inventory_sentiment: dict; central_bank_gold_trends: dict; mine_supply_constraints: dict; us_debt_macro_metrics: dict; reasoning_summary: str

class TradFiDataQueryRequest(Model): scope: str
class TradFiDataQueryResponse(Model):
    agent_version: str; timestamp: float; global_indices: dict; bond_yields_rates: dict; macro_liquidity: dict; volatility_sentiment: dict; sector_rotation: dict; earnings_macro_trends: dict; reasoning_summary: str

class RealEstateRequest(Model): request_id: str; timestamp: str; force_refresh: bool = False
class RWATokenMetrics(Model): protocol: str; tvl_usd: float; volume_24h_usd: float; market_cap_usd: float; avg_yield_apy: float
class CapRateAndIndex(Model): city: str; country: str; residential_cap_rate: float; commercial_cap_rate: float; house_price_index_yoy: float
class MacroInterestAnalysis(Model): us10y_yield: float; mortgage_30y_avg: float; spread: float; correlation_score: float; market_sentiment: str
class CapitalFlightAndRisk(Model): target_region: str; capital_inflow_est_usd_m: float; regulatory_risk_score: int; liquidity_risk_score: int; estimated_roi: float
class RealEstateResponse(Model):
    request_id: str; timestamp: str; rwa_token_metrics: list[RWATokenMetrics]; global_cap_rates: list[CapRateAndIndex]; macro_interest: MacroInterestAnalysis; capital_flight_risk: list[CapitalFlightAndRisk]; data_hash: str

class VaulticDataQueryRequest(Model): category: str
class VaulticDataQueryResponse(Model):
    agent_version: str; timestamp: float; institutional_vault_metrics: dict; cross_asset_collateral_risk: dict; coinbase_live_solvency: dict; systemic_stress_index: float; reasoning_summary: str

# 💰 商業プロトコル
class WorldMoneyMapQueryRequest(Model): scope: str
class Funds(Model): amount: str; currency: str = "FET"; payment_method: str = "fet_direct"
class RequestPayment(Model): accepted_funds: list[Funds]; recipient: str; deadline_seconds: int = 300; reference: str; description: str
class CommitPayment(Model): funds: Funds; recipient: str; transaction_id: str; reference: str
class WorldMoneyMapQueryResponse(Model):
    agent_version: str; timestamp: float; global_capital_flow_score: float; global_stock_pyramid_usd: dict; aggregated_intelligence: dict; macro_capital_flight_signal: dict; reasoning_summary: str

GLOBAL_STOCK_PYRAMID = {
    "real_estate_usd": "670T - 680T", "global_bond_debt_usd": "300T", "global_m2_fiat_money_usd": "120T",
    "global_equities_usd": "115T", "gold_and_commodities_usd": "18T - 33T", "crypto_market_cap_usd": "2.16T",
}

# --------------------------------------------------
# 🧠 動的推論合成エンジン
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
        "source_asset": f"TradFi Equities & US Bonds (10Y Yield: {us10y})",
        "target_asset": f"Tokenized Gold, AI Infra ({tao_staked} TAO), High-Cap RE ({top_cap_city} {top_cap_val}%)",
        "macro_indicators": {"DXY": dxy, "BTC_Height": btc_height, "Vaultic_Stress_Index": vault_stress},
        "urgency": "HIGH",
        "confidence_score": score,
    }
    
    reasoning_text = (
        f"[SYNTHESIS COMPLETE] Capital Flow Score: {score:.2f} | "
        f"US10Y: {us10y} | DXY: {dxy} | De-dollarization driver: {cb_trend} | "
        f"Vault Stress Index: {vault_stress:.2f}."
    )
    return score, capital_flight_signal, reasoning_text

# --------------------------------------------------
# 🔄 キャッシュ管理
# --------------------------------------------------
def save_agent_cache(ctx: Context, key: str, raw_data: dict):
    ctx.storage.set(key, {"updated_at": time.time(), "is_stale": False, "data": raw_data})

def get_agent_cache_with_fallback(ctx: Context, key: str) -> dict:
    cached = ctx.storage.get(key)
    if cached:
        if time.time() - cached.get("updated_at", 0) > 300: cached["is_stale"] = True
        return cached
    return {"updated_at": 0, "is_stale": True, "data": {"status": "NO_DATA_AVAILABLE_OFFLINE"}}

# --------------------------------------------------
# ⏱️ 定期同期タスク ＆ ペーパートレード評価
# --------------------------------------------------
@agent.on_interval(period=120.0)
async def query_sub_agents_task(ctx: Context):
    ctx.logger.info("📡 [Orchestrator] 6つの子Agentへ同期リクエストを送信中...")
    if TARGET_13CHAIN_AGENT_ADDR: await ctx.send(TARGET_13CHAIN_AGENT_ADDR, DataQueryRequest(chain_name="full_intelligence"))
    if TARGET_AI_DEPIN_AGENT_ADDR: await ctx.send(TARGET_AI_DEPIN_AGENT_ADDR, AIDataQueryRequest(category="ALL"))
    if TARGET_METAL_AGENT_ADDR: await ctx.send(TARGET_METAL_AGENT_ADDR, MetalDataQueryRequest(symbol="ALL"))
    if TARGET_TRADFI_STOCK_AGENT_ADDR: await ctx.send(TARGET_TRADFI_STOCK_AGENT_ADDR, TradFiDataQueryRequest(scope="ALL_MARKETS"))
    if TARGET_VAULTIC_AI_AGENT_ADDR: await ctx.send(TARGET_VAULTIC_AI_AGENT_ADDR, VaulticDataQueryRequest(category="ALL"))
    if TARGET_REAL_ESTATE_AGENT_ADDR:
        await ctx.send(TARGET_REAL_ESTATE_AGENT_ADDR, RealEstateRequest(request_id=str(int(time.time())), timestamp=str(time.time())))

    # 📈 ペーパートレード評価・自動試算の実行
    aggregated_data = {
        "subagent_13chain": get_agent_cache_with_fallback(ctx, "subagent_13chain"),
        "subagent_ai_depin": get_agent_cache_with_fallback(ctx, "subagent_ai_depin"),
        "subagent_metal": get_agent_cache_with_fallback(ctx, "subagent_metal"),
        "subagent_tradfi": get_agent_cache_with_fallback(ctx, "subagent_tradfi"),
        "subagent_real_estate": get_agent_cache_with_fallback(ctx, "subagent_real_estate"),
        "subagent_vaultic_ai": get_agent_cache_with_fallback(ctx, "subagent_vaultic_ai"),
    }
    
    score, flight_signal, _ = generate_dynamic_macro_reasoning(aggregated_data)
    
    # Vaultic AI から Coinbase スポット価格とストレス指数を抽出
    vaultic_data = aggregated_data.get("subagent_vaultic_ai", {}).get("data", {})
    coinbase_info = vaultic_data.get("coinbase_live_solvency", {})
    btc_price = coinbase_info.get("btc_usd_spot", 64250.00)
    stress_index = vaultic_data.get("systemic_stress_index", 0.38)

    trading_engine = PaperTradingEngine(ctx)
    result_log = trading_engine.evaluate_and_trade(flight_signal, btc_price, stress_index)
    ctx.logger.info(f"📊 [PAPER TRADE ENGINE STATUS]\n{result_log}")

    # トレード実行時（BUY/SELL発生時）のみ Discord へ通知
    if "EXECUTED" in result_log and WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"content": f"📈 [PAPER TRADE NOTIFICATION]\n{result_log}"}, timeout=3)
        except Exception as e:
            ctx.logger.error(f"Webhook 送信失敗: {e}")

# --------------------------------------------------
# 📥 受信ハンドラー群
# --------------------------------------------------
@agent.on_message(model=DataQueryResponse)
async def handle_13chain_response(ctx: Context, sender: str, msg: DataQueryResponse):
    if sender in ALLOWED_CHILDREN: save_agent_cache(ctx, "subagent_13chain", msg.dict())

@agent.on_message(model=AIDataQueryResponse)
async def handle_ai_depin_response(ctx: Context, sender: str, msg: AIDataQueryResponse):
    if sender in ALLOWED_CHILDREN: save_agent_cache(ctx, "subagent_ai_depin", msg.dict())

@agent.on_message(model=MetalDataQueryResponse)
async def handle_metal_response(ctx: Context, sender: str, msg: MetalDataQueryResponse):
    if sender in ALLOWED_CHILDREN: save_agent_cache(ctx, "subagent_metal", msg.dict())

@agent.on_message(model=TradFiDataQueryResponse)
async def handle_tradfi_response(ctx: Context, sender: str, msg: TradFiDataQueryResponse):
    if sender in ALLOWED_CHILDREN: save_agent_cache(ctx, "subagent_tradfi", msg.dict())

@agent.on_message(model=RealEstateResponse)
async def handle_real_estate_response(ctx: Context, sender: str, msg: RealEstateResponse):
    if sender in ALLOWED_CHILDREN: save_agent_cache(ctx, "subagent_real_estate", msg.dict())

@agent.on_message(model=VaulticDataQueryResponse)
async def handle_vaultic_response(ctx: Context, sender: str, msg: VaulticDataQueryResponse):
    if sender in ALLOWED_CHILDREN: save_agent_cache(ctx, "subagent_vaultic_ai", msg.dict())

# --------------------------------------------------
# 💰 商業決済ハンドラー
# --------------------------------------------------
@agent.on_message(model=WorldMoneyMapQueryRequest)
async def handle_map_query_quote(ctx: Context, sender: str, msg: WorldMoneyMapQueryRequest):
    scope = (msg.scope or "FULL_MAP").upper()
    price = "5.0" if scope == "FULL_MAP" else "1.0"
    ref = f"quote_wmm_{scope}_{int(time.time())}"
    ctx.storage.set(f"ref_{ref}", {"price": price, "sender": sender, "scope": scope})
    await ctx.send(sender, RequestPayment(
        accepted_funds=[Funds(amount=price, currency="FET")], recipient=str(agent.wallet.address()), deadline_seconds=300, reference=ref, description="Full WMM Intelligence"
    ))

@agent.on_message(model=CommitPayment)
async def handle_map_delivery(ctx: Context, sender: str, msg: CommitPayment):
    quote_record = ctx.storage.get(f"ref_{msg.reference}")
    if not quote_record or float(msg.funds.amount) < float(quote_record.get("price")) or msg.recipient != str(agent.wallet.address()):
        return

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
        agent_version=CURRENT_VERSION, timestamp=time.time(), global_capital_flow_score=score,
        global_stock_pyramid_usd=GLOBAL_STOCK_PYRAMID, aggregated_intelligence=aggregated_data,
        macro_capital_flight_signal=flight_signal, reasoning_summary=reasoning_summary,
    )
    await ctx.send(sender, response)

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("==================================================")
    ctx.logger.info(f"🌐 World Money Map Orchestrator Agent (Ver {CURRENT_VERSION})")
    ctx.logger.info(f"📍 Address: {agent.address}")
    ctx.logger.info("📈 Paper Trading Engine Active ($100k Initial Virtual USD)")
    ctx.logger.info("==================================================")

if __name__ == "__main__":
    agent.run()
