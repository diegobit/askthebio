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

document.title = appConfig.title;
setMetaContent('meta[name="description"]', appConfig.description);
setMetaContent('meta[property="og:title"]', appConfig.title);
setMetaContent('meta[property="og:description"]', appConfig.description);

createRoot(document.getElementById("root")!).render(<App />);
