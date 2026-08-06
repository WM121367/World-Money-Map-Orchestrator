# 🌐 World Money Map Orchestrator (`@prime-money-oracle`)

> **Institutional-Grade Global Capital Flow, Macro Stock Pyramid & Multi-Agent Intelligence Engine**

[![Version](https://img.shields.io/badge/Version-4.0.0-blue.svg)](https://github.com/your-org/world-money-map-agent)
[![Framework](https://img.shields.io/badge/Framework-Fetch.ai%20uAgents-orange.svg)](https://fetch.ai/)
[![Protocol](https://img.shields.io/badge/Protocol-X402%20Agentic%20Payments-green.svg)](https://x402.org)

## 📌 Overview

**World Money Map Orchestrator Agent** is an autonomous AI agent built on the Fetch.ai `uAgents` framework. It serves as a master orchestrator that synthesizes macro-financial data feeds, global asset stock pyramids, and real-time intelligence from four specialized sub-agents:

1. **13-Chain Unified Ledger Agent (`@prime-rwa-oracle`)**: Monitors multi-chain events, Farside BTC ETF flows, and institutional RSS feeds.
2. **AI-Chain & DePIN Infrastructure Agent (`@prime-ai-oracle`)**: Tracks Web3 compute arbitrage (TAO/RENDER), data center power grid loads (PJM Virginia), and mega-capital deployments.
3. **Metal & Tokenized Commodity Agent (`@prime-metal-oracle`)**: Evaluates central bank gold reserves, COMEX registered vault drawdowns, and US Debt Clock inflation pressures.
4. **Global Stock Intelligence Agent (`@prime-stock-oracle`)**: Tracks major equity indices (S&P 500, Nasdaq, Nikkei), sovereign bond yields (US10Y/US02Y), liquidity metrics (DXY, Fed Balance Sheet), and MOVE/VIX volatility indicators.

By unifying static **Asset Stock Pools** (Real Estate, Bonds, Equities, Fiat M2, Crypto) with dynamic **Capital Flows** (Bridge activity, ETF inflows, TradFi liquidity shifts, X402 micro-settlements), the Orchestrator outputs actionable cross-asset anomaly signals and real-time capital flight diagnostics.

---

## 🏗️ Architecture System Diagram

```text
                              [ Human App UI / 3D Globe Dashboard ]
                                               │
                                 (HTTP / WebSocket / X402)
                                               ▼
                     ┌──────────────────────────────────────────────────┐
                     │  World Money Map Orchestrator Agent             │
                     │  Handle: @prime-money-oracle                     │
                     └────────────────────────┬─────────────────────────┘
                                              │
              ┌───────────────────────────────┼───────────────────────────────┬───────────────────────────────┐
              │ (uAgents Protocol)            │ (uAgents Protocol)            │ (uAgents Protocol)            │ (uAgents Protocol)
              ▼                               ▼                               ▼                               ▼
  ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
  │   13-Chain Agent      │       │   AI & DePIN Agent    │       │     Metal Agent       │       │   Global Stock Agent  │
  │ • 13 RPCs / RSS Feeds │       │ • TAO / RENDER        │       │ • PAXG / XAUT         │       │ • S&P500 / Nikkei     │
  │ • BTC ETF Flow        │       │ • Grid Proxies / SWF  │       │ • COMEX / Central Bank│       │ • US10Y / DXY / VIX   │
  └───────────────────────┘       └───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```
🔒 Security & Privacy Notice
Secret Seed Protection: The agent loads its seed via AGENT_SEED. All startup handlers and internal logging modules sanitize seed variables, preventing sensitive keys from ever being exposed in logs or console outputs.

⚙️ Environment Variables Setup
Create a .env file in the root directory:
```
AGENT_SEED="your_custom_secure_seed_here"
DISCORD_WEBHOOK_URL="[https://discord.com/api/webhooks/your_webhook_id/your_webhook_token](https://discord.com/api/webhooks/your_webhook_id/your_webhook_token)"

# Sub-Agent Addresses (Configured to Live Deployment Addresses)
TARGET_13CHAIN_AGENT_ADDR="agent1qga88jf6c9hh9cmqq3l37hxftpwhtgzxy6c59fd0a6u7fxn30h9c7pzw9k2"
TARGET_AI_DEPIN_AGENT_ADDR="agent1q0dn5syks2wwdf83jjdqnfjxvf394qh43df0jux8hcw6t67ac7uqq9k03xf"
TARGET_METAL_AGENT_ADDR="agent1q08d8wnsjw3p55dxlf43ugktvz664n4k40wy058zq72lqpvehkdlq2gl8rp"
TARGET_TRADFI_STOCK_AGENT_ADDR="agent1qdr4754jmd9p852frtj8f2j6v6pc55zfnj5gj52zkapfgvx3wet2sxga5mq"
```
📦 Installation & Execution
1. Install Dependencies
```
pip install uagents requests
```
2. Run the Orchestrator
```
python world_money_map_agent.py
```
💬 Message Protocols & Data Models
Query Request Schema (WorldMoneyMapQueryRequest)
```
{
  "scope": "FULL_MAP"
}
```
Response Schema (WorldMoneyMapQueryResponse)
```
{
  "agent_version": "4.0.0",
  "timestamp": 1722880000.0,
  "global_capital_flow_score": 0.93,
  "global_stock_pyramid_usd": {
    "real_estate_usd": "670T - 680T",
    "global_bond_debt_usd": "300T",
    "global_equities_usd": "115T",
    "crypto_market_cap_usd": "2.16T"
  },
  "aggregated_intelligence": {
    "subagent_13chain": {},
    "subagent_ai_depin": {},
    "subagent_metal": {},
    "subagent_tradfi": {
      "global_indices": { "S&P500": { "value": 5450.25 }, "NIKKEI_225": { "value": 38200.0 } },
      "bond_yields_rates": { "US_10Y_YIELD": "4.18%", "US_02Y_YIELD": "4.32%" },
      "macro_liquidity": { "DXY_DOLLAR_INDEX": 104.15 }
    }
  },
  "macro_capital_flight_signal": {
    "flight_detected": true,
    "source_asset": "TradFi Bonds ($300T) & Equities ($115T)",
    "target_asset": "Tokenized Gold (PAXG/XAUT), BTC ETF, & High-Yield DePIN Infra",
    "confidence_score": 0.95
  }
}
```
⚖️ Disclaimer
NOT FINANCIAL ADVICE. This software is generated automatically for informational, research, and analytical purposes only. It does not constitute investment, legal, or tax advice.
```
