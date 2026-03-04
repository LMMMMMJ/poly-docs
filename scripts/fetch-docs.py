#!/usr/bin/env python3
"""
fetch-docs.py — Mirror Polymarket official documentation.

Fetches all pages from https://docs.polymarket.com/llms.txt,
cleans MDX/JSX syntax to plain Markdown, and saves to a local
mirror under docs/. OpenAPI/AsyncAPI specs are saved under specs/.

Usage:
    python fetch-docs.py [--dry-run] [--force]

Options:
    --dry-run   Fetch and process content but do not write files
    --force     Re-fetch and overwrite even if content is unchanged
"""

import argparse
import hashlib
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

BASE_URL = "https://docs.polymarket.com"
SITEMAP_URL = f"{BASE_URL}/llms.txt"
# When run via `nix run`, __file__ is inside /nix/store; use cwd instead.
_script_path = Path(__file__).resolve()
REPO_ROOT = Path.cwd() if str(_script_path).startswith("/nix/store") else _script_path.parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SPECS_DIR = REPO_ROOT / "specs"
MANIFEST_PATH = DOCS_DIR / "MANIFEST.md"

REQUEST_DELAY = 0.3   # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# JSX component names used by Mintlify (Polymarket's doc platform)
_JSX_COMPONENTS = (
    "Card", "CardGroup", "CodeGroup", "Accordion", "AccordionGroup",
    "Tabs", "Tab", "Frame", "Note", "Warning", "Info", "Tip", "Check",
    "Steps", "Step", "Update", "ResponseField", "ParamField",
    "RequestExample", "ResponseExample", "ExpandableRow", "Snippet",
    "IconCard", "Callout", "Columns", "Column", "Property", "Properties",
    "EndpointRequestSnippet", "EndpointResponseSnippet",
    "OpenApiParameters", "OpenApiResponse", "SwaggerUI",
    "api-playground", "ApiPlayground",
)
_JSX_NAMES = "|".join(_JSX_COMPONENTS)
_RE_OPEN_TAG = re.compile(rf"<({_JSX_NAMES})(\s[^>]*)?>")
_RE_CLOSE_TAG = re.compile(rf"</({_JSX_NAMES})>")
_RE_SELF_CLOSING = re.compile(r"<\w[\w.-]*(\s[^>]*)?\s*/>")
_RE_IMPORT = re.compile(r"^import\s+")
_RE_EXPORT_CONST = re.compile(r"^export\s+const\s+")
_RE_BLANK_LINES = re.compile(r"\n{3,}")


