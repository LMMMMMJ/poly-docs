# Polymarket 文档总览（中文）

> 本文件帮助 LLM 快速定位开发所需文档，避免逐一阅读全部内容。

---

## 一、核心概念速查

| 概念 | 结论 |
|------|------|
| 价格单位 | 0.0～1.0（即概率，0.65 = 65%） |
| 金额单位 | 6位小数定点（1000000 = 1 USDC） |
| 抵押品 | USDC.e（Polygon 上的 Bridged USDC，合约 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`） |
| 链 | Polygon 主网，chain ID = 137 |
| Token 标准 | ERC1155（Gnosis CTF） |
| 心跳 | 持有挂单时每 ≤10s POST `/heartbeats`，否则全部订单被取消 |
| 匹配引擎重启 | 每周二 7:00 AM ET，约 90s，期间返回 HTTP 425 |

---

## 二、API 基础信息

| API | Base URL | 认证 | 用途 |
|-----|----------|------|------|
| Gamma API | `https://gamma-api.polymarket.com` | 无 | 市场/事件/标签/搜索/评论/运动数据 |
| Data API | `https://data-api.polymarket.com` | 无 | 持仓/交易/排行榜/OI/分析 |
| CLOB API | `https://clob.polymarket.com` | 读取无需/交易需 L2 | 订单簿/定价/挂单/撤单/交易 |
| Bridge API | `https://bridge.polymarket.com` | 无 | 充提款（fun.xyz 代理） |
| WS 市场 | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | 无 | 实时订单簿/价格/成交 |
| WS 用户 | `wss://ws-subscriptions-clob.polymarket.com/ws/user` | 需要 | 实时订单/成交状态 |
| WS 体育 | `wss://sports-api.polymarket.com/ws` | 无 | 实时比赛比分 |
| RTDS | `wss://ws-live-data.polymarket.com` | 可选 | 实时数据流（高频） |

---

## 三、认证体系

**阅读认证相关开发时，优先读：**
- `docs/api-reference/authentication.md` — 完整 L1/L2 说明、Headers 表、EIP-712 签名示例
- `docs/trading/overview.md` — 签名类型（EOA/PROXY/GNOSIS_SAFE）及初始化客户端

**L1 认证**（一次性使用，创建 API 凭证）：
- EIP-712 签名，Header: `POLY_ADDRESS / POLY_SIGNATURE / POLY_TIMESTAMP / POLY_NONCE`
- 端点：`POST /auth/api-key` 或 `GET /auth/derive-api-key`

**L2 认证**（每次交易请求）：
- HMAC-SHA256 签名，5 个 Header: `POLY_ADDRESS / POLY_SIGNATURE / POLY_TIMESTAMP / POLY_API_KEY / POLY_PASSPHRASE`

**签名类型**（初始化客户端时必填）：

| 类型 | ID | 使用场景 |
|------|----|---------|
| EOA | 0 | 标准以太坊钱包，自付 Gas |
| POLY_PROXY | 1 | Magic Link/Google 登录用户（已从 Polymarket.com 导出私钥） |
| GNOSIS_SAFE | 2 | 浏览器钱包/嵌入钱包，最常用 |

---

## 四、文档目录与用途

### 4.1 入门文档

| 文件 | 内容 |
|------|------|
| `docs/quickstart.md` | 5分钟上手：取市场 → 初始化客户端 → 挂第一单（含 TS/Python 示例） |
| `docs/polymarket-101.md` | 平台基础：价格即概率、非托管、CTF Token、交易/解析流程 |
| `docs/index.md` | 官方首页（含大量 JSX 残留，内容价值低） |

### 4.2 核心概念

| 文件 | 内容摘要 |
|------|---------|
| `docs/concepts/markets-events.md` | Market（二元问题，有 conditionId/questionId/tokenIds）与 Event（容器，可含多个 Market）的关系；slug 来源于 URL |
| `docs/concepts/positions-tokens.md` | Yes/No ERC1155 Token；Split（USDC→Yes+No）、Merge（Yes+No→USDC）、Redeem（赢家 Token→USDC）操作 |
| `docs/concepts/prices-orderbook.md` | 价格 = 概率（0~1）；显示价 = 买卖中点；订单簿结构；市价单/限价单区别 |
| `docs/concepts/order-lifecycle.md` | 订单类型（GTC/GTD/FOK/FAK）；EIP-712 签名流程；链下撮合+链上结算 |
| `docs/concepts/resolution.md` | UMA 乐观预言机；提案→2h 挑战期→结算；争议→DVM 投票；结果 Yes/No/50-50 |

### 4.3 API 参考（各端点）

