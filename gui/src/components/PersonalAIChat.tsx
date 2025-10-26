import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";
import heroBackground from "@/assets/hero-background.jpg";

const PersonalAIChat = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    setIsLoading(true);
    // TODO: Implement AI chat functionality
    console.log("Sending message:", message);
    
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      setMessage("");
    }, 1000);
  };

  return (
    <main className="min-h-screen relative overflow-hidden bg-paper">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20"
        style={{ backgroundImage: `url(${heroBackground})` }}
      />
      
      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-overlay" />
      
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
              Diego Giorgini
            </h2>
          </div>
          
          {/* Chat Input */}
          <form onSubmit={handleSubmit} className="relative">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask me anything about Diego."
              className="w-full h-16 text-xl bg-paper/90 backdrop-blur-sm border-2 rounded-inf px-6 text-ink placeholder:text-ink-light/70 shadow-ink  transition-all duration-300 font-serif"
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
        </div>
      </div>
    </main>
  );
};

export default PersonalAIChat;
