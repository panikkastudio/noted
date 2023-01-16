<script setup>
import { provide } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { getAppConfig } from "./base/fetchers";

import Actions from "./components/Actions.vue";

import NerBinary from "./components/tools/NerBinary.vue";
import NerManual from "./components/tools/NerManual.vue";
import Classification from "./components/tools/Classification.vue";

const { data } = useQuery({ queryKey: ["app_config"], queryFn: getAppConfig });

provide("app_config", data);

function getComponent(view_type) {
    if (view_type === "classification") {
        return Classification;
    }

    if (view_type === "ner") {
        return NerBinary;
    }

    if (view_type === "ner_manual") {
        return NerManual;
    }
}
</script>

<template>
    <div class="h-screen w-screen bg-gray-100">
        <div v-if="data" class="pt-[80px] overflow-y-scroll">
            <component :is="getComponent(data.view_type)"></component>
        </div>

        <Actions />
    </div>
</template>

<style scoped>
.logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
}

.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