#### Gamma API（市场数据发现）

| 文件 | 端点 | 关键参数 |
|------|------|---------|
| `docs/api-reference/markets/list-markets.md` | `GET /markets` | slug, condition_ids, clob_token_ids, active, closed, limit, offset |
| `docs/api-reference/markets/get-market-by-id.md` | `GET /markets/{id}` | — |
| `docs/api-reference/markets/get-market-by-slug.md` | `GET /markets/slug/{slug}` | — |
| `docs/api-reference/markets/get-prices-history.md` | `GET /markets/{id}/prices-history` | interval, fidelity, startTs, endTs |
| `docs/api-reference/markets/get-sampling-markets.md` | `GET /sampling-markets` | 随机采样市场 |
| `docs/api-reference/markets/get-simplified-markets.md` | `GET /simplified-markets` | 精简字段列表 |
| `docs/api-reference/events/list-events.md` | `GET /events` | slug, tag_id, active, closed |
| `docs/api-reference/events/get-event-by-id.md` | `GET /events/{id}` | — |
| `docs/api-reference/events/get-event-by-slug.md` | `GET /events/slug/{slug}` | — |
| `docs/api-reference/tags/list-tags.md` | `GET /tags` | — |
| `docs/api-reference/series/list-series.md` | `GET /series` | — |
| `docs/api-reference/search/search-markets-events-and-profiles.md` | `GET /public-search` | q |
| `docs/api-reference/profiles/get-public-profile-by-wallet-address.md` | `GET /profiles/{address}` | — |
| `docs/api-reference/comments/list-comments.md` | `GET /comments` | market |
| `docs/api-reference/sports/get-sports-metadata-information.md` | `GET /sports` | — |

#### CLOB API 市场数据（公开，无需认证）

| 文件 | 端点 | 说明 |
|------|------|------|
| `docs/api-reference/market-data/get-order-book.md` | `GET /book?token_id=` | 订单簿快照（bids/asks/last_trade_price） |
| `docs/api-reference/market-data/get-order-books-request-body.md` | `POST /books` | 批量获取订单簿 |
| `docs/api-reference/market-data/get-market-price.md` | `GET /price?token_id=&side=` | 单个 Token 当前价格 |
| `docs/api-reference/market-data/get-market-prices-request-body.md` | `POST /prices` | 批量价格 |
| `docs/api-reference/market-data/get-midpoint-prices-query-parameters.md` | `GET /midpoint?token_id=` | 中间价 |
| `docs/api-reference/market-data/get-spread.md` | `GET /spread?token_id=` | 买卖价差 |
| `docs/api-reference/market-data/get-tick-size.md` | `GET /tick-size?token_id=` | 最小价格单位（0.1/0.01/0.001/0.0001） |
| `docs/api-reference/market-data/get-fee-rate.md` | `GET /neg-risk?token_id=` | 费率 |
| `docs/api-reference/market-data/get-last-trade-price.md` | `GET /last-trade-price?token_id=` | 最近成交价 |
| `docs/api-reference/data/get-midpoint-price.md` | `GET /midpoint` (CLOB) | — |
| `docs/api-reference/data/get-server-time.md` | `GET /time` | 服务器时间 |

#### CLOB API 交易（需要 L2 认证）

| 文件 | 端点 | 说明 |
|------|------|------|
| `docs/api-reference/trade/post-a-new-order.md` | `POST /order` | 提交单个订单（含完整 order 对象结构） |
| `docs/api-reference/trade/post-multiple-orders.md` | `POST /orders` | 批量提交订单 |
| `docs/api-reference/trade/cancel-single-order.md` | `DELETE /order/{id}` | 撤销单个订单 |
| `docs/api-reference/trade/cancel-multiple-orders.md` | `DELETE /orders` | 批量撤单 |
| `docs/api-reference/trade/cancel-orders-for-a-market.md` | `DELETE /orders/{market}` | 撤销某市场全部订单 |
| `docs/api-reference/trade/cancel-all-orders.md` | `DELETE /orders/all` | 撤销所有订单 |
| `docs/api-reference/trade/get-user-orders.md` | `GET /orders?maker=` | 查询用户挂单 |
| `docs/api-reference/trade/get-single-order-by-id.md` | `GET /orders/{id}` | 查询单个订单 |
| `docs/api-reference/trade/get-trades.md` | `GET /trades?maker=` | 查询成交记录 |
| `docs/api-reference/trade/send-heartbeat.md` | `POST /heartbeats` | 维持挂单心跳（≤10s 一次） |
| `docs/api-reference/trade/get-builder-trades.md` | `GET /builders/trades` | Builder 专属交易查询 |
| `docs/api-reference/rebates/get-current-rebated-fees-for-a-maker.md` | `GET /rebates/maker` | Maker 返佣 |

