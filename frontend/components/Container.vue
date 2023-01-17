<script setup>
import { useSlots } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { getCurrentTask } from "../base/fetchers";

const slots = useSlots();

const { isLoading, isFetching, data, isError, error } = useQuery({
    queryKey: ["current_task"],
    queryFn: getCurrentTask,
});

const isBusy = isLoading || isFetching;
</script>

<template>
    <div v-if="!isBusy && data" class="container">
        <div v-if="slots.header" class="bg-black">
            <div class="h-14">
                <slot name="header" :data="data"></slot>
            </div>
        </div>

        <div class="p-5 text-lg leading-loose text-gray-800 overflow-y-scroll max-h-full">
            <slot name="body" :data="data"></slot>
        </div>

        <div v-if="data.meta" class="absolute right-0 bottom-0 text-gray-500 bg-gray-50 px-2 rounded space-x-2">
            <span v-for="metaKey in Object.keys(data.meta)" class="text-xs space-x-1">
                <span class="font-semibold uppercase">{{ metaKey }}:</span>
                <span>{{ data.meta[metaKey] }}</span>
            </span>
        </div>
    </div>

    <div v-if="isBusy" class="loader_container">Loading</div>
</template>

<style scoped>
.container {
    @apply relative flex flex-col rounded overflow-hidden bg-white shadow-sm w-full max-w-3xl mx-auto min-h-[250px] max-h-[calc(100vh_-_160px)];
}

.loader_container {
    @apply bg-white rounded w-full max-w-3xl mx-auto min-h-[250px] flex items-center justify-center text-lg uppercase;
}
</style>
