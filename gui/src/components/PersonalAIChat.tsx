import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { appConfig } from "@/lib/app-config";

const PersonalAIChat = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [heroBackground, setHeroBackground] = useState<string | null>(null);
  const [responseText, setResponseText] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [activeController, setActiveController] = useState<AbortController | null>(null);

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const prompt = message.trim();
    if (!prompt || isLoading) return;

    setIsLoading(true);
    setError(null);
    setResponseText("");
    setMessage("");

    if (activeController) {
      activeController.abort();
    }
    const controller = new AbortController();
    setActiveController(controller);

    try {
      const response = await fetch(chatEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
        signal: controller.signal,
      });

      if (!response.ok) {
        const fallbackMessage = `Request failed with status ${response.status}`;
        const errorBody = await response.text().catch(() => "");
        throw new Error(errorBody || fallbackMessage);
      }

      if (!response.body) {
        throw new Error("Response body is missing.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let pendingChunk = "";

      const appendToResponse = (chunk: string) => {
        if (!chunk) return;
        setResponseText((prev) => {
          if (!prev) return chunk;
          if (chunk === prev) return prev;
          if (chunk.startsWith(prev)) {
            return chunk;
          }
          return prev + chunk;
        });
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

      const processLine = (rawLine: string) => {
        const trimmed = rawLine.trim();
        if (!trimmed) return;

        if (trimmed === "[DONE]") {
          pendingChunk = "";
          return;
        }

        const withoutPrefix = trimmed.startsWith("data:") ? trimmed.slice(5).trim() : trimmed;
        if (!withoutPrefix) return;

        pendingChunk = pendingChunk ? `${pendingChunk}${withoutPrefix}` : withoutPrefix;

        try {
          const parsed = JSON.parse(pendingChunk);
          const chunk = extractTextFromPayload(parsed);
          appendToResponse(chunk);
          pendingChunk = "";
        } catch (err) {
          // Ignore parsing errors for partial chunks; they will resolve as more data arrives.
          if (!(err instanceof SyntaxError)) {
            console.error("Failed to parse chunk:", err);
            pendingChunk = "";
          }
        }
      };

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        if (!value) continue;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split(/\r?\n/);
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          processLine(line);
        }
      }

      if (buffer) {
        processLine(buffer);
      }

      if (pendingChunk) {
        try {
          const parsed = JSON.parse(pendingChunk);
          const chunk = extractTextFromPayload(parsed);
          appendToResponse(chunk);
        } catch {
          // Swallow parsing errors on trailing partial data.
        }
      }
    } catch (err) {
      if ((err as DOMException).name === "AbortError") {
        return;
      }
      console.error(err);
      setError(err instanceof Error ? err.message : "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
      setActiveController(null);
    }
  };

  return (
    <main className="min-h-screen relative overflow-hidden bg-paper">
      {/* Background Surface */}
      {shouldUseImage && heroBackground && (
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20"
          style={{ backgroundImage: `url(${heroBackground})` }}
        />
      )}
      {!shouldUseImage && <div className="absolute inset-0 bg-gradient-overlay" />}
      
      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-6">
        <div className="w-full max-w-2xl text-center space-y-8">
          {/* Typography Header */}
          <div className="space-y-2">
            <h1 className="text-6xl md:text-7xl font-cursive font-semibold text-ink tracking-wide">
              Ask The Bio
            </h1>
            <p className="text-3xl md:text-4xl font-cursive italic text-ink-light font-light">
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
          
          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center justify-center space-x-2 text-ink-light/60 mt-6">
              <div className="w-2 h-2 bg-ink rounded-full animate-pulse" />
              <div className="w-2 h-2 bg-ink rounded-full animate-pulse" style={{ animationDelay: '0.2s' }} />
              <div className="w-2 h-2 bg-ink rounded-full animate-pulse" style={{ animationDelay: '0.4s' }} />
              <span className="ml-3 text-sm font-serif">Thinking...</span>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="p-4 rounded-xl bg-destructive/10 border border-destructive/40 text-destructive text-left font-serif">
              {error}
            </div>
          )}

          {/* Response */}
          {responseText && !error && (
            <div className="p-6 rounded-3xl bg-paper/90 backdrop-blur-sm border border-border text-left shadow-paper">
              <p className="whitespace-pre-wrap text-base leading-relaxed text-ink font-sans">
                {responseText}
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
};

export default PersonalAIChat;
