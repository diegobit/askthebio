import { buildSystemPrompt } from "./prompt";

const LOG_TTL_SECONDS = 60 * 60 * 24 * 90; // ~90 days
const LOG_ENABLE_FLAG = "true";

export default {
  async fetch(req: Request, env: any, ctx: ExecutionContext): Promise<Response> {
    const { pathname } = new URL(req.url);
    if (req.method === "OPTIONS") return cors(new Response(null, { status: 204 }));
    if (pathname !== "/chat") return cors(new Response("Not found", { status: 404 }));
    if (req.method !== "POST") return cors(new Response("Use POST", { status: 405 }));

    // --- Rate limit (IP-based) ---
    const rateLimiters = [
      env?.IP_LIMITER_BURST,
      env?.IP_LIMITER_MINUTE,
      env?.IP_LIMITER, // backward compatibility if only one limiter is configured
    ].filter((l: any) => l?.limit);

    if (rateLimiters.length > 0) {
      const ip = req.headers.get("CF-Connecting-IP") ?? "unknown";
      for (const limiter of rateLimiters) {
        const result = await limiter.limit({ key: ip });
        if (!result.success) {
          const resetMs = Number(result.reset);
          const retryAfterSeconds = Number.isFinite(resetMs)
            ? Math.max(1, Math.ceil((resetMs - Date.now()) / 1000))
            : 60;
          const h = new Headers({ "Content-Type": "application/json" });
          if (Number.isFinite(retryAfterSeconds)) h.set("Retry-After", String(retryAfterSeconds));
          return cors(new Response(JSON.stringify({ error: "rate_limited", retry_after_seconds: retryAfterSeconds }), { status: 429, headers: h }));
        }
      }
    }

    // --- Load context from R2 ---
    const contextKey = env.CONTEXT_KEY ?? "diego-giorgini-y4tfirbg/latest/extraction.md";
    const obj = await env.R2.get(contextKey);
    const contextText = obj ? await obj.text() : "(no context found)";
    const contextVersion = obj?.version ?? obj?.etag ?? null;
    const envSnippetLength = Number(env.CONTEXT_SNIPPET_LENGTH);
    const contextSnippetLength = Number.isFinite(envSnippetLength) && envSnippetLength > 0 ? envSnippetLength : 500000;
    const contextSnippet = contextText.slice(0, contextSnippetLength);
    const personName = env.PERSON_NAME ?? "Diego Giorgini";
    const systemPrompt = buildSystemPrompt(personName, contextSnippet);

    // --- Read user input ---
    let body: any = {};
    try { body = await req.json(); } catch {}
    const prompt = body.prompt ?? "";
    const envMaxTokens = Number(env.MAX_OUTPUT_TOKENS);
    const defaultMaxTokens = Number.isFinite(envMaxTokens) && envMaxTokens > 0 ? envMaxTokens : 4096;
    const requestedMaxTokens = Number(body.max_tokens);
    const maxOutputTokens = Number.isFinite(requestedMaxTokens) && requestedMaxTokens > 0
      ? requestedMaxTokens
      : defaultMaxTokens;

    // --- Call Gemini (stream) ---
    const model = env.GEMINI_MODEL ?? env.MODEL ?? "gemini-2.5-flash";
    const url = new URL(`https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent`);
    url.searchParams.set("key", env.GOOGLE_API_KEY);
    url.searchParams.set("alt", "sse");

    const upstream = await fetch(url.toString(), {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "accept": "text/event-stream",
      },
      body: JSON.stringify({
        systemInstruction: { role: "system", parts: [{ text: systemPrompt }] },
        contents: [{ role: "user", parts: [{ text: prompt }]}],
        generationConfig: {
          temperature: body.temperature ?? 0.7,
          maxOutputTokens
        }
      }),
      signal: req.signal,
    });

    if (!upstream.ok || !upstream.body) {
      const errTxt = await upstream.text().catch(() => "");
      return cors(new Response(`Upstream error ${upstream.status}: ${errTxt}`, { status: 502 }));
    }

    const upstreamBody = upstream.body as ReadableStream<Uint8Array>;

    // --- Log input/output to KV (best-effort) ---
    const shouldLog = String(env.LOG_GEMINI_IO ?? "").toLowerCase() === LOG_ENABLE_FLAG && !!env.LOGS_KV;
    let responseStream: ReadableStream = upstreamBody;

    if (shouldLog) {
      const kv = env.LOGS_KV as KVNamespace;
      const [clientStream, logStream] = upstreamBody.tee();
      responseStream = clientStream;
      const logPromise = collectAssistantText(logStream)
        .then((assistantText) => logGeminiIo(kv, {
          userText: prompt,
          assistantText,
          model,
          contextVersion,
        }))
        .catch(() => {});
      ctx?.waitUntil?.(logPromise);
    }

    const h = new Headers();
    h.set("Content-Type", "text/event-stream; charset=utf-8");
    h.set("Cache-Control", "no-cache, no-transform");
    h.set("Connection", "keep-alive");
    ["content-length", "content-encoding", "transfer-encoding"].forEach(k => h.delete(k));
    return cors(new Response(responseStream, { status: 200, headers: h }));
  },
};

