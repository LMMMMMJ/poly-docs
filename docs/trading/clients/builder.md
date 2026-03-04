> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Builder Methods

> Methods for querying orders and trades using builder API credentials.

## Client Initialization

Builder methods require the client to initialize with a separate builder config using credentials acquired from [Polymarket.com](https://polymarket.com/settings?tab=builder) and the `@polymarket/builder-signing-sdk` package.

      ```typescript TypeScript theme={null}
      import { ClobClient } from "@polymarket/clob-client";
      import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";

      const builderConfig = new BuilderConfig({
        localBuilderCreds: new BuilderApiKeyCreds({
          key: process.env.BUILDER_API_KEY,
          secret: process.env.BUILDER_SECRET,
          passphrase: process.env.BUILDER_PASS_PHRASE,
        }),
      });

      const clobClient = new ClobClient(
        "https://clob.polymarket.com",
        137,
        signer,
        apiCreds, // User's API credentials from L1 authentication
        signatureType,
        funderAddress,
        undefined,
        false,
        builderConfig
      );
      ```

      ```python Python theme={null}
      from py_clob_client.client import ClobClient
      from py_builder_signing_sdk.config import BuilderConfig, BuilderApiKeyCreds
      import os

      builder_config = BuilderConfig(
          local_builder_creds=BuilderApiKeyCreds(
              key=os.getenv("BUILDER_API_KEY"),
              secret=os.getenv("BUILDER_SECRET"),
              passphrase=os.getenv("BUILDER_PASS_PHRASE"),
          )
      )

      clob_client = ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key=os.getenv("PRIVATE_KEY"),
          creds=creds, # User's API credentials from L1 authentication
          signature_type=signature_type,
          funder=funder,
          builder_config=builder_config
      )
      ```

      ```typescript TypeScript theme={null}
      import { ClobClient } from "@polymarket/clob-client";
      import { BuilderConfig } from "@polymarket/builder-signing-sdk";

      const builderConfig = new BuilderConfig({
        remoteBuilderConfig: { url: "http://localhost:3000/sign" }
      });

      const clobClient = new ClobClient(
        "https://clob.polymarket.com",
        137,
        signer,
        apiCreds, // User's API credentials from L1 authentication
        signatureType,
        funder,
        undefined,
        false,
        builderConfig
      );
      ```

      ```python Python theme={null}
      from py_clob_client.client import ClobClient
      from py_builder_signing_sdk.config import BuilderConfig, RemoteBuilderConfig
      import os

      builder_config = BuilderConfig(
          remote_builder_config=RemoteBuilderConfig(
              url="http://localhost:3000/sign"
          )
      )

      clob_client = ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key=os.getenv("PRIVATE_KEY"),
          creds=creds, # User's API credentials from L1 authentication
          signature_type=signature_type,
          funder=funder,
          builder_config=builder_config
      )
      ```

  See [Order Attribution](/trading/orders/attribution) for more information on builder signing.

***

## Methods

***

### getOrder

Get details for a specific order by ID using builder authentication. When called from a builder-configured client, the request authenticates with builder headers and returns orders attributed to the builder.

```typescript Signature theme={null}
async getOrder(orderID: string): Promise<OpenOrder>
```

  When a `BuilderConfig` is present, the client automatically sends builder headers. If builder auth is unavailable, it falls back to standard L2 headers.

  ```typescript TypeScript theme={null}
  const order = await clobClient.getOrder("0xb816482a...");
  console.log(order);
  ```

  ```python Python theme={null}
  order = clob_client.get_order("0xb816482a...")
  print(order)
  ```

***

### getOpenOrders

Get all open orders attributed to the builder. When called from a builder-configured client, returns orders placed through the builder rather than orders owned by the authenticated user.

```typescript Signature theme={null}
async getOpenOrders(
  params?: OpenOrderParams,
  only_first_page?: boolean,
): Promise<OpenOrder[]>
```

**Params**

  Optional. Filter by order ID.

  Optional. Filter by market condition ID.

  Optional. Filter by token ID.

```typescript TypeScript theme={null}
// All open orders for this builder
const orders = await clobClient.getOpenOrders();

// Filtered by market
const marketOrders = await clobClient.getOpenOrders({
  market: "0xbd31dc8a...",
});
```

***

### getBuilderTrades

Retrieves all trades attributed to your builder account. Use this to track which trades were routed through your platform.

```typescript Signature theme={null}
async getBuilderTrades(
  params?: TradeParams,
): Promise<BuilderTradesPaginatedResponse>
```

**Params (`TradeParams`)**

  Optional. Filter trades by trade ID.

  Optional. Filter trades by maker address.

  Optional. Filter trades by market condition ID.

  Optional. Filter trades by asset (token) ID.

  Optional. Return trades created before this cursor value.

  Optional. Return trades created after this cursor value.

**Response (`BuilderTradesPaginatedResponse`)**

  Array of trades attributed to the builder account.

  Cursor string for fetching the next page of results.

  Maximum number of trades returned per page.

  Total number of trades returned in this response.

**`BuilderTrade` fields**

  Unique identifier for the trade.

  Type of the trade.

  Hash of the taker order associated with this trade.

  Address of the builder who attributed this trade.

  Condition ID of the market this trade belongs to.

  Token ID of the asset traded.

  Side of the trade (e.g. BUY or SELL).

  Size of the trade in shares.

  Size of the trade denominated in USDC.

  Price at which the trade was executed.

  Current status of the trade.

  Outcome label associated with the traded asset.

  Index of the outcome within the market.

  Address of the order owner (taker).

  Address of the maker in the trade.

  On-chain transaction hash for the trade.

  Timestamp when the trade was matched.

  Bucket index used for trade grouping.

  Fee charged for the trade in shares.

  Fee charged for the trade denominated in USDC.

  Optional. Error message if the trade encountered an issue, otherwise null.

  Timestamp when the trade record was created, or null if unavailable.

  Timestamp when the trade record was last updated, or null if unavailable.

***

### revokeBuilderApiKey

Revokes the builder API key used to authenticate the current request. After revocation, the key can no longer be used for builder-authenticated requests.

```typescript Signature theme={null}
async revokeBuilderApiKey(): Promise<any>
```

  Response from the revocation request.

***

## See Also

    Learn about the Builders Program and its benefits.

    Attribute orders to your builder account.

    Place and manage orders with API credentials.

    Execute onchain operations without paying gas.
