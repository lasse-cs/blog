import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
    publicDir: false,
    resolve: {
        alias: {
            "@": resolve(__dirname, "src/static_src/"),
        },
    },
    build: {
        outDir: resolve(__dirname, "src/static_built/"),
        rollupOptions: {
            input: {
                blog: resolve(__dirname, "src/static_src/js/blog.js"),
            },
            output: {
                entryFileNames: `js/[name].js`,
                chunkFileNames: `js/[name].js`,
                assetFileNames: `css/[name].css`,
                manualChunks: {
                    stimulus: ["@hotwired/stimulus"],
                    d3: ["d3"],
                },
            },
        },
    },
});