import { useEffect, useRef, useState } from "react";
import type { Components } from "react-markdown";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Input } from "@/components/ui/input";
import { appConfig } from "@/lib/app-config";

const markdownComponents: Components = {
  p: ({ children }) => <p className="mb-4 last:mb-0">{children}</p>,
  ul: ({ children }) => <ul className="mb-4 list-disc space-y-2 pl-6">{children}</ul>,
  ol: ({ children }) => <ol className="mb-4 list-decimal space-y-2 pl-6">{children}</ol>,
  li: ({ children }) => <li className="text-base leading-relaxed text-ink">{children}</li>,
  code: ({ inline, children }) =>
    inline ? (
      <code className="rounded bg-ink/10 px-1.5 py-0.5 text-sm font-mono text-ink">
        {children}
      </code>
    ) : (
      <code className="text-sm font-mono text-ink">{children}</code>
    ),
  pre: ({ children }) => (
    <pre className="mb-4 overflow-x-auto rounded-2xl bg-ink/5 p-4 text-sm font-mono text-ink">
      {children}
    </pre>
  ),
  blockquote: ({ children }) => (
    <blockquote className="mb-4 border-l-4 border-ink/40 pl-4 italic text-ink/80">
      {children}
    </blockquote>
  ),
  a: ({ children, ...props }) => (
    <a
      className="text-primary underline underline-offset-2"
      target="_blank"
      rel="noopener noreferrer"
      {...props}
    >
      {children}
    </a>
  ),
  strong: ({ children }) => <strong className="font-semibold text-ink">{children}</strong>,
  em: ({ children }) => <em className="italic text-ink">{children}</em>,
};

