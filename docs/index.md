> ## Documentation Index
> Fetch the complete documentation index at: https://docs.polymarket.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Overview

> Build on the world's largest prediction market. Trade, integrate, and access real-time market data with the Polymarket API.

  return (
    <a
      className="group flex flex-col p-5 border border-gray-200 dark:border-zinc-800 rounded-2xl hover:border-gray-300 dark:hover:border-zinc-700 hover:bg-gray-50 dark:hover:bg-zinc-900/50 transition-all duration-200"
      href={href}
    >
      <div
        className="flex items-center justify-center w-10 h-10 rounded-lg mb-4"
        style={{ backgroundColor: color ? `${color}1A` : "#2E5CFF15" }}
      >
      </div>
      <h3 className="text-base font-semibold text-gray-900 dark:text-zinc-50">
        {title}
      </h3>
      <p className="mt-1.5 text-sm text-gray-500 dark:text-zinc-400">
        {description}
      </p>
    </a>
  );
};

<svg className=" absolute stroke-black dark:stroke-white opacity-30 dark:opacity-40 top-0 right-0 md:w-[700px] md:h-[700px] w-[300px] h-[300px] pointer-events-none rotate-[-10deg] translate-x-20 md:translate-x-60 -translate-y-0 " width="1000" height="1205" viewBox="0 0 422 509" fill="none" xmlns="http://www.w3.org/2000/svg">
</svg>

<div className="relative overflow-hidden">
  <div className="relative z-10 py-18 max-w-6xl mx-auto ">
    <h1 className="block text-3xl px-4  md:px-24 font-semibold text-gray-900 dark:text-zinc-50 tracking-tight">
      Polymarket Documentation
    </h1>

    <div className="max-w-2xl px-4  md:px-24 mt-4 text-lg text-gray-500 dark:text-zinc-500">
      Build on the world's largest prediction market. APIs, SDKs, and tools for prediction market developers.
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12 px-4  md:px-24 ">
      <div className="flex flex-col justify-center ">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-zinc-50">
          Developer Quickstart
        </h2>

        <p className="mt-3 text-gray-500 dark:text-zinc-400">
          Make your first API request in minutes. Learn the basics of the Polymarket platform, fetch market data, place orders, and redeem winning positions.
        </p>

        <div className="mt-6">
          <a href="/quickstart" className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-primary rounded-full hover:bg-indigo-700 transition-colors">
            Get Started →
          </a>
        </div>
      </div>

        ```typescript TypeScript theme={null}
        import { ClobClient, Side } from "@polymarket/clob-client";

        const client = new ClobClient(host, chainId, signer, creds);

        const order = await client.createAndPostOrder(
          { tokenID, price: 0.50, size: 10, side: Side.BUY },
          { tickSize: "0.01", negRisk: false }
        );
        ```

        ```python Python theme={null}
        from py_clob_client.client import ClobClient
        from py_clob_client.order_builder.constants import BUY

        client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)
        order = client.create_and_post_order(
            OrderArgs(token_id=token_id, price=0.50, size=10, side=BUY),
            options={"tick_size": "0.01", "neg_risk": False}
        )
        ```
    </div>
  </div>

  <div className="max-w-6xl mx-auto px-4  md:px-24">
    <h2 className="text-2xl font-semibold text-gray-900 dark:text-zinc-50">
      Get Familiar with Polymarket
    </h2>

    <p className="mt-2 text-gray-500 dark:text-zinc-400 max-w-2xl">
      Learn the fundamentals, explore our APIs, and start building on the world's largest prediction market.
    </p>

    <div className="mt-8">
          Set up your environment and make your first API call in minutes.

          Understand markets, events, tokens, and how trading works.

          Explore REST endpoints, WebSocket streams, and authentication.

          Official Python and TypeScript libraries for faster development.
    </div>

    <div className="my-12 ">
      <a href="https://builders.polymarket.com" target="_blank">
      </a>
    </div>
  </div>

  <div className="max-w-6xl mx-auto px-4  md:px-24 pb-12">
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">

    </div>
  </div>
</div>
