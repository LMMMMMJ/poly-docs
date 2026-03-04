> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Matching Engine Restarts

> Restart schedule, maintenance windows, and how to handle downtime

The Polymarket matching engine undergoes periodic restarts for maintenance and upgrades. This page covers the restart schedule, how to detect and handle downtime, and where to get advance notice of changes.

***

## Restart Schedule

The matching engine restarts **weekly on Tuesdays at 7:00 AM ET**. During a restart window, the engine is temporarily unavailable — typically for about **90 seconds**.

|                      | Details                                     |
| -------------------- | ------------------------------------------- |
| **Cadence**          | Weekly                                      |
| **Day & time**       | Tuesday, 7:00 AM ET                         |
| **Typical duration** | \~90 seconds                                |
| **What happens**     | Order matching is paused, API returns `425` |

  Unscheduled restarts may occur for critical updates or hotfixes. These are announced with as much advance notice as possible.

***

## Announcements

Matching engine changes — planned restarts, updates, and maintenance windows — are announced **before they happen** in these channels:

    Join the Polymarket Trading APIs channel for real-time announcements.

    Join the #trading-apis channel in the Polymarket Discord.

Announcements typically include **what's changing**, the **scheduled time**, and the **expected downtime window**. The goal is \~2 days notice when possible.

***

## Handling HTTP 425

During a restart window, the CLOB API returns **HTTP 425 (Too Early)** on all order-related endpoints. This tells your client that the matching engine is restarting and will be back shortly.

### Recommended Retry Strategy

    When you receive an HTTP `425` response, the matching engine is restarting. Do not treat this as a permanent error.

    Wait and retry with exponential backoff. Start at 1–2 seconds and increase the interval on each retry.

    Once you receive a successful response, the engine is back online. Resume normal order flow.

### Code Examples

Check the HTTP status code on responses to the CLOB API and retry on `425`:

  ```typescript TypeScript theme={null}
  const CLOB_HOST = "https://clob.polymarket.com";

  async function postWithRetry(path: string, body: any, headers: Record<string, string>) {
    const MAX_RETRIES = 10;
    let delay = 1000;

    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      const response = await fetch(`${CLOB_HOST}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...headers },
        body: JSON.stringify(body),
      });

      if (response.status === 425) {
        console.log(`Engine restarting, retrying in ${delay / 1000}s...`);
        await new Promise((r) => setTimeout(r, delay));
        delay = Math.min(delay * 2, 30000);
        continue;
      }

      return response;
    }
    throw new Error("Engine restart exceeded maximum retry attempts");
  }
  ```

  ```python Python theme={null}
  import time
  import requests

  CLOB_HOST = "https://clob.polymarket.com"

  def post_with_retry(path, body, headers, max_retries=10):
      delay = 1

      for attempt in range(max_retries):
          response = requests.post(
              f"{CLOB_HOST}{path}",
              json=body,
              headers=headers,
          )

          if response.status_code == 425:
              print(f"Engine restarting, retrying in {delay}s...")
              time.sleep(delay)
              delay = min(delay * 2, 30)
              continue

          return response

      raise Exception("Engine restart exceeded maximum retry attempts")
  ```

***

## Best Practices

* **Subscribe to announcement channels** — get notified before restarts happen so you can prepare
* **Handle 425 gracefully** — treat it as a temporary condition, not an error; your retry logic should resume automatically
* **Avoid aggressive retries** — the engine needs time to reload orderbooks; rapid-fire retries won't speed things up and may hit rate limits once the engine is back
* **Log restart events** — track when your client encounters 425s to correlate with announced maintenance windows