#### Data API（用户数据，无需认证）

| 文件 | 端点 | 说明 |
|------|------|------|
| `docs/api-reference/core/get-current-positions-for-a-user.md` | `GET /positions?user=` | 用户当前持仓（支持 redeemable/mergeable 过滤） |
| `docs/api-reference/core/get-closed-positions-for-a-user.md` | `GET /closed-positions?user=` | 已平仓持仓 |
| `docs/api-reference/core/get-trades-for-a-user-or-markets.md` | `GET /trades?user=` | 用户交易历史 |
| `docs/api-reference/core/get-user-activity.md` | `GET /activity?user=` | 用户操作历史（Split/Merge/Redeem 等） |
| `docs/api-reference/core/get-trader-leaderboard-rankings.md` | `GET /leaderboard` | 交易者排行榜 |
| `docs/api-reference/core/get-top-holders-for-markets.md` | `GET /positions/holders?market=` | 市场最大持仓者 |
| `docs/api-reference/core/get-total-value-of-a-users-positions.md` | `GET /value?user=` | 用户持仓总价值 |
| `docs/api-reference/misc/get-open-interest.md` | `GET /open-interest` | 全网未平仓合约量 |
| `docs/api-reference/misc/get-live-volume-for-an-event.md` | `GET /volume?eventId=` | 事件实时成交量 |
| `docs/api-reference/misc/download-an-accounting-snapshot-zip-of-csvs.md` | `GET /snapshot` | 下载会计快照 ZIP |

#### Bridge API

| 文件 | 端点 | 说明 |
|------|------|------|
| `docs/api-reference/bridge/create-deposit-addresses.md` | `POST /deposit` | 生成充值地址（EVM/SVM/BTC/TVM） |
| `docs/api-reference/bridge/create-withdrawal-addresses.md` | `POST /withdraw` | 发起提款 |
| `docs/api-reference/bridge/get-a-quote.md` | `GET /quote` | 获取跨链报价 |
| `docs/api-reference/bridge/get-transaction-status.md` | `GET /status/{address}` | 查询充提状态 |
| `docs/api-reference/bridge/get-supported-assets.md` | `GET /supported-assets` | 支持的资产和最小充值量 |

#### Builder API

| 文件 | 端点 | 说明 |
|------|------|------|
| `docs/api-reference/builders/get-aggregated-builder-leaderboard.md` | `GET /builders/leaderboard` | Builder 排行榜 |
| `docs/api-reference/builders/get-daily-builder-volume-time-series.md` | `GET /builders/volume` | Builder 日成交量时序 |

#### WebSocket

| 文件 | 内容 |
|------|------|
| `docs/api-reference/wss/market.md` | 市场频道规范（book/price_change/tick_size_change/last_trade_price/best_bid_ask/new_market/market_resolved） |
| `docs/api-reference/wss/user.md` | 用户频道规范（trade/order 事件，需要 L2 认证订阅） |
| `docs/api-reference/wss/sports.md` | 体育频道规范（sport_result 实时比分） |

### 4.4 参考资料

| 文件 | 内容 |
|------|------|
| `docs/api-reference/rate-limits.md` | 各 API 限速表（Gamma: 300/10s `/markets`；CLOB: 1500/10s `/book`；Data: 200/10s `/trades`） |
| `docs/api-reference/geoblock.md` | 地理封锁：封锁国家列表（含中国以外大部分主流国家）；检测接口 `GET https://polymarket.com/api/geoblock` |
| `docs/api-reference/clients-sdks.md` | 官方 SDK：TS `@polymarket/clob-client`、Python `py-clob-client`、Rust `polymarket-client-sdk`；Builder SDK；Relayer SDK |
| `docs/resources/error-codes.md` | CLOB 错误码大全（Unauthorized/Invalid token/Too Many Requests/425 等） |
| `docs/resources/contract-addresses.md` | Polygon 主网合约地址（CTF Exchange、Neg Risk Exchange、CTF、USDC.e、UMA Adapter） |
| `docs/resources/blockchain-data.md` | 链上数据：Goldsky（实时流）、Dune（SQL 分析）、Allium；社区 Dashboard 链接 |

### 4.5 交易指南

