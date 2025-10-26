/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BACKGROUND_MODE?: "gradient" | "image";
  readonly VITE_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
