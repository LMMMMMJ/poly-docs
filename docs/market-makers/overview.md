> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Overview

> Market making on Polymarket

A Market Maker (MM) on Polymarket is a trader who provides liquidity to prediction markets by continuously posting bid and ask orders. By laying the spread, market makers enable other users to trade efficiently while earning the spread as compensation for the risk they take.

Market makers are essential to Polymarket's ecosystem — they provide liquidity across markets, tighten spreads for better user experience, enable price discovery through continuous quoting, and absorb trading flow from retail and institutional users.

  **Not a Market Maker?** If you're building an application that routes orders
  for your users, see the [Builder Program](/builders/overview) instead.

***

## Getting Started

    Deploy wallets, fund with USDC.e, and set token approvals. See the [Getting
    Started](/market-makers/getting-started) guide.

    WebSocket for real-time orderbook updates, Gamma API for market metadata.
    See [Market Data](/market-data/overview).

    Post orders via the CLOB REST API. See [Trading ](/market-makers/trading).

***

## Quick Reference

| Action                 | Tool           | Documentation                                     |
| ---------------------- | -------------- | ------------------------------------------------- |
| Deposit USDC.e         | Bridge API     | [Bridge](/trading/bridge/deposit)                 |
| Approve tokens         | Relayer Client | [Getting Started](/market-makers/getting-started) |
| Post limit orders      | CLOB REST API  | [Create Orders](/trading/orders/create)           |
| Monitor orderbook      | WebSocket      | [WebSocket](/market-data/websocket/overview)      |
| Split USDC.e to tokens | CTF / Relayer  | [Inventory](/market-makers/inventory)             |
| Merge tokens to USDC.e | CTF / Relayer  | [Inventory](/market-makers/inventory)             |

***

## What Is in This Section

    Deposits, token approvals, wallet deployment, API keys

    Quoting best practices, strategies, and risk controls

    Split, merge, and redeem outcome tokens

    Earn rewards for providing liquidity

## Risks

  Be careful with spread management — if your bid price is higher than your ask
  price (a "negative spread" or "crossed market"), you will lose money on every
  fill. Always validate your quote prices before submission.

## Support

For market maker onboarding and support, contact [support@polymarket.com](mailto:support@polymarket.com).
