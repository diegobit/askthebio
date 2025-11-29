export default {
  async fetch(req: Request, env: any): Promise<Response> {
    const { pathname } = new URL(req.url);
    if (req.method === "OPTIONS") return cors(new Response(null, { status: 204 }));
    if (pathname !== "/chat") return cors(new Response("Not found", { status: 404 }));
    if (req.method !== "POST") return cors(new Response("Use POST", { status: 405 }));

    // --- Load context from R2 ---
    const contextKey = env.CONTEXT_KEY ?? "diego-giorgini-y4tfirbg/latest/extraction.md";
    const obj = await env.R2.get(contextKey);
    const contextText = obj ? await obj.text() : "(no context found)";
    const envSnippetLength = Number(env.CONTEXT_SNIPPET_LENGTH);
    const contextSnippetLength = Number.isFinite(envSnippetLength) && envSnippetLength > 0 ? envSnippetLength : 500000;
    const contextSnippet = contextText.slice(0, contextSnippetLength);
    const personName = env.PERSON_NAME ?? "Diego Giorgini";
    const systemPrompt = [
      `You are the personal AI assistant of ${personName}. Your name is AskTheBio. You answer personal questions about ${personName}.`,
      "",
      `You talk like you know and care for ${personName}. You use an adult, but not corporate tone.`,
      "",
      `You have been given information about ${personName}, some of which are extracted from personal websites or socials. You never explicitly say you have been provided context information.`,
      "",
      "Context:",
      "<context>",
      contextSnippet,
      "</context>",
    ].join("\n");

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

    const h = new Headers();
    h.set("Content-Type", "text/event-stream; charset=utf-8");
    h.set("Cache-Control", "no-cache, no-transform");
    h.set("Connection", "keep-alive");
    ["content-length", "content-encoding", "transfer-encoding"].forEach(k => h.delete(k));
    return cors(new Response(upstream.body, { status: 200, headers: h }));
  },
};

function cors(res: Response) {
  const h = new Headers(res.headers);
  h.set("Access-Control-Allow-Origin", "*");
  h.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  h.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
  return new Response(res.body, { status: res.status, headers: h });
}
