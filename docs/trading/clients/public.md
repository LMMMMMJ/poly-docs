> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Public Methods

> These methods can be called without a signer or user credentials. Use these for reading market data, prices, and order books.

## Client Initialization

Public methods require the client to initialize with the host URL and Polygon chain ID.

    ```typescript  theme={null}
    import { ClobClient } from "@polymarket/clob-client";

    const client = new ClobClient(
      "https://clob.polymarket.com",
      137
    );

    // Ready to call public methods
    const markets = await client.getMarkets();
    ```

    ```python  theme={null}
    from py_clob_client.client import ClobClient

    client = ClobClient(
        host="https://clob.polymarket.com",
        chain_id=137
    )

    # Ready to call public methods
    markets = client.get_markets()
    ```

***

## Health Check

***

### getOk

Health check endpoint to verify the CLOB service is operational.

```typescript Signature theme={null}
async getOk(): Promise<any>
```

***

## Markets

***

### getMarket

Get details for a single market by condition ID.

```typescript Signature theme={null}
async getMarket(conditionId: string): Promise<Market>
```

  Timestamp from which the market started accepting orders, or null if not set.

  Whether the market is currently accepting orders.

  Whether the market is active.

  Whether the market has been archived.

  Whether the market is closed.

  The unique condition ID for the market.

  Human-readable description of the market.

  Whether the order book is enabled for this market.

  ISO 8601 end date of the market.

  Address of the Fixed Product Market Maker contract.

  Start time of the underlying game or event.

  URL of the market icon image.

  URL of the market image.

  Whether the market has equal 50/50 outcomes.

  Base fee charged to makers in basis points.

  URL-friendly slug identifier for the market.

  Minimum order size allowed in this market.

  Minimum price increment allowed in this market.

  Whether the market uses negative risk (binary complementary tokens).

  Negative risk market identifier, if applicable.

  Negative risk request identifier, if applicable.

  Whether notifications are enabled for this market.

  The market question text.

  Unique identifier for the market question.

  Object containing reward config: `max_spread` (number), `min_size` (number), `rates` (any)

  Delay in seconds before orders are processed.

  List of tags associated with the market.

  Base fee charged to takers in basis points.

  Array of market tokens, each containing `outcome` (string), `price` (number), `token_id` (string), and `winner` (boolean).

***

### getMarkets

Get details for multiple markets paginated.

```typescript Signature theme={null}
async getMarkets(): Promise<PaginationPayload>
```

  Maximum number of results per page.

  Total number of markets returned.

  Array of Market objects. See `getMarket()` for the full Market structure.

***

### getSimplifiedMarkets

Get simplified market data paginated for faster loading.

```typescript Signature theme={null}
async getSimplifiedMarkets(): Promise<PaginationPayload>
```

  Maximum number of results per page.

  Total number of markets returned.

  Array of simplified market objects, each containing `accepting_orders` (boolean), `active` (boolean), `archived` (boolean), `closed` (boolean), `condition_id` (string), `rewards` (object with `rates`, `min_size`, `max_spread`), and `tokens` (SimplifiedToken\[]) with `outcome` (string), `price` (number), `token_id` (string).

***

### getSamplingMarkets

Get markets eligible for sampling/liquidity rewards.

```typescript Signature theme={null}
async getSamplingMarkets(): Promise<PaginationPayload>
```

***

### getSamplingSimplifiedMarkets

Get simplified market data for markets eligible for sampling/liquidity rewards.

```typescript Signature theme={null}
async getSamplingSimplifiedMarkets(): Promise<PaginationPayload>
```

***

## Order Books and Prices

***

### calculateMarketPrice

Calculate the estimated price for a market order of a given size.

```typescript Signature theme={null}
async calculateMarketPrice(
  tokenID: string,
  side: Side,
  amount: number,
  orderType: OrderType = OrderType.FOK
): Promise<number>
```

  The token ID to calculate the market price for.

  The side of the order. One of: `BUY`, `SELL`

  The size of the order to calculate price for.

  The order type. One of: `GTC` (Good Till Cancelled), `FOK` (Fill or Kill), `GTD` (Good Till Date), `FAK` (Fill and Kill). Defaults to `FOK`.

  The calculated estimated market price for the given order size.

***

### getOrderBook

Get the order book for a specific token ID.

```typescript Signature theme={null}
async getOrderBook(tokenID: string): Promise<OrderBookSummary>
```

  The market condition ID.

  The token/asset ID for this order book.

  Timestamp of the order book snapshot.

  Array of bid entries, each with `price` (string) and `size` (string).

  Array of ask entries, each with `price` (string) and `size` (string).

  Minimum order size for this market.

  Minimum price increment for this market.

  Whether the market uses negative risk.

  Hash of the order book state.

***

### getOrderBooks

Get order books for multiple token IDs.

