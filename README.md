World Money Map (WMM) Autonomous Agent Network
複数の市場・アセットクラスをリアルタイム監視し、自動でマクロ資金流動性スコア（Capital Flow Score）を分析・合成する自律型マルチAIエージェントシステムです。

🏗️ システムアーキテクチャ
中央の Orchestrator Agent が各専門領域の 5 つの Sub-Agent と非同期分散通信を行い、包括的な市場統合データを収集・算出します。
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
エージェント名,監視ドメイン,取得・分析データ指標,主なデータソース / 外部API
13Chain Sub-Agent,マルチチェーンWeb3,EVM / Solana クロスチェーンアクティビティ、ガス価格、オンチェーン流動性,"Alchemy (Ethereum, Solana, Base, Linea)"
TradFi Sub-Agent,伝統的金融・マクロ経済,米国10年債利回り（US10Y）、ドルインデックス（DXY）、金利動向,マクロ指標データフィード
Metal Sub-Agent,貴金属・コモディティ,金/銀比率、脱ドル化進展指標、中央銀行準備資産動向,コモディティ・リアルタイムフィード
AI & DePIN Sub-Agent,AIインフラ・分散インフラ,H100/A100 GPU クラスタ利用率、Bittensor (TAO) ステーキング率,DePIN ネットワークモニタ
Real Estate Sub-Agent,実物資産（RWA）,グローバル不動産 Cap Rate（還元利回り）、機関投資家資金フロー,不動産・RWAデータアナリティクス
```
```
⚙️ 環境構築 ＆ サービス登録
1. 環境変数 (.env.*) の配置
~/Documents/ 配下に各エージェントごとの環境変数ファイルを配置します。
```
~/Documents/
├── .env.orchestrator
├── .env.13chain
├── .env.tradfi
├── .env.metal
├── .env.aidepin
└── .env.realestate
```
各ファイルには以下の変数を設定し、適切なアクセス制限（chmod 600）を付与します：
```