function cors(res: Response) {
  const h = new Headers(res.headers);
  h.set("Access-Control-Allow-Origin", "*");
  h.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  h.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
  return new Response(res.body, { status: res.status, headers: h });
}

async function collectAssistantText(stream: ReadableStream<Uint8Array>): Promise<string> {
  let buffer = "";
  let assistantText = "";
  const reader = stream
    .pipeThrough(new TextDecoderStream())
    .getReader();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    if (value) buffer += value;

    let splitIndex = buffer.indexOf("\n\n");
    while (splitIndex !== -1) {
      const eventChunk = buffer.slice(0, splitIndex);
      buffer = buffer.slice(splitIndex + 2);
      assistantText += extractTextFromEvent(eventChunk);
      splitIndex = buffer.indexOf("\n\n");
    }
  }

  if (buffer.trim()) assistantText += extractTextFromEvent(buffer);
  return assistantText;
}

function extractTextFromEvent(eventChunk: string): string {
  let collected = "";
  const dataLines = eventChunk
    .split("\n")
    .map(line => line.trim())
    .filter(line => line.startsWith("data:"))
    .map(line => line.slice(5).trim())
    .filter(Boolean);

  for (const data of dataLines) {
    if (data === "[DONE]") continue;
    try {
      const parsed = JSON.parse(data);
      const parts = parsed?.candidates?.[0]?.content?.parts;
      if (Array.isArray(parts)) {
        for (const part of parts) {
          const text = part?.text;
          if (typeof text === "string") collected += text;
        }
      }
    } catch {
      // ignore malformed JSON chunks
    }
  }

  return collected;
}

async function logGeminiIo(kv: KVNamespace, data: { userText: string; assistantText: string; model: string; contextVersion: string | null }) {
  const key = buildLogKey();
  const payload = {
    timestamp: new Date().toISOString(),
    userText: data.userText ?? "",
    assistantText: data.assistantText ?? "",
    model: data.model ?? "",
    contextVersion: data.contextVersion ?? undefined,
  };

  try {
    await kv.put(key, JSON.stringify(payload), { expirationTtl: LOG_TTL_SECONDS });
  } catch {
    // best-effort: ignore logging failures
  }
}

function buildLogKey(): string {
  const now = new Date();
  const yyyy = now.getUTCFullYear();
  const mm = String(now.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(now.getUTCDate()).padStart(2, "0");
  const hh = String(now.getUTCHours()).padStart(2, "0");
  const min = String(now.getUTCMinutes()).padStart(2, "0");
  const ss = String(now.getUTCSeconds()).padStart(2, "0");
  const uuid = crypto.randomUUID();
  return `gemini:${yyyy}${mm}${dd}T${hh}${min}${ss}:${uuid}`;
}
