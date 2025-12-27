import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
    publicDir: false,
    resolve: {
        alias: {
            "@": resolve(__dirname, "src/static_src/js"),
        },
    },
    build: {
        outDir: resolve(__dirname, "src/blog/static/js"),
        rollupOptions: {
            input: {
                activity: resolve(__dirname, "src/static_src/js/activity.js"),
                blog: resolve(__dirname, "src/static_src/js/blog.js"),
            },
            output: {
                entryFileNames: `[name].js`,
                chunkFileNames: `[name].js`,
                manualChunks: {
                },
            },
        },
    },
});