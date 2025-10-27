import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { appConfig } from "@/lib/app-config";

const setMetaContent = (selector: string, content: string) => {
  const element = document.querySelector<HTMLMetaElement>(selector);
  if (element) {
    element.setAttribute("content", content);
  }
};

const applySystemTheme = (mq: MediaQueryList) => {
  document.documentElement.classList.toggle('dark', mq.matches);
};

document.title = appConfig.title;
setMetaContent('meta[name="description"]', appConfig.description);
setMetaContent('meta[property="og:title"]', appConfig.title);
setMetaContent('meta[property="og:description"]', appConfig.description);

const systemThemeQuery = window.matchMedia('(prefers-color-scheme: dark)');
applySystemTheme(systemThemeQuery);

const listener = (event: MediaQueryListEvent) => applySystemTheme(event);
if (typeof systemThemeQuery.addEventListener === 'function') {
  systemThemeQuery.addEventListener('change', listener);
} else {
  systemThemeQuery.addListener(listener); // Safari < 14
}

createRoot(document.getElementById("root")!).render(<App />);
