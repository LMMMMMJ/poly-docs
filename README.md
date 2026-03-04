# Polymarket API Documentation

LLM-friendly reference for the Polymarket prediction market APIs. All content is mirrored directly from the [official Polymarket documentation](https://docs.polymarket.com) — no LLM interpretation, no summarization.

## How to Use This Repo

**Start here:**
- `docs/quickstart.md` — fetch a market and place your first order in minutes
- `docs/api-reference/introduction.md` — API overview and base URLs
- `docs/api-reference/authentication.md` — L1/L2 auth, signature types, credentials

**Find any page by topic:** see [Documentation Map](#documentation-map) below, or check `docs/MANIFEST.md` for the full file list with source URLs and fetch timestamps.

**Find any endpoint:** check `specs/api-spec/` for OpenAPI YAML specs (machine-readable, all endpoints with params/responses).

## Updating Documentation

```bash
# Re-fetch all docs from official source
nix run .#fetch-docs

# Options
nix run .#fetch-docs -- --dry-run   # preview without writing
nix run .#fetch-docs -- --force     # re-fetch even if unchanged

# Or in dev shell
nix develop
python scripts/fetch-docs.py
```

The scraper reads `https://docs.polymarket.com/llms.txt`, fetches each page, strips MDX/JSX syntax to plain Markdown, and saves under `docs/` mirroring the official URL path. Specs go to `specs/`. See `docs/MANIFEST.md` for last-updated timestamp.

## APIs at a Glance

| API | Base URL | Auth | Purpose |
|-----|----------|------|---------|
| **Gamma API** | `https://gamma-api.polymarket.com` | None | Markets, events, tags, series, search, profiles, comments, sports |
| **Data API** | `https://data-api.polymarket.com` | None | Positions, trades, leaderboards, activity, open interest, analytics |
| **CLOB API** | `https://clob.polymarket.com` | None (read) / L2 (trading) | Orderbook, pricing, order management |
| **Bridge API** | `https://bridge.polymarket.com` | None | Deposits/withdrawals (proxy of fun.xyz) |

**WebSocket streams:**
- Market channel: `wss://ws-subscriptions-clob.polymarket.com/ws/market`
- User channel: `wss://ws-subscriptions-clob.polymarket.com/ws/user`
- Sports channel: `wss://sports-api.polymarket.com/ws`

## Authentication

The Gamma API, Data API, and CLOB read endpoints (orderbook, prices) are **fully public — no auth needed**.

CLOB trading endpoints use a two-level auth system:
- **L1 (Private Key):** EIP-712 signature to create/derive API credentials. Used once to bootstrap.
- **L2 (API Key):** HMAC-SHA256 signed headers for all trading requests. Requires 5 `POLY_*` headers.

**Signature types** (set when initializing the CLOB client):
- `0` = EOA (standard wallet, needs POL for gas)
- `1` = POLY_PROXY (Magic Link / Google login users)
- `2` = GNOSIS_SAFE (multisig proxy, most common for new integrations)

See `docs/api-reference/authentication.md` for full details, code examples, and troubleshooting.

## Key Concepts

**Prices** are probabilities: `0.0` to `1.0`. A price of `0.65` means 65¢ per share = 65% implied probability.

**Amounts** use 6-decimal fixed-point: `1000000` = 1 USDC.

**Collateral:** USDC.e (Bridged USDC on Polygon, `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`).

**Chain:** Polygon mainnet (chain ID `137`).

**Heartbeat:** POST `/heartbeats` every ≤10s while holding open orders, or all orders are canceled.

See `docs/concepts/` for markets/events model, token structure, orderbook, order lifecycle, and resolution.

## Documentation Map

```
docs/
├── quickstart.md                     # Start here — fetch a market, place an order
├── polymarket-101.md                 # Platform basics for newcomers
├── index.md                          # Official docs home page (heavy JSX residue)
│
├── concepts/                         # Core data model
│   ├── markets-events.md             # Market vs Event structure, slugs, condition IDs
│   ├── positions-tokens.md           # Yes/No tokens, CTF mechanics
│   ├── prices-orderbook.md           # How prices work, orderbook structure
│   ├── order-lifecycle.md            # Order states, matching, fills
│   └── resolution.md                 # How markets resolve
│
├── api-reference/                    # All REST endpoints (one file per endpoint)
│   ├── introduction.md               # API overview
│   ├── authentication.md             # L1/L2 auth, headers, signature types
│   ├── rate-limits.md                # Per-API rate limit tables
│   ├── geoblock.md                   # Blocked regions, check endpoint
│   ├── clients-sdks.md               # TypeScript, Python, Rust SDKs
│   │
│   ├── markets/                      # Gamma: list, get by ID/slug, tags, prices history
│   ├── events/                       # Gamma: list, get by ID/slug, tags
│   ├── tags/                         # Gamma: list, get, related tags
│   ├── series/                       # Gamma: list, get by ID
│   ├── search/                       # Gamma: search markets/events/profiles
│   ├── profiles/                     # Gamma: public profiles by wallet
│   ├── comments/                     # Gamma: list, get by ID/user
│   ├── sports/                       # Gamma: sports metadata, market types, teams
│   │
│   ├── market-data/                  # CLOB (public): orderbook, prices, spreads, tick size, fee rate
│   ├── data/                         # CLOB: midpoint price, server time
│   │
│   ├── trade/                        # CLOB (auth): post/cancel orders, get orders/trades, heartbeat
│   ├── rebates/                      # CLOB: maker rebate info
│   │
│   ├── core/                         # Data API: positions, trades, activity, leaderboard, holders
│   ├── misc/                         # Data API: open interest, volume, accounting snapshot
│   │
│   ├── bridge/                       # Bridge API: deposit, withdraw, quote, status, assets
│   ├── builders/                     # Builder leaderboard, volume time series
│   └── wss/                          # WebSocket: market channel, user channel, sports channel
│
├── market-data/                      # Guides for fetching market data
│   ├── overview.md
│   ├── fetching-markets.md           # Strategies: by slug, tag, event, pagination
│   ├── subgraph.md                   # Blockchain subgraph / Goldsky / Dune
│   └── websocket/                    # WebSocket deep-dives
│       ├── overview.md
│       ├── market-channel.md         # Subscribe to orderbook/price updates
│       ├── user-channel.md           # Subscribe to order/trade events
│       ├── rtds.md                   # Real-time data service
│       └── sports.md
│
├── trading/                          # Trading guides
│   ├── overview.md
│   ├── quickstart.md
│   ├── fees.md                       # Fee structure, maker/taker rates
│   ├── orderbook.md                  # Orderbook mechanics
│   ├── matching-engine.md            # Matching engine restart schedule (Tue 7AM ET)
│   ├── gasless.md                    # Gasless order submission
│   ├── orders/                       # Order creation, cancellation, attribution
│   ├── clients/                      # Auth client types: public, L1, L2, builder
│   ├── ctf/                          # Conditional Token Framework: split/merge/redeem
│   └── bridge/                       # Deposit/withdraw flow
│
├── builders/                         # Builder program
│   ├── overview.md
│   ├── api-keys.md                   # How to get builder API keys
│   └── tiers.md                      # Volume tiers and benefits
│
├── market-makers/                    # Market making program
│   ├── overview.md
│   ├── liquidity-rewards.md
│   ├── maker-rebates.md
│   ├── trading.md
│   └── inventory.md
│
├── resources/                        # Reference material
│   ├── contract-addresses.md         # Polygon mainnet contract addresses
│   ├── error-codes.md                # HTTP error codes, endpoint-specific errors
│   └── blockchain-data.md            # On-chain data: subgraph, Goldsky, Dune, Allium
│
├── advanced/
│   └── neg-risk.md                   # Negative risk markets explanation
│
└── MANIFEST.md                       # Auto-generated: fetch timestamps, file status

specs/
├── api-spec/
│   ├── clob-openapi.yaml             # CLOB API — full OpenAPI spec
│   ├── gamma-openapi.yaml            # Gamma API — full OpenAPI spec
│   ├── data-openapi.yaml             # Data API — full OpenAPI spec
│   └── bridge-openapi.yaml           # Bridge API — full OpenAPI spec
├── asyncapi.json                     # WebSocket market channel — AsyncAPI spec
├── asyncapi-user.json                # WebSocket user channel — AsyncAPI spec
└── asyncapi-sports.json              # WebSocket sports channel — AsyncAPI spec
```

## Official Resources

- Documentation: https://docs.polymarket.com
- Full sitemap: https://docs.polymarket.com/llms.txt
- Builder Program: https://builders.polymarket.com
- Status Page: https://status.polymarket.com