def fetch_url(session: requests.Session, url: str, retries: int = MAX_RETRIES) -> str | None:
    """Fetch a URL, return content string or None on failure."""
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=TIMEOUT)
            if resp.status_code == 200:
                return resp.text
            elif resp.status_code in (429, 503):
                wait = 2 ** (attempt + 1)
                print(f"  Rate limited ({resp.status_code}), waiting {wait}s...")
                time.sleep(wait)
            elif resp.status_code == 404:
                print(f"  404 Not Found: {url}")
                return None
            else:
                print(f"  HTTP {resp.status_code}: {url}")
                if attempt < retries - 1:
                    time.sleep(1)
        except requests.RequestException as e:
            print(f"  Request error: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None


def clean_mdx(content: str) -> str:
    """Convert MDX content to clean Markdown.

    Removes JSX/MDX-specific syntax while preserving all meaningful content:
    - Removes import/export statements
    - Strips JSX component open/close tags (inner content is kept)
    - Removes self-closing JSX components (carry no text content)
    - Collapses excessive blank lines
    """
    lines = content.splitlines()
    cleaned_lines = []
    in_code_block = False

    for line in lines:
        # Track fenced code blocks — never modify content inside them
        stripped_line = line.strip()
        if stripped_line.startswith("```") or stripped_line.startswith("~~~"):
            in_code_block = not in_code_block
            cleaned_lines.append(line)
            continue

        if in_code_block:
            cleaned_lines.append(line)
            continue

        # Remove import statements (MDX-specific)
        if _RE_IMPORT.match(line):
            continue

        # Remove export const statements (MDX-specific)
        if _RE_EXPORT_CONST.match(line):
            continue

        # Strip JSX open and close tags, keep inner content on same line
        processed = _RE_OPEN_TAG.sub("", line)
        processed = _RE_CLOSE_TAG.sub("", processed)
        processed = _RE_SELF_CLOSING.sub("", processed)

        # If this line was purely a JSX tag (now empty), skip it
        if processed.strip() == "" and line.strip().startswith("<"):
            continue

        cleaned_lines.append(processed)

    result = "\n".join(cleaned_lines)
    result = _RE_BLANK_LINES.sub("\n\n", result)
    return result.strip() + "\n"


def url_to_local_path(url: str) -> Path | None:
    """Map a docs URL to a local file path.

    .md files  -> DOCS_DIR / <url-path>
    .yaml/.json -> SPECS_DIR / <url-path>
    Other URLs  -> None (skip)
    """
    parsed = urlparse(url)
    if parsed.netloc != "docs.polymarket.com":
        return None
    path = parsed.path.lstrip("/")
    if path.endswith(".md"):
        return DOCS_DIR / path
    elif path.endswith((".yaml", ".json")):
        return SPECS_DIR / path
    return None


def file_hash(path: Path) -> str | None:
    """Return MD5 hash of existing file content, or None if missing."""
    if not path.exists():
        return None
    return hashlib.md5(path.read_bytes()).hexdigest()


def content_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


_RE_MD_LINK_URL = re.compile(r"\(https?://[^)]+\)")


def get_sitemap_urls(session: requests.Session) -> list[str]:
    """Fetch llms.txt and return all documented URLs.

    llms.txt uses Markdown link syntax: - [Title](URL): description
    """
    print(f"Fetching sitemap from {SITEMAP_URL} ...")
    raw = fetch_url(session, SITEMAP_URL)
    if not raw:
        print("ERROR: Could not fetch sitemap", file=sys.stderr)
        sys.exit(1)

    urls = []
    for match in _RE_MD_LINK_URL.finditer(raw):
        url = match.group(0)[1:-1]  # strip leading ( and trailing )
        urls.append(url)
    return urls


def write_manifest(results: list[dict], stats: dict) -> None:
    """Write MANIFEST.md with fetch timestamp and per-file status."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Documentation Manifest",
        "",
        f"Last updated: {now}",
        f"Source: {SITEMAP_URL}",
        "",
        (
            f"**Stats**: {stats['fetched']} fetched "
            f"({stats['new']} new, {stats['updated']} updated), "
            f"{stats['skipped']} unchanged, {stats['failed']} failed"
        ),
        "",
        "## Files",
        "",
        "| Status | File | Source URL |",
        "|--------|------|------------|",
    ]

    for r in sorted(results, key=lambda x: str(x["path"])):
        rel = r["path"].relative_to(REPO_ROOT)
        status = r["status"]
        lines.append(f"| {status} | `{rel}` | {r['url']} |")

    MANIFEST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Manifest written to {MANIFEST_PATH.relative_to(REPO_ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mirror Polymarket API documentation from official source."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and process but do not write files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-fetch and overwrite even if content is unchanged",
    )
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "poly-docs-mirror/1.0",
            "Accept": "text/plain, text/markdown, */*",
        }
    )

    all_urls = get_sitemap_urls(session)

    # Split into processable and unrecognised
    mapped = [(url, url_to_local_path(url)) for url in all_urls]
    processable = [(url, path) for url, path in mapped if path is not None]
    skipped_count = len(all_urls) - len(processable)

    md_count = sum(1 for _, p in processable if str(p).endswith(".md"))
    spec_count = len(processable) - md_count

    print(
        f"Found {len(processable)} files to sync "
        f"({md_count} docs, {spec_count} specs)"
        + (f", skipping {skipped_count} unrecognised URLs" if skipped_count else "")
    )
    if args.dry_run:
        print("DRY RUN — no files will be written")

    results = []
    stats = {"fetched": 0, "skipped": 0, "failed": 0, "new": 0, "updated": 0}

    for i, (url, local_path) in enumerate(processable, 1):
        rel = url.replace(BASE_URL, "")
        print(f"[{i:>3}/{len(processable)}] {rel}", end="", flush=True)

        time.sleep(REQUEST_DELAY)
        raw = fetch_url(session, url)

        if raw is None:
            print(" -> FAILED")
            stats["failed"] += 1
            results.append({"url": url, "path": local_path, "status": "failed"})
            continue

        processed = clean_mdx(raw) if str(local_path).endswith(".md") else raw

        new_hash = content_hash(processed)
        old_hash = file_hash(local_path)

        if old_hash == new_hash and not args.force:
            print(" -> unchanged")
            stats["skipped"] += 1
            results.append({"url": url, "path": local_path, "status": "unchanged"})
            continue

        is_new = old_hash is None

        if not args.dry_run:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_text(processed, encoding="utf-8")

        status = "new" if is_new else "updated"
        print(f" -> {status}")
        stats[status] += 1
        stats["fetched"] += 1
        results.append({"url": url, "path": local_path, "status": status})

    if not args.dry_run:
        write_manifest(results, stats)

    print(
        f"\nDone: {stats['fetched']} fetched "
        f"({stats['new']} new, {stats['updated']} updated), "
        f"{stats['skipped']} unchanged, {stats['failed']} failed"
    )

    if stats["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
