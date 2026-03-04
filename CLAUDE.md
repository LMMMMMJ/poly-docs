# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A direct mirror of official Polymarket API documentation. Content is fetched verbatim from `https://docs.polymarket.com` via `scripts/fetch-docs.py` — no LLM interpretation. The goal is accuracy and reproducibility.

## Common Commands

```bash
# Fetch/update all docs (recommended)
nix run .#fetch-docs

# Or in a dev shell
nix develop
python scripts/fetch-docs.py

# Options
python scripts/fetch-docs.py --dry-run   # preview without writing files
python scripts/fetch-docs.py --force     # re-fetch even if content unchanged
```

## Architecture

```
flake.nix                    # Nix flake: nixpkgs=nixos-25.11, flake-utils
pkgs/
  dev-shell/default.nix      # mkShell with python3 + requests
  fetch-docs/default.nix     # writeShellApplication wrapping the script
scripts/
  fetch-docs.py              # The scraper (single file, ~310 lines)
docs/                        # Mirrored from docs.polymarket.com URL structure
specs/                       # OpenAPI/AsyncAPI specs (.yaml, .json)
docs/MANIFEST.md             # Auto-generated: timestamps + per-file status
```

### How the Scraper Works

1. Fetches `https://docs.polymarket.com/llms.txt` — sitemap in Markdown link format `[Title](URL)`
2. Maps each URL: `.md` → `docs/<url-path>`, `.yaml/.json` → `specs/<url-path>`
3. For `.md` files: applies `clean_mdx()` to strip JSX/MDX syntax (import/export statements, JSX component tags) while preserving all Markdown content
4. Incremental: compares MD5 content hashes, skips unchanged files
5. Writes `docs/MANIFEST.md` with fetch timestamp and per-file status

### Key Implementation Notes

- `llms.txt` uses **Markdown link syntax** `[Title](URL)`, not bare URLs — the regex `_RE_MD_LINK_URL` extracts URLs from inside parentheses
- `clean_mdx()` tracks fenced code blocks (```` ``` ````) to avoid modifying content inside them
- The Nix package uses `builtins.path` to copy the script into the nix store for `writeShellApplication`
- Rate limit: 0.3s between requests, exponential backoff on 429/503
