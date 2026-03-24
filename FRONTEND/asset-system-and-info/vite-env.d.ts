// src/vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_PROTOCOL: string;
    readonly VITE_API_HOST: string;
    readonly VITE_API_PORT: string;
    readonly VITE_API_VERSION: string;
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }