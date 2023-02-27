import vue from "@vitejs/plugin-vue";

export default {
    plugins: [vue()],
    build: {
        outDir: "noted/_static",
    },
};
