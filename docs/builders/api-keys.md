> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# API Keys

> Create and manage your Builder API credentials

Builder API keys authenticate your application with Polymarket's relayer and enable order attribution. You'll need these credentials to access gasless transactions and track volume.

## Accessing Your Builder Profile

    Go to
    [polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)

  Click your profile image → Select "Builders"

## Creating API Keys

In the **Builder Keys** section of your profile:

1. Click **"+ Create New"** to generate a new API key
2. **Copy all three values immediately** — the secret and passphrase are only shown once
3. Store them securely in your secrets manager or environment variables

Each API key includes three components:

| Component    | Description                                | Example                 |
| ------------ | ------------------------------------------ | ----------------------- |
| `key`        | Public identifier for your builder account | `abc123-def456-...`     |
| `secret`     | Secret key for signing requests            | `base64-encoded-secret` |
| `passphrase` | Additional authentication value            | `your-passphrase`       |

  The `secret` and `passphrase` are only displayed once when created. If you
  lose them, you'll need to generate a new key.

## Managing Keys

Create separate keys for different environments:

| Environment | Purpose                       |
| ----------- | ----------------------------- |
| Development | Testing and local development |
| Staging     | Pre-production testing        |
| Production  | Live trading                  |

## Profile Settings

Your builder profile includes customizable settings:

| Setting             | Description                                                             |
| ------------------- | ----------------------------------------------------------------------- |
| **Profile Picture** | Displayed on the [Builder Leaderboard](https://builders.polymarket.com) |
| **Builder Name**    | Public name shown on the leaderboard                                    |
| **Builder Address** | Your unique builder identifier (read-only)                              |
| **Current Tier**    | Your rate limit tier: Unverified, Verified, or Partner                  |

## Environment Variables

Store your credentials as environment variables:

    ```bash .env theme={null}
    POLY_BUILDER_API_KEY=your-api-key
    POLY_BUILDER_SECRET=your-secret
    POLY_BUILDER_PASSPHRASE=your-passphrase
    ```

    ```typescript  theme={null}
    import { BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";

    const builderCreds: BuilderApiKeyCreds = {
      key: process.env.POLY_BUILDER_API_KEY!,
      secret: process.env.POLY_BUILDER_SECRET!,
      passphrase: process.env.POLY_BUILDER_PASSPHRASE!,
    };
    ```

    ```python  theme={null}
    import os
    from py_builder_signing_sdk import BuilderApiKeyCreds

    builder_creds = BuilderApiKeyCreds(
        key=os.environ["POLY_BUILDER_API_KEY"],
        secret=os.environ["POLY_BUILDER_SECRET"],
        passphrase=os.environ["POLY_BUILDER_PASSPHRASE"],
    )
    ```

## Security Best Practices

| Practice                      | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| **Never commit credentials**  | Use `.gitignore` to exclude `.env` files                  |
| **Use environment variables** | Load credentials from env vars, not hardcoded strings     |
| **Use a secrets manager**     | AWS Secrets Manager, HashiCorp Vault, etc. for production |
| **Separate environments**     | Use different keys for dev, staging, and production       |
| **Monitor usage**             | Check the leaderboard for unexpected volume changes       |

  **Never expose Builder API credentials in client-side code.** Your secret and
  passphrase must stay on your server.

## Troubleshooting

    **Cause:** You've exceeded your tier's daily transaction limit.

    **Solution:**

    * Wait until the daily limit resets
    * [Contact Polymarket](/builders/tiers#contact) to upgrade your tier

    **Cause:** The secret and passphrase are only shown once when created.

    **Solution:** Create a new API key. You cannot recover the original values.

## Next Steps

    Configure your client to credit trades to your account.

    Learn about rate limits and how to upgrade.