| 文件 | 内容 |
|------|------|
| `docs/trading/overview.md` | 整体交易流程、L1/L2 认证、签名类型、REST API 请求头说明 |
| `docs/trading/quickstart.md` | 快速开始交易（含 SDK 示例） |
| `docs/trading/fees.md` | 费率结构：大部分市场免费；加密/NCAAB/Serie A 市场收 Taker 费（最高 1.56%@50%概率） |
| `docs/trading/orderbook.md` | 订单簿机制详解 |
| `docs/trading/matching-engine.md` | 匹配引擎重启（周二 7AM ET，90s，HTTP 425）；退避重试策略 |
| `docs/trading/gasless.md` | Gasless 交易：需要 Builder 凭证 + Relayer Client；覆盖钱包部署/授权/CTF 操作/转账 |
| `docs/trading/orders/overview.md` | 订单类型（GTC/GTD/FOK/FAK）；Tick Size（0.1/0.01/0.001/0.0001）；Post-Only；Neg Risk 标志 |
| `docs/trading/orders/create.md` | 创建订单完整示例（SDK + REST 两种方式）；市价单/限价单 |
| `docs/trading/orders/cancel.md` | 撤单操作 |
| `docs/trading/orders/attribution.md` | Builder 订单归因：添加 `POLY_BUILDER_*` Headers；本地/远程签名两种模式 |
| `docs/trading/clients/public.md` | 公开客户端（无需认证） |
| `docs/trading/clients/l1.md` | L1 客户端（获取 API 凭证） |
| `docs/trading/clients/l2.md` | L2 客户端（完整交易功能） |
| `docs/trading/clients/builder.md` | Builder 客户端（含 BuilderConfig 初始化） |

### 4.6 CTF（条件 Token 框架）

| 文件 | 内容 |
|------|------|
| `docs/trading/ctf/overview.md` | CTF 原理；Token ID 计算（conditionId → collectionId → positionId）；Neg Risk Adapter |
| `docs/trading/ctf/split.md` | Split：USDC → Yes+No Token；前提条件、合约参数 |
| `docs/trading/ctf/merge.md` | Merge：Yes+No → USDC（等量） |
| `docs/trading/ctf/redeem.md` | Redeem：赢家 Token → USDC（市场结算后） |

### 4.7 充提款

| 文件 | 内容 |
|------|------|
| `docs/trading/bridge/deposit.md` | 充值流程：支持 EVM/SVM/BTC/TVM；USDC vs USDC.e 区别；>$5万建议用 DeBridge |
| `docs/trading/bridge/withdraw.md` | 提款流程 |
| `docs/trading/bridge/quote.md` | 查询跨链报价 |
| `docs/trading/bridge/status.md` | 查询交易状态 |
| `docs/trading/bridge/supported-assets.md` | 支持资产列表 |

### 4.8 市场数据获取指南

| 文件 | 内容 |
|------|------|
| `docs/market-data/overview.md` | 市场数据架构（Events 包含 Markets）；Gamma + CLOB + Data API 分工 |
| `docs/market-data/fetching-markets.md` | 三种查询策略：按 Slug / 按 Tags / 通过 Events 端点批量获取；分页参数 |
| `docs/market-data/subgraph.md` | Goldsky GraphQL 子图（5 个子图：持仓/订单/活动/OI/PNL） |
| `docs/market-data/websocket/overview.md` | 4 个 WS 频道对比（Market/User/Sports/RTDS）；订阅消息格式 |
| `docs/market-data/websocket/market-channel.md` | 市场频道详细消息格式（book/price_change/last_trade_price 等含完整 JSON 示例） |
| `docs/market-data/websocket/user-channel.md` | 用户频道（trade/order 事件，认证订阅） |
| `docs/market-data/websocket/rtds.md` | RTDS 高频实时数据服务 |
| `docs/market-data/websocket/sports.md` | 体育 WS |

### 4.9 Builder 计划

| 文件 | 内容 |
|------|------|
| `docs/builders/overview.md` | Builder 定义（为用户路由订单）；权益（Relayer/排行榜/周奖励/工程支持） |
| `docs/builders/api-keys.md` | 获取 Builder API Key 步骤（polymarket.com/settings?tab=builder） |
| `docs/builders/tiers.md` | 三级（Unverified/Verified/Partner）：Relayer 限额 100/3000/无限；Verified+ 可见排行榜+周奖励 |

### 4.10 做市商

| 文件 | 内容 |
|------|------|
| `docs/market-makers/overview.md` | 做市商职责；快速参考表（充值/授权/挂单/监控订单簿/Split/Merge 各用哪个工具） |
| `docs/market-makers/getting-started.md` | 部署钱包、充值 USDC.e、设置 Token 授权 |
| `docs/market-makers/trading.md` | 做市策略和最佳实践（警告：bid > ask 会亏损） |
| `docs/market-makers/inventory.md` | 库存管理：Split/Merge Token |
| `docs/market-makers/liquidity-rewards.md` | 流动性奖励算法（每日结算；基于二次评分函数奖励深度和紧密价差） |
| `docs/market-makers/maker-rebates.md` | Maker 返佣（仅收费市场：加密/NCAAB/Serie A；每日分配） |

