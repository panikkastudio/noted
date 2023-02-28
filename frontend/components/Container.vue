<script setup>
import { useSlots, watchEffect, provide, inject } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { getCurrentTask } from "../base/fetchers";
import { useCachedData } from "../store";

// Here we keep a reference to the
//  data so child components can mutate it.
// We will send this version of the data back to
//  server upon verdict.
const slots = useSlots();
const cachedData = useCachedData();

const { isLoading, isFetching, data, isError, error } = useQuery({
    queryKey: ["current_task"],
    queryFn: getCurrentTask,
});

const isBusy = isLoading || isFetching;

// Maintain the cached version of our data.
watchEffect(() => {
    if (data?.value && cachedData.data?._task_hash !== data?.value?._task_hash) {
        cachedData.updateData(data.value);
    }
});

function updateData(data) {
    cachedData.updateData(data);
}
</script>

<template>
    <div v-if="!isBusy && data && cachedData.data.value" class="container">
        <div v-if="slots.header" class="bg-black">
            <div class="h-14">
                <slot name="header" :data="cachedData.data.value" :update="updateData"></slot>
            </div>
        </div>

        <div class="p-5 text-lg leading-loose text-gray-800 overflow-y-scroll max-h-full">
            <slot name="body" :data="cachedData.data.value" :update="updateData"></slot>
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
