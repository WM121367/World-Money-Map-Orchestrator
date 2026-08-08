World Money Map (WMM) Autonomous Agent Network
An autonomous multi-AI agent system that monitors multiple financial markets and asset classes in real time, automatically analyzing and synthesizing a macro Capital Flow Score.

🏗️ System Architecture
The central Orchestrator Agent communicates asynchronously with 5 specialized Sub-Agents via distributed messaging protocols to aggregate and evaluate market data across multiple domains.
```
                        +--------------------------+
                        |   Client / External AI   |
                        +------------+-------------+
                                     | (uAgents Protocol)
                                     v
                        +--------------------------+
                        |  WMM Orchestrator Agent  |
                        +------------+-------------+
                                     |
    +-----------------+--------------+--------------+-----------------+-----------------+
    |                 |                             |                 |                 |
    v                 v                             v                 v                 v
+-------+     +---------------+             +---------------+     +-------+     +---------------+
|13Chain|     | AI & DePIN    |             | Metal Asset   |     | TradFi|     | Real Estate   |
|SubAgent     | Sub-Agent     |             | Sub-Agent     |     |SubAgent     | Sub-Agent     |
+-------+     +---------------+             +---------------+     +-------+     +---------------+
```

🌐 Specialized Sub-Agent DomainsSub-AgentDomainMonitored Metrics & IndicatorsData Sources & Integrations13Chain Sub-AgentMulti-chain Web3EVM & Solana cross-chain activity, gas prices, on-chain liquidityAlchemy API (Ethereum, Solana, Base, Linea)TradFi Sub-AgentTraditional Finance & MacroUS 10-Year Treasury Yield (US10Y), Dollar Index (DXY), rate benchmarksMacroeconomic data feedsMetal Sub-AgentPrecious Metals & CommoditiesGold/Silver ratio, de-dollarization trends, central bank reserve shiftsReal-time commodity market feedsAI & DePIN Sub-AgentAI & DePIN InfrastructureH100/A100 GPU cluster utilization, Bittensor (TAO) validator staking ratioDePIN network telemetry & monitorsReal Estate Sub-AgentReal World Assets (RWA)Global commercial real estate Cap Rates, institutional capital flow trackingReal Estate & RWA data analytics

```
⚙️ Setup & Service Deployment
1. Environment Configuration (.env.*)
Place individual environment configuration files in the ~/Documents/ directory:
```
~/Documents/
├── .env.orchestrator
├── .env.13chain
├── .env.tradfi
├── .env.metal
├── .env.aidepin
└── .env.realestate

```
Define the required keys in each configuration file and enforce strict file permissions (chmod 600):
```
AGENT_SEED_PHRASE=your_agent_seed_phrase
AGENTVERSE_KEY=your_agentverse_api_key
AGENTVERSE_SEED_PHRASE=your_agentverse_seed_phrase
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# 13Chain Sub-Agent Specific Keys:
ALCHEMY_SEPOLIA_KEY=alch_...
ALCHEMY_SOLANA_KEY=alch_...
ALCHEMY_BASE_KEY=alch_...
ALCHEMY_LINEA_KEY=alch_...

AGENT_SEED_PHRASE=your_agent_seed_phrase
AGENTVERSE_KEY=your_agentverse_api_key
AGENTVERSE_SEED_PHRASE=your_agentverse_seed_phrase
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

chmod 600 ~/Documents/.env.*

```
2. Continuous 24/7 Deployment via systemd

All 6 agent services are managed by systemd to ensure continuous background operation and automatic recovery on system boot.

Enable and Start All Services
```
sudo systemctl daemon-reload
sudo systemctl enable wmm-orchestrator wmm-sub-13chain wmm-sub-tradfi wmm-sub-metal wmm-sub-aidepin wmm-sub-realestate
sudo systemctl start wmm-orchestrator wmm-sub-13chain wmm-sub-tradfi wmm-sub-metal wmm-sub-aidepin wmm-sub-realestate

```
Check Active Service Status
```

sudo systemctl list-units --type=service | grep wmm

```
Run End-to-End Integration Test
```

python3 ~/Documents/test_client.py