### 4.11 高级主题

| 文件 | 内容 |
|------|------|
| `docs/advanced/neg-risk.md` | Neg Risk 市场：多结果事件的 No Token 可转换为其他结果的 Yes Token；通过 Neg Risk Adapter 合约；下单时需设 `negRisk: true` |

---

## 五、按开发任务快速定位文档

### 我想…获取市场列表/搜索市场
→ `docs/market-data/fetching-markets.md`（策略）
→ `docs/api-reference/markets/list-markets.md`（端点参数）
→ `docs/api-reference/events/list-events.md`（按事件获取）

### 我想…实时获取价格/订单簿
→ 轮询：`docs/api-reference/market-data/get-order-book.md`
→ 流式：`docs/market-data/websocket/market-channel.md`

### 我想…初始化交易客户端（认证）
→ `docs/api-reference/authentication.md`（完整认证文档）
→ `docs/trading/overview.md`（签名类型选择）
→ `docs/api-reference/clients-sdks.md`（SDK 安装）

### 我想…挂单/撤单
→ `docs/trading/orders/create.md`（创建订单，含代码）
→ `docs/trading/orders/overview.md`（GTC/GTD/FOK/FAK 区别、Tick Size）
→ `docs/api-reference/trade/post-a-new-order.md`（端点 schema）
→ `docs/api-reference/trade/send-heartbeat.md`（心跳，持仓挂单时必须）

### 我想…查看用户持仓/交易历史
→ `docs/api-reference/core/get-current-positions-for-a-user.md`
→ `docs/api-reference/core/get-trades-for-a-user-or-markets.md`

### 我想…充值/提款
→ `docs/trading/bridge/deposit.md`
→ `docs/api-reference/bridge/create-deposit-addresses.md`

### 我想…做市（Split/Merge Token）
→ `docs/trading/ctf/split.md` / `docs/trading/ctf/merge.md`
→ `docs/market-makers/inventory.md`
→ `docs/resources/contract-addresses.md`（合约地址）

### 我想…接入 Builder 计划（Gasless 交易/归因）
→ `docs/builders/overview.md` + `docs/builders/api-keys.md`
→ `docs/trading/gasless.md`（Relayer Client）
→ `docs/trading/orders/attribution.md`（订单归因）

### 我想…处理多结果市场（选举/锦标赛）
→ `docs/advanced/neg-risk.md`
→ 下单时 `negRisk: true`，使用 Neg Risk CTF Exchange

### 我想…订阅实时推送
→ `docs/market-data/websocket/overview.md`（频道选择）
→ `docs/market-data/websocket/market-channel.md`（订单簿/价格推送）
→ `docs/market-data/websocket/user-channel.md`（个人订单/成交推送）

### 我想…查链上数据/做数据分析
→ `docs/market-data/subgraph.md`（GraphQL）
→ `docs/resources/blockchain-data.md`（Goldsky/Dune/Allium）

### 我想…了解费率/错误码/限速/封锁地区
→ `docs/trading/fees.md` / `docs/api-reference/rate-limits.md`
→ `docs/resources/error-codes.md` / `docs/api-reference/geoblock.md`

---

## 六、机器可读规范

| 文件 | 内容 |
|------|------|
| `specs/api-spec/clob-openapi.yaml` | CLOB API 完整 OpenAPI 规范 |
| `specs/api-spec/gamma-openapi.yaml` | Gamma API 完整 OpenAPI 规范 |
| `specs/api-spec/data-openapi.yaml` | Data API 完整 OpenAPI 规范 |
| `specs/api-spec/bridge-openapi.yaml` | Bridge API 完整 OpenAPI 规范 |
| `specs/asyncapi.json` | WebSocket 市场频道 AsyncAPI 规范 |
| `specs/asyncapi-user.json` | WebSocket 用户频道 AsyncAPI 规范 |
| `specs/asyncapi-sports.json` | WebSocket 体育频道 AsyncAPI 规范 |

> **提示**：每个 `docs/api-reference/` 下的端点文件均内嵌了对应的 OpenAPI YAML 片段（从 `specs/` 提取），可直接读取端点文件获取参数/响应 Schema，无需单独解析 YAML 规范。

---

*内容来源：https://docs.polymarket.com | 最后更新：见 `docs/MANIFEST.md`*
