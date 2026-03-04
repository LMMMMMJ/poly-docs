> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Builder Program

> Build applications that route orders through Polymarket

A **builder** is a person, group, or organization that routes orders from users to Polymarket. If you've created a platform that allows users to trade on Polymarket through your system, this program is for you.

## Program Benefits

    All onchain operations are gas-free through our relayer

    Get credit for orders and compete for grants on the Builder Leaderboard

### What You Get

| Benefit             | Description                                                                     |
| ------------------- | ------------------------------------------------------------------------------- |
| **Relayer Access**  | Gas-free wallet deployment, approvals, order execution and CTF operations       |
| **Volume Tracking** | All orders attributed to your builder profile                                   |
| **Weekly Rewards**  | USDC rewards program based on volume (Verified+)                                |
| **Leaderboard**     | Public visibility on [builders.polymarket.com](https://builders.polymarket.com) |
| **Support**         | Telegram channel and engineering support (Verified+)                            |

  EOA wallets do not have relayer access. Users trading directly from an EOA pay
  their own gas fees.

## How It Works

    User places an order through your application.

    Your app signs the request with Builder API credentials.

    Order is submitted to Polymarket's CLOB with attribution headers.

    Polymarket matches the order and covers gas fees for onchain operations.

    Volume is credited to your builder account.

## Getting Started

    Go to
    [polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)
    and generate your API keys.

    Set up your CLOB client to include builder authentication headers with every
    order.

    Use the Relayer Client for gas-free wallet deployment and onchain
    operations.

    Monitor your volume on the [Builder
    Leaderboard](https://builders.polymarket.com).

## SDKs and Libraries

    Place orders with builder attribution

    Place orders with builder attribution

    Gasless onchain transactions

    Gasless onchain transactions

    Place orders with builder attribution

    Sign builder authentication headers

    Sign builder authentication headers

## Examples

These open-source demo applications show how to integrate Polymarket's CLOB Client and Builder Relayer Client for gasless trading with builder order attribution.

    Multiple wallet providers

    Safe & Proxy wallet support

    Orders, positions, CTF ops

### Safe Wallet Examples

Deploy Gnosis Safe wallets for your users:

    MetaMask, Phantom, Rabby, and other browser wallets

    Privy embedded wallets

    Magic Link email/social authentication

    Turnkey embedded wallets

### Proxy Wallet Examples

For existing Magic Link users from Polymarket.com:

    Auto-deploying proxy wallets for Polymarket.com Magic users

### What Each Demo Covers

    * User sign-in via wallet provider
    * User API credential derivation (L2 auth)
    * Builder config with remote signing
    * Signature types for Safe vs Proxy wallets

    * Safe wallet deployment via Relayer
    * Batch token approvals (USDC.e + outcome tokens)
    * CTF operations (split, merge, redeem)
    * Transaction monitoring

    * CLOB client initialization
    * Order placement with builder attribution
    * Position and order management
    * Market discovery via Gamma API

***

## Next Steps

    Create and manage your Builder API credentials.

    Learn about rate limits and how to upgrade.

    Configure your client to credit trades to your account.

    Set up gasless transactions for your users.
