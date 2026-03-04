> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Conditional Token Framework

> Onchain token mechanics powering Polymarket positions

All outcomes on Polymarket are tokenized using the **Conditional Token Framework (CTF)**, an open standard developed by Gnosis. Understanding CTF operations enables advanced trading strategies, market making, and direct smart contract interactions.

## What is CTF

The Conditional Token Framework creates **ERC1155 tokens** representing outcomes of prediction markets. Each binary market has two tokens:

| Token   | Redeems for   | Condition            |
| ------- | ------------- | -------------------- |
| **Yes** | \$1.00 USDC.e | Event occurs         |
| **No**  | \$1.00 USDC.e | Event does not occur |

These tokens are always **fully collateralized** — every Yes/No pair is backed by exactly \$1.00 USDC.e locked in the CTF contract.

## Core Operations

CTF provides three fundamental operations:

    Convert USDC.e into Yes + No token pairs

    Convert Yes + No pairs back to USDC.e

    Exchange winning tokens for USDC.e after resolution

## Token Flow

## Token Identifiers

Each outcome token has a unique **position ID** (also called token ID or asset ID), computed onchain in three steps.

### Step 1 - Condition ID

```
getConditionId(oracle, questionId, outcomeSlotCount)
```

| Parameter          | Type      | Value                                                            |
| ------------------ | --------- | ---------------------------------------------------------------- |
| `oracle`           | `address` | [UMA CTF Adapter](https://github.com/Polymarket/uma-ctf-adapter) |
| `questionId`       | `bytes32` | Hash of the UMA ancillary data                                   |
| `outcomeSlotCount` | `uint`    | `2` for all binary markets                                       |

### Step 2 - Collection IDs

```
getCollectionId(parentCollectionId, conditionId, indexSet)
```

| Parameter            | Type      | Value                                                           |
| -------------------- | --------- | --------------------------------------------------------------- |
| `parentCollectionId` | `bytes32` | `bytes32(0)` — always zero for top-level positions              |
| `conditionId`        | `bytes32` | The condition ID from step 1                                    |
| `indexSet`           | `uint`    | `1` (`0b01`) for the first outcome, `2` (`0b10`) for the second |

The `indexSet` is a bitmask denoting which outcome slots belong to a collection. It must be a nonempty proper subset of the condition's outcome slots. Binary markets always have exactly two collections — one per outcome.

### Step 3 - Position IDs

```
getPositionId(collateralToken, collectionId)
```

| Parameter         | Type      | Value                                     |
| ----------------- | --------- | ----------------------------------------- |
| `collateralToken` | `IERC20`  | USDC.e contract address on Polygon        |
| `collectionId`    | `bytes32` | One of the two collection IDs from step 2 |

The two resulting position IDs are the ERC1155 token IDs for the Yes and No outcomes of the market.

  You can look up token IDs directly via the Gamma API (`GET /markets` or `GET /events`
  — the `tokens` array on each market contains both outcome token IDs). Computing them
  manually is only necessary for direct smart contract integration.

## Standard vs Neg Risk Markets

Polymarket has two market types with different CTF configurations:

| Feature           | Standard Markets    | Neg Risk Markets      |
| ----------------- | ------------------- | --------------------- |
| CTF Contract      | ConditionalTokens   | ConditionalTokens     |
| Exchange Contract | CTF Exchange        | Neg Risk CTF Exchange |
| Multi-outcome     | Independent markets | Linked via conversion |
| `negRisk` flag    | `false`             | `true`                |

For neg risk markets, an additional **conversion** operation allows exchanging a No token for Yes tokens in all other outcomes. See [Negative Risk Markets](/advanced/neg-risk) for details.

## Contract Addresses

See [Contract Addresses](/resources/contract-addresses) for all Polymarket smart contract addresses on Polygon.

## Resources

    Gnosis Conditional Tokens smart contracts

    Python and TypeScript examples for onchain operations

## Next Steps

    Create outcome token pairs from USDC.e

    Convert token pairs back to USDC.e

    Collect winnings after resolution
