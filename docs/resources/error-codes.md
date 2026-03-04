> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Error Codes

> Complete reference for CLOB API error responses

All CLOB API errors return a JSON object with a single `error` field:

```json  theme={null}
{
  "error": "<message>"
}
```

***

## Global Errors

These errors can occur on **any authenticated endpoint**.

  `Unauthorized/Invalid api key` — Your API key is missing, expired, or invalid. Ensure you're sending all required [authentication headers](/trading/overview#authentication).

  `Invalid L1 Request headers` — Your L1 authentication headers (HMAC signature) are malformed or the signature doesn't match. See [Authentication](/api-reference/authentication).

  `Trading is currently disabled. Check polymarket.com for updates` — The exchange is temporarily paused. No orders (including cancels) are accepted.

  `Trading is currently cancel-only. New orders are not accepted, but cancels are allowed.` — The exchange is in cancel-only mode. You can cancel existing orders but cannot place new ones.

  `Too Many Requests` — You've exceeded the [rate limit](/api-reference/rate-limits). Back off and retry with exponential backoff.

***

## Order Book

Errors from the order book endpoints.

### GET book

  `Invalid token id` — The `token_id` query parameter is missing or not a valid token ID.

  `No orderbook exists for the requested token id`

### POST books

  `Invalid payload` — The request body is malformed or missing required fields.

  `Payload exceeds the limit` — Too many token IDs in a single request. Reduce the batch size.

***

## Pricing

Errors from price, midpoint, and spread endpoints.

### GET price

  `Invalid token id` — The `token_id` parameter is missing or invalid.

  `Invalid side` — The `side` parameter must be `BUY` or `SELL`.

  `No orderbook exists for the requested token id`

### POST prices

  `Invalid payload` — The request body is malformed or missing required fields.

  `Invalid side` — The `side` field must be `BUY` or `SELL`.

  `Payload exceeds the limit` — Too many token IDs in a single request.

### GET midpoint

  `Invalid token id` — The `token_id` parameter is missing or invalid.

  `No orderbook exists for the requested token id`

### POST midpoints

  `Invalid payload` — The request body is malformed or missing required fields.

  `Payload exceeds the limit` — Too many token IDs in a single request.

### GET spread

  `Invalid token id` — The `token_id` parameter is missing or invalid.

  `No orderbook exists for the requested token id`

### POST spreads

  `Invalid payload` — The request body is malformed or missing required fields.

  `Payload exceeds the limit` — Too many token IDs in a single request.

***

## Place Orders

Errors from order placement endpoints.

### POST order

  `Invalid order payload` — The request body is malformed, missing required fields, or contains invalid values.

  `the order owner has to be the owner of the API KEY` — The `maker` address in the order doesn't match the address associated with your API key.

  `the order signer address has to be the address of the API KEY`

  `'{address}' address banned` — This address has been banned from trading.

  `'{address}' address in closed only mode`

### POST orders

All errors from `POST /order` apply, plus:

  `Too many orders in payload: {N}, max allowed: {M}` — The batch contains more orders than the maximum allowed per request.

Per-order errors are returned in the `200` response array, with individual error messages for each failed order.

***

## Order Processing Errors

