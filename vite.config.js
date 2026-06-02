import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
    root: resolve(__dirname, "src/static_src/"),
    publicDir: false,
    resolve: {
        alias: {
            "@": resolve(__dirname, "src/static_src/"),
        },
    },
    server: {
        cors: {
            origin: "http://localhost:8000",
        },
    },
    build: {
        manifest: true,
        outDir: resolve(__dirname, "src/static_built/"),
        rolldownOptions: {
            input: {
                blog: resolve(__dirname, "src/static_src/js/blog.ts"),
            },
            output: {
                entryFileNames: `js/[name].js`,
                chunkFileNames: `js/[name].js`,
                assetFileNames: `css/[name].css`,
                codeSplitting: {
                    groups: [
                        {
                            name: "stimulus",
                            test: /node_modules[\\/]@hotwired[\\/]stimulus/,
                        },
                        {
                            name: "d3",
                            test: /node_modules[\\/]d3(?:[\\/]|-|$)/,
                        },
                    ],
                },
            },
        },
    },
});
