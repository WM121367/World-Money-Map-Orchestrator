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
