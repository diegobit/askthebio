# askthebio / crawl

Crawler that spins up multiple Chrome sessions and uses `browser-use` agents to gather structured profile data about a person from GitHub/code hosts, LinkedIn, X, Hugging Face, and generic websites. Results are saved as JSON and Markdown for downstream use.

## Quick start

- Requirements: Python 3.12+, Google Chrome (macOS path `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`), and a Chrome profile that is already signed in to the sites you want to crawl.
- Export env vars in your shell:
  ```bash
  export MODEL=gemini-...
  export GOOGLE_API_KEY=sk-...
  ```
- Configure the person to crawl in `main.py` by editing the `UserInput` block (name, links, texts/docs if you add them).
- Run with `uv`:
  ```bash
  uv run main.py
  ```

## What it does
- Copies your Chrome profile into per-port temp directories, launches multiple remote-debugging Chrome instances, and pools them for parallel crawling (`src/crawl.py`).
- Picks site-specific agent customizations under `src/customizations/` (GitHub, Hugging Face, LinkedIn, X, generic websites) to drive the browser and extract structured data models defined there.
- Writes aggregated outputs to `out/<slugified-name>.json` and `out/<slugified-name>.md`; per-site artifacts (and optional conversation logs when `verbose=True`) land in `out/<site>/`.

## Auth / sessions
- The crawler reuses your local Chrome profile (`~/Library/Application Support/Google/Chrome/<profile>`). Make sure you are logged into the target sites in that profile before running.

## Notes and tweaks
- Adjust concurrency or verbosity via `crawl_user(..., concurrency=5, verbose=True)` in `main.py`.
- Chrome path and profile directory are currently macOS defaults; change them in `src/crawl.py` if your setup differs.
- To add new site behavior, create a new customization class (see `src/customizations/base_customization.py` for the interface) and extend the domain routing logic in `src/crawl.py`.