```typescript Signature theme={null}
async getOrderBooks(params: BookParams[]): Promise<OrderBookSummary[]>
```

  The token ID to fetch the order book for.

  The side of the book to query. One of: `BUY`, `SELL`

  Array of OrderBookSummary objects. See `getOrderBook()` for the full structure.

***

### getPrice

Get the current best price for buying or selling a token ID.

```typescript Signature theme={null}
async getPrice(
  tokenID: string,
  side: "BUY" | "SELL"
): Promise<any>
```

  The current best price for the requested side.

***

### getPrices

Get the current best prices for multiple token IDs.

```typescript Signature theme={null}
async getPrices(params: BookParams[]): Promise<PricesResponse>
```

  A map of token IDs to their prices. Each entry contains an optional `BUY` (string) and/or `SELL` (string) price.

***

### getMidpoint

Get the midpoint price (average of best bid and best ask) for a token ID.

```typescript Signature theme={null}
async getMidpoint(tokenID: string): Promise<any>
```

  The midpoint price, calculated as the average of best bid and best ask.

***

### getMidpoints

Get the midpoint prices for multiple token IDs.

```typescript Signature theme={null}
async getMidpoints(params: BookParams[]): Promise<any>
```

  A map of token IDs to their midpoint price strings. Each key is a token ID and its value is the midpoint price as a string.

***

### getSpread

Get the spread (difference between best ask and best bid) for a token ID.

```typescript Signature theme={null}
async getSpread(tokenID: string): Promise<SpreadResponse>
```

  The spread value, calculated as the difference between best ask and best bid.

***

### getSpreads

Get the spreads for multiple token IDs.

```typescript Signature theme={null}
async getSpreads(params: BookParams[]): Promise<SpreadsResponse>
```

  A map of token IDs to their spread strings. Each key is a token ID and its value is the spread as a string.

***

### getPricesHistory

Get historical price data for a token.

```typescript Signature theme={null}
async getPricesHistory(params: PriceHistoryFilterParams): Promise<MarketPrice[]>
```

  The token ID to fetch price history for.

  Optional start timestamp (Unix seconds) for the price history range.

  Optional end timestamp (Unix seconds) for the price history range.

  Optional fidelity/resolution of the price history data.

  Time interval for the price history. One of: `max`, `1w`, `1d`, `6h`, `1h`

  Unix timestamp of the price data point.

  Price value at the corresponding timestamp.

***

## Trades

***

### getLastTradePrice

Get the price of the most recent trade for a token.

```typescript Signature theme={null}
async getLastTradePrice(tokenID: string): Promise<LastTradePrice>
```

  The price of the most recent trade.

  The side of the most recent trade.

***

### getLastTradesPrices

Get the most recent trade prices for multiple tokens.

```typescript Signature theme={null}
async getLastTradesPrices(params: BookParams[]): Promise<LastTradePriceWithToken[]>
```

  The price of the most recent trade for the token.

  The side of the most recent trade.

  The token ID this trade price corresponds to.

***

### getMarketTradesEvents

Get recent trade events for a market.

```typescript Signature theme={null}
async getMarketTradesEvents(conditionID: string): Promise<MarketTradeEvent[]>
```

  The type of trade event.

  Object containing market info: `condition_id` (string), `asset_id` (string), `question` (string), `icon` (string), `slug` (string).

  Object containing user info: `address` (string), `username` (string), `profile_picture` (string), `optimized_profile_picture` (string), `pseudonym` (string).

  The side of the trade. One of: `BUY`, `SELL`

  The size of the trade.

  The fee rate in basis points for the trade.

  The price at which the trade was executed.

  The outcome label for the traded token.

  The index of the outcome in the market.

  The on-chain transaction hash for the trade.

  The timestamp of when the trade event occurred.

***

## Market Parameters

***

### getFeeRateBps

Get the fee rate in basis points for a token.

```typescript Signature theme={null}
async getFeeRateBps(tokenID: string): Promise<number>
```

  The fee rate in basis points for the specified token.

***

### getTickSize

Get the tick size (minimum price increment) for a market.

```typescript Signature theme={null}
async getTickSize(tokenID: string): Promise<TickSize>
```

  The tick size for the market. One of: `0.1`, `0.01`, `0.001`, `0.0001`

***

### getNegRisk

Check if a market uses negative risk (binary complementary tokens).

```typescript Signature theme={null}
async getNegRisk(tokenID: string): Promise<boolean>
```

  Whether the market uses negative risk.

***

## Time and Server Info

### getServerTime

Get the current server timestamp.

```typescript Signature theme={null}
async getServerTime(): Promise<number>
```

  Unix timestamp in seconds representing the current server time.

***

## See Also

    Private key authentication to create or derive API credentials.

    Place orders, cancel orders, and query your trades.

    Complete REST endpoint documentation.

    Real-time market data streaming.
