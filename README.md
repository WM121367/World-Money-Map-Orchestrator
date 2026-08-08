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
