import { useEffect, useRef, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

export function CornerInfoBadge() {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const handlePointerDown = (event: PointerEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    window.addEventListener("pointerdown", handlePointerDown);
    return () => window.removeEventListener("pointerdown", handlePointerDown);
  }, [isOpen]);

  return (
    <div className="fixed top-3 right-3 z-50 pointer-events-auto">
      <div
        ref={containerRef}
        className="relative inline-flex items-center justify-center"
      >
        <button
          type="button"
          aria-label="About this project"
          aria-expanded={isOpen}
          className={cn(
            "flex h-10 w-10 justify-center rounded-full text-3xl font-light transition-all duration-200 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black/30 dark:focus-visible:ring-white/40",
            isOpen
              ? "bg-black/80 text-white shadow-lg dark:bg-white/85 dark:text-black"
              : "bg-transparent text-black/70 hover:bg-black/80 hover:text-white hover:shadow-lg dark:text-white/80 dark:hover:bg-white/80 dark:hover:text-black"
          )}
          onClick={() => setIsOpen((prev) => !prev)}
        >
          ≡
        </button>

        <Bubble
          href="/privacy"
          open={isOpen}
          className="-translate-x-5 translate-y-20 rotate-[-50deg] min-w-[8.2rem]"
        >
          <span className="font-bold">privacy policy</span>&nbsp;↗
        </Bubble>

        <Bubble
          href="https://github.com/diegobit/askthebio"
          open={isOpen}
          className="-translate-x-11 translate-y-12 rotate-[-28deg] min-w-[8.2rem]"
        >
          <span className="font-bold">source code</span>&nbsp;↗
        </Bubble>
        
        <Bubble
          href="https://diegobit.com/post/ask-the-bio"
          open={isOpen}
          className="-translate-x-14 translate-y-3 rotate-[-8deg] min-w-[8.2rem]"
        >
          <span className="font-bold">blog post</span>&nbsp;↗
        </Bubble>

      </div>
    </div>
  );
}

type BubbleProps = {
  href: string;
  className?: string;
  children: ReactNode;
  open: boolean;
  external?: boolean;
};

function Bubble({ href, className = "", children, open, external = true }: BubbleProps) {
  const bubbleClasses = cn(
    "pointer-events-none absolute bottom-0 right-0 inline-flex min-w-[10.5rem] max-w-[18rem] items-center justify-center rounded-full bg-white/60 px-4 py-3 text-xs text-black/80 shadow-md backdrop-blur-sm opacity-0 scale-50 translate-x-0 translate-y-0 transition-all duration-300 ease-out hover:bg-white/80 focus-visible:bg-white/80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70 dark:bg-gray-800/60 dark:text-white/80 dark:hover:bg-gray-800/80 dark:focus-visible:ring-white/20",
    open && [
      "pointer-events-auto opacity-100 scale-100",
      className,
      "shadow-lg"
    ]
  );

  if (external) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        tabIndex={open ? 0 : -1}
        className={bubbleClasses}
      >
        {children}
      </a>
    );
  }

  return (
    <Link to={href} tabIndex={open ? 0 : -1} className={bubbleClasses}>
      {children}
    </Link>
  );
}
