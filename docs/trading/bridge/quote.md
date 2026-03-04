> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quote

> Preview fees and estimated output for deposits and withdrawals

Get an estimated quote before executing a deposit or withdrawal. Quotes include estimated output amounts, checkout time, and a detailed fee breakdown.

## Get a Quote

```bash  theme={null}
curl -X POST https://bridge.polymarket.com/quote \
  -H "Content-Type: application/json" \
  -d '{
    "fromAmountBaseUnit": "10000000",
    "fromChainId": "137",
    "fromTokenAddress": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
    "recipientAddress": "0x17eC161f126e82A8ba337f4022d574DBEaFef575",
    "toChainId": "137",
    "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
  }'
```

### Request Parameters

| Parameter            | Type   | Description                                                   |
| -------------------- | ------ | ------------------------------------------------------------- |
| `fromAmountBaseUnit` | string | Amount to send in base units (e.g., `"10000000"` for 10 USDC) |
| `fromChainId`        | string | Source chain ID (e.g., `"137"` for Polygon)                   |
| `fromTokenAddress`   | string | Token contract address on the source chain                    |
| `recipientAddress`   | string | Destination wallet address to receive funds                   |
| `toChainId`          | string | Destination chain ID                                          |
| `toTokenAddress`     | string | Token contract address on the destination chain               |

### Response

The quote response includes:

| Field                | Type   | Description                             |
| -------------------- | ------ | --------------------------------------- |
| `estCheckoutTimeMs`  | number | Estimated checkout time in milliseconds |
| `estInputUsd`        | number | Estimated input value in USD            |
| `estOutputUsd`       | number | Estimated output value in USD           |
| `estToTokenBaseUnit` | string | Estimated output amount in base units   |
| `quoteId`            | string | Unique identifier for this quote        |
| `estFeeBreakdown`    | object | Detailed fee breakdown (see below)      |

### Fee Breakdown

The `estFeeBreakdown` object contains:

  Gas fee in USD

  Label of the app fee

  App fee as a percentage of the total amount

  App fee in USD

  Fill cost as a percentage of the total amount

  Fill cost in USD

  Maximum potential slippage as a percentage

  Minimum amount received after slippage

  Swap impact as a percentage of the total amount

  Swap impact in USD

  Total impact as a percentage of the total amount

  Total impact cost in USD

  Quotes are estimates. Actual amounts may vary slightly due to market
  conditions.

## Next Steps

    Execute a deposit to Polymarket.

    Withdraw from Polymarket to another chain.