const PersonalAIChat = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [heroBackground, setHeroBackground] = useState<string | null>(null);
  const [responseText, setResponseText] = useState("");
  const [error, setError] = useState<string | null>(null);
  const controllerRef = useRef<AbortController | null>(null);

  const backgroundMode = (import.meta.env.VITE_BACKGROUND_MODE ?? "gradient") as string;
  const shouldUseImage = backgroundMode.toLowerCase() === "image";
  const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8787").replace(/\/+$/, "");
  const chatEndpoint = `${apiBaseUrl}/chat`;

  useEffect(() => {
    if (!shouldUseImage) {
      setHeroBackground(null);
      return;
    }

    let isActive = true;

    import("@/assets/bg.png")
      .then((module) => {
        if (isActive) {
          setHeroBackground(module.default);
        }
      })
      .catch(() => {
        if (isActive) {
          setHeroBackground(null);
        }
      });

    return () => {
      isActive = false;
    };
  }, [shouldUseImage]);

  useEffect(() => {
    return () => {
      controllerRef.current?.abort();
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const prompt = message.trim();
    if (!prompt || isLoading) return;

    setIsLoading(true);
    setError(null);
    setResponseText("");
    setMessage("");

    if (controllerRef.current) {
      controllerRef.current.abort();
    }
    const controller = new AbortController();
    controllerRef.current = controller;

    let reader: ReadableStreamDefaultReader<Uint8Array> | null = null;

    try {
      const response = await fetch(chatEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "text/event-stream",
        },
        body: JSON.stringify({ prompt }),
        signal: controller.signal,
        cache: "no-store",
      });

      if (!response.ok) {
        const fallbackMessage = `Request failed with status ${response.status}`;
        const errorBody = await response.text().catch(() => "");
        throw new Error(errorBody || fallbackMessage);
      }

      if (!response.body) {
        throw new Error("Response body is missing.");
      }

      reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffered = "";
      let pendingPayload = "";
      let liveText = "";
      let shouldTerminate = false;

      const emitText = (text: string) => {
        if (!text) return;

        let nextText = text;

        if (!liveText) {
          nextText = text;
        } else if (text.startsWith(liveText)) {
          nextText = text;
        } else if (liveText.includes(text)) {
          nextText = liveText;
        } else {
          let overlap = 0;
          const maxOverlap = Math.min(liveText.length, text.length);
          for (let i = maxOverlap; i > 0; i--) {
            if (text.startsWith(liveText.slice(-i))) {
              overlap = i;
              break;
            }
          }
          nextText = `${liveText}${text.slice(overlap)}`;
        }

        if (nextText === liveText) {
          return;
        }

        liveText = nextText;
        setResponseText(nextText);
      };

      const extractTextFromPayload = (payload: unknown): string => {
        if (!payload) return "";

        if (typeof payload === "string") {
          return payload;
        }

        if (Array.isArray(payload)) {
          return payload.map(extractTextFromPayload).join("");
        }

        if (typeof payload === "object") {
          const record = payload as Record<string, unknown>;

          if (typeof record.text === "string") {
            return record.text;
          }

          if (Array.isArray(record.parts)) {
            return record.parts.map(extractTextFromPayload).join("");
          }

          if (record.content) {
            return extractTextFromPayload(record.content);
          }

          if (Array.isArray(record.candidates)) {
            return record.candidates.map(extractTextFromPayload).join("");
          }

          if (record.delta) {
            return extractTextFromPayload(record.delta);
          }
        }

        return "";
      };

      const parseAndEmit = (rawPayload: string): boolean => {
        let payload = pendingPayload ? pendingPayload + rawPayload : rawPayload;
        pendingPayload = "";

        try {
          const parsed = JSON.parse(payload);
          emitText(extractTextFromPayload(parsed));
          return true;
        } catch (_) {
          // fall through to incremental parsing
        }

        if (payload.includes("\n")) {
          let parsedAny = false;
          for (const line of payload.split(/\r?\n/)) {
            const trimmed = line.trim();
            if (!trimmed) continue;
            try {
              const parsed = JSON.parse(trimmed);
              emitText(extractTextFromPayload(parsed));
              parsedAny = true;
            } catch {
              pendingPayload += trimmed;
            }
          }
          return parsedAny;
        }

        pendingPayload = payload;
        return false;
      };

      const processEvent = (event: string): boolean => {
        let sawDone = false;

        for (const rawLine of event.split(/\r?\n/)) {
          if (!rawLine) continue;
          const line = rawLine.trim();
          if (!line || line.startsWith(":")) continue;
          if (!line.startsWith("data:")) continue;

          const value = rawLine.slice(rawLine.indexOf("data:") + 5).trim();
          if (!value) continue;

          if (value === "[DONE]") {
            sawDone = true;
            continue;
          }

          parseAndEmit(value);
        }

        if (sawDone) {
          shouldTerminate = true;
          return true;
        }

        return false;
      };

      while (!shouldTerminate && reader) {
        const { value, done } = await reader.read();
        if (done) {
          break;
        }

        if (value) {
          buffered += decoder.decode(value, { stream: true });
        }

        const events = buffered.split(/\r?\n\r?\n/);
        buffered = events.pop() ?? "";

        for (const event of events) {
          if (processEvent(event)) {
            break;
          }
        }
      }

      if (reader) {
        buffered += decoder.decode();
      }

      if (!shouldTerminate && buffered) {
        const trailingEvents = buffered.split(/\r?\n\r?\n/);
        buffered = trailingEvents.pop() ?? "";

        for (const event of trailingEvents) {
          if (processEvent(event)) {
            break;
          }
        }
      }

      if (!shouldTerminate) {
        const leftover = (pendingPayload || buffered).trim();
        if (leftover) {
          parseAndEmit(leftover);
        }
      }

      if (shouldTerminate && reader) {
        await reader.cancel().catch(() => undefined);
      }
    } catch (err) {
      if (reader) {
        await reader.cancel().catch(() => undefined);
      }
      if ((err as DOMException).name === "AbortError") {
        return;
      }
      console.error(err);
      setError(err instanceof Error ? err.message : "An unexpected error occurred.");
    } finally {
      if (reader) {
        try {
          reader.releaseLock();
        } catch {
          // Ignore release errors.
        }
        reader = null;
      }
      controllerRef.current = null;
      setIsLoading(false);
    }
  };
  return (
    <main className="min-h-screen relative overflow-hidden bg-paper">
      {/* Background Surface */}
      {shouldUseImage && heroBackground && (
        <div
          className="pointer-events-none fixed inset-0 bg-cover bg-center bg-no-repeat opacity-20"
          style={{ backgroundImage: `url(${heroBackground})` }}
        />
      )}
      {!shouldUseImage && <div className="pointer-events-none fixed inset-0 bg-gradient-overlay" />}
      
      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-6 pt-8 pb-12">
        <div className="w-full max-w-2xl text-center space-y-8 pb-8">
          {/* Typography Header */}
          <div className="space-y-2">
            <h1 className="text-6xl md:text-7xl font-cursive font-semibold text-ink tracking-wide">
              Ask The Bio
            </h1>
            <p className="text-3xl md:text-4xl font-cursive italic text-ink-light/60 font-light">
              of
            </p>
            <h2 className="text-5xl md:text-6xl font-cursive font-medium text-ink tracking-wide">
              {appConfig.personaName}
            </h2>
          </div>

          {/* Chat Input */}
          <form onSubmit={handleSubmit} className="relative">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={`Ask me anything about ${appConfig.personaFirstName}.`}
              className="w-full h-16 text-base md:text-base bg-paper/90 backdrop-blur-sm rounded-inf px-6 text-ink placeholder:text-ink-light/70 shadow-ink transition-[transform,_box-shadow] duration-300 font-sans border-0 focus:border-0 focus-visible:border-none focus:shadow-ink-lift focus-visible:shadow-ink-lift focus:scale-[1.03] focus-visible:scale-[1.03] focus-visible:outline-none focus-visible:!ring-0 focus-visible:!ring-transparent focus-visible:!ring-offset-0 focus-visible:!ring-offset-transparent focus:!ring-0 focus:!ring-transparent focus:!ring-offset-0 focus:!ring-offset-transparent"
              disabled={isLoading}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
          </form>
          
          {/* Error State */}
          {error && (
            <div className="p-4 rounded-xl bg-destructive/10 border border-destructive/40 text-destructive text-left font-serif">
              {error}
            </div>
          )}

          {/* Response */}
          {responseText && !error && (
            <div className="p-6 rounded-3xl bg-paper/90 backdrop-blur-sm border border-border text-left shadow-paper">
              <div className="space-y-4 text-base leading-relaxed text-ink font-sans">
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents} skipHtml>
                  {responseText}
                </ReactMarkdown>
              </div>
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center justify-center space-x-2 text-ink-light/60 mt-6">
              <div className="w-2 h-2 bg-ink rounded-full animate-pulse" />
              <div className="w-2 h-2 bg-ink rounded-full animate-pulse" style={{ animationDelay: '0.2s' }} />
              <div className="w-2 h-2 bg-ink rounded-full animate-pulse" style={{ animationDelay: '0.4s' }} />
              {/* <span className="ml-3 text-sm font-sans">Thinking...</span> */}
            </div>
          )}

        </div>
      </div>
    </main>
  );
};

export default PersonalAIChat;