These errors are returned when an order passes initial validation but fails during processing. They appear in the response body of `POST /order` and `POST /orders`.

  `invalid post-only order: order crosses book` — A post-only (maker) order would immediately match. Adjust the price so it rests on the book.

  `order {id} is invalid. Price ({price}) breaks minimum tick size rule: {tick}` — The order price doesn't align with the market's tick size. Use [`GET /tick-size`](/api-reference/clob#get-tick-size) to check the valid tick size.

  `order {id} is invalid. Size ({size}) lower than the minimum: {min}` — The order size is below the market minimum.

  `order {id} is invalid. Duplicated.`

  `order {id} crosses the book`

  `not enough balance / allowance` — Insufficient USDC.e balance or token allowance. Check your balance with [`GET /balance-allowance`](/api-reference/clob#get-balance-allowance) and approve the exchange contract if needed.

  `invalid nonce` — The order nonce has already been used or is invalid.

  `invalid expiration` — The order expiration timestamp is in the past or invalid.

  `order canceled in the CTF exchange contract`

  `order match delayed due to market conditions`

  `order couldn't be fully filled. FOK orders are fully filled or killed.` — A Fill-or-Kill order could not be completely filled by available liquidity. The entire order is rejected.

  `no orders found to match with FAK order. FAK orders are partially filled or killed if no match is found.` — A Fill-and-Kill order found no matching orders at all. At least one match is required.

  `the market is not yet ready to process new orders`

***

## Matching Engine Errors

Internal matching engine errors that may surface during order execution.

  The matching engine is restarting. Retry with exponential backoff. See [Matching Engine](/trading/matching-engine) for details on restart schedule and handling.

  `there are no matching orders`

  `FOK orders are filled or killed` — A Fill-or-Kill order could not be fully satisfied.

  `the trade contains rounding issues`

  `the price of the taker's order has a discrepancy greater than allowed with the worst maker order`

***

## Cancel Orders

Errors from order cancellation endpoints.

### DELETE order

  `Invalid order payload` — The request body is malformed.

  `Invalid orderID` — The provided order ID is not a valid format.

### DELETE orders

  `Invalid order payload` — The request body is malformed.

  `Too many orders in payload, max allowed: {N}` — Too many order IDs in a single cancellation request.

  `Invalid orderID` — One or more order IDs are not valid.

### DELETE cancel-market-orders

  `Invalid order payload` — The request body is malformed or contains invalid filter parameters.

***

## Query Orders

Errors from order query endpoints.

### GET order by ID

  `Invalid orderID` — The order ID in the URL path is not valid.

  `Internal server error` — An unexpected error occurred while fetching the order.

### GET orders

  `invalid order params payload` — The query parameters are malformed or contain invalid values.

  `Internal server error` — An unexpected error occurred while fetching orders.

***

## Trades

### GET trades

  `Invalid trade params payload` — The query parameters are malformed or contain invalid values.

  `Internal server error` — An unexpected error occurred while fetching trades.

### GET last-trade-price

  `Invalid token id` — The `token_id` parameter is missing or invalid.

  `Internal server error` — An unexpected error occurred while fetching the last trade price.

### POST last-trades-prices

  `Invalid payload` — The request body is malformed or missing required fields.

  `Payload exceeds the limit` — Too many token IDs in a single request.

***

## Markets

### GET market by condition ID

  `Invalid market` — The condition ID is not a valid format.

  `market not found` — No market exists with this condition ID.

### GET tick-size

  `Invalid token id` — The token ID is not valid.

  `market not found` — No market found for this token ID.

### GET neg-risk

  `Invalid token id` — The token ID is not valid.

  `market not found` — No market found for this token ID.

***

## Price History

### GET prices-history

  Filter validation errors — One or more query parameters (`market`, `startTs`, `endTs`, `fidelity`) are invalid.

### GET ohlc

  `startTs is required` — The `startTs` query parameter is missing.

  `asset_id is required` — The `asset_id` query parameter is missing.

  `invalid fidelity: {val}` — The `fidelity` parameter must be one of: `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`, `1w`.

  `limit cannot exceed 1000` — Reduce the `limit` parameter to 1000 or below.

### GET orderbook-history

  `startTs is required` — The `startTs` query parameter is missing.

  `either market or asset_id must be provided` — You must specify either a `market` (condition ID) or `asset_id` (token ID).

  `limit cannot exceed 1000` — Reduce the `limit` parameter to 1000 or below.

***

## Authentication and API Keys

### POST auth api-key

  `Invalid L1 Request headers` — L1 authentication headers are missing or invalid.

  `Could not create api key`

### GET auth api-keys

  `Could not retrieve API keys` — An unexpected error occurred while fetching your API keys.

### DELETE auth api-key

  `Could not delete API key` — An unexpected error occurred while deleting the API key.

### GET auth derive-api-key

  `Invalid L1 Request headers` — L1 authentication headers are missing or invalid.

  `Could not derive api key!`

***

## Builder API Keys

### POST auth builder-api-key

  `could not create builder api key` — Builder API key creation failed.

### GET auth builder-api-key

  `could not get builder api keys` — An unexpected error occurred while fetching builder API keys.

### DELETE auth builder-api-key

  `invalid revoke builder api key body` — The request body is malformed.

  `invalid revoke builder api key headers` — Required authentication headers are missing.

  `could not revoke the builder api key: {key}` — An unexpected error occurred while revoking the key.

***

## Builder Trades

### GET builder trades

  `invalid builder trade params` — The query parameters are malformed or contain invalid values.

  `could not fetch builder trades` — An unexpected error occurred while fetching builder trades.

***

## Balance and Allowance

### GET balance-allowance

  `Invalid asset type` — The `asset_type` parameter is not a recognized asset type.

  `Invalid signature_type` — The `signature_type` parameter must be `EOA`, `POLY_PROXY`, or `GNOSIS_SAFE`.

***

## Status Code Reference

| Status | Meaning               | Common Causes                                                                                       |
| ------ | --------------------- | --------------------------------------------------------------------------------------------------- |
| `400`  | Bad Request           | Invalid parameters, malformed payload, business logic violation                                     |
| `401`  | Unauthorized          | Missing or invalid API key, bad HMAC signature, expired timestamp                                   |
| `404`  | Not Found             | Market doesn't exist, order not found, token ID not recognized                                      |
| `425`  | Too Early             | Matching engine is restarting — retry with backoff. See [Matching Engine](/trading/matching-engine) |
| `429`  | Too Many Requests     | Rate limit exceeded — implement exponential backoff                                                 |
| `500`  | Internal Server Error | Unexpected server error — retry with backoff                                                        |
| `503`  | Service Unavailable   | Exchange paused or in cancel-only mode                                                              |

  The CLOB API has an internal override: any error message containing `"not found"` returns `404`, `"unauthorized"` returns `401`, and `"context canceled"` returns `400`, regardless of the original status code.
