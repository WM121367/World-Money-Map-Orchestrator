# 🌐 World Money Map Orchestrator Agent (`@prime-money-oracle`)

> **Institutional-Grade Global Capital Flow, Macro Stock Pyramid & Multi-Agent Intelligence Engine**

[![Version](https://img.shields.io/badge/Version-3.0.0-blue.svg)](https://github.com/your-org/world-money-map-agent)
[![Framework](https://img.shields.io/badge/Framework-Fetch.ai%20uAgents-orange.svg)](https://fetch.ai/)
[![Protocol](https://img.shields.io/badge/Protocol-X402%20Agentic%20Payments-green.svg)](https://x402.org)

## 📌 Overview

**World Money Map Orchestrator Agent** is an autonomous AI agent built on the Fetch.ai `uAgents` framework. It serves as a master orchestrator that synthesizes macro-financial data feeds, global asset stock pyramids, and real-time intelligence from three specialized sub-agents:

1. **13-Chain Unified Ledger Agent**: Monitors multi-chain events, Farside BTC ETF flows, and institutional RSS feeds.
2. **AI-Chain & DePIN Infrastructure Agent**: Tracks Web3 compute arbitrage (TAO/RENDER), data center power grid loads (PJM Virginia), and mega-capital deployments.
3. **Metal & Tokenized Commodity Agent**: Evaluates central bank gold reserves, COMEX registered vault drawdowns, and US Debt Clock inflation pressures.

By unifying static **Asset Stock Pools** (Real Estate, Bonds, Fiat M2, Crypto) with dynamic **Capital Flows** (Bridge activity, ETF inflows, X402 micro-settlements), the Orchestrator outputs actionable cross-asset anomaly signals and real-time capital flight diagnostics.

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
              ┌───────────────────────────────┼───────────────────────────────┐
              │ (uAgents Protocol)            │ (uAgents Protocol)            │ (uAgents Protocol)
              ▼                               ▼                               ▼
  ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
  │   13-Chain Agent      │       │   AI & DePIN Agent    │       │     Metal Agent       │
  │ • 13 RPCs / RSS Feeds │       │ • TAO / RENDER        │       │ • PAXG / XAUT         │
  │ • BTC ETF Flow        │       │ • Grid Proxies / SWF  │       │ • COMEX / Central Bank│
  └───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

##🚀 Key Features

Cross-Asset Capital Flight Detection: Detects structural money shifts across TradFi equities, tokenized gold, and digital assets before public market reactions.

Global Asset Pyramid Integration: Benchmarks macro events against global asset pools ($670T Real Estate, $300T Debt, $120T M2, $2.16T Crypto) to calculate asymmetric market multipliers.

Automated Sub-Agent Orchestration: Queries and verifies intelligence payloads from connected domain-specific agents.

Autonomous Micro-Payments (X402 Ready): Integrates native FET/USDC payment requests and transactional delivery verification.

⚙️ Environment Variables Setup

Create a .env file in the root directory:
```

AGENT_SEED="your_custom_secure_seed_here"
DISCORD_WEBHOOK_URL="[https://discord.com/api/webhooks/your_webhook_id/your_webhook_token](https://discord.com/api/webhooks/your_webhook_id/your_webhook_token)"

# Sub-Agent uAgent Addresses
TARGET_13CHAIN_AGENT_ADDR="agent1qga88jf6c9hh9cmqq3l37hxftpwhtgzxy6c59fd0a6u7fxn30h9c7pzw9k2"
TARGET_AI_DEPIN_AGENT_ADDR="agent1q0dn5syks2wwdf83jjdqnfjxvf394qh43df0jux8hcw6t67ac7uqq9k03xf"
TARGET_METAL_AGENT_ADDR="agent1q08d8wnsjw3p55dxlf43ugktvz664n4k40wy058zq72lqpvehkdlq2gl8rp"

```
📦 Installation & Local Execution
1. Prerequisites
Python 3.10 or higher

Pip package manager
```
2. Install Dependencies
```
pip install uagents requests
```
3. Run the Orchestrator
```
python world_money_map_agent.py

```
💬 Message Protocols & Data Models

Query Request Schema (WorldMoneyMapQueryRequest)

{
  "scope": "FULL_MAP"
}

```
Response Schema (WorldMoneyMapQueryResponse)
```

{
  "agent_version": "3.0.0",
  "timestamp": 1722880000.0,
  "global_capital_flow_score": 0.88,
  "global_stock_pyramid_usd": {
    "real_estate_usd": "670T - 680T",
    "global_bond_debt_usd": "300T",
    "crypto_market_cap_usd": "2.16T"
  },
  "macro_capital_flight_signal": {
    "flight_detected": true,
    "source_asset": "TradFi Equities & US Debt ($39.9T)",
    "target_asset": "Tokenized Gold (PAXG/XAUT) & BTC ETF Flows",
    "confidence_score": 0.92
  }
}

```
⚖️ Disclaimer
NOT FINANCIAL ADVICE. This software is generated automatically for informational, research, and analytical purposes only. It does not constitute investment, legal, or tax advice.
```
