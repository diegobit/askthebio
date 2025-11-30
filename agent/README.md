# askthebio / agent

Cloudflare Worker that exposes a `/chat` endpoint backed by Gemini. It reads a pre-generated `extraction.md` from R2, streams responses (SSE), rate-limits by IP, and optionally logs Gemini I/O to KV.

## Quick start
- Requirements: Node 20+, `pnpm`, Cloudflare Wrangler (`npm i -g wrangler`), R2 + KV access.
- Install deps: `pnpm install`
- Cloudflare auth: `wrangler login` (once).
- Configure `wrangler.toml` (see below) and set the Gemini API key: `wrangler secret put GOOGLE_API_KEY`.
- Run locally: `pnpm dev`. Deploy: `pnpm deploy`.

## API
- POST `/chat` with JSON `{ "prompt": "...", "max_tokens": 2048?, "temperature": 0.7? }`.
- Response is `text/event-stream` with Gemini tokens; includes the R2 context snippet in the system prompt.

## Upload extraction.md to R2
- Use `rclone` (or any R2-capable client) to copy the markdown to your bucket:
  ```bash
  rclone copy /path/to/crawl/out/* rclone_config_name:r2_bucket_name/path/to/dir/
  ```
- You can also drop the resulting `.md` anywhere on R2 as long as the worker can read it.

## Configure wrangler.toml
- Create two R2 buckets and set `bucket_name` and `preview_bucket_name`.
- Set `CONTEXT_KEY` to the R2 path of the uploaded `extraction.md`.
- Adjust `PERSON_NAME`, `GEMINI_MODEL`, `CONTEXT_SNIPPET_LENGTH`, `MAX_OUTPUT_TOKENS`, and rate-limit/KV bindings as needed.

