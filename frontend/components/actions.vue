<script setup>
import KeyboardJS from "keyboardjs";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useMutation, useQueryClient } from "@tanstack/vue-query";

import { useCachedData } from "../store";
import { advanceCurrentTask } from "../base/fetchers";

const ready = ref(false);
const queryClient = useQueryClient();
const cachedData = useCachedData();

const advanceTask = useMutation({
    mutationFn: advanceCurrentTask,
    onSuccess: () =>
        queryClient.invalidateQueries({
            queryKey: ["current_task"],
        }),
});

onMounted(() => {
    if (!ready.value) {
        ready.value = true;

        KeyboardJS.bind("a", onAccept);
        KeyboardJS.bind("x", onReject);
        KeyboardJS.bind("space", onIgnore);
    }
});

onBeforeUnmount(() => {
    KeyboardJS.unbind("a", onAccept);
    KeyboardJS.unbind("x", onReject);
    KeyboardJS.unbind("space", onIgnore);
});

function onAccept() {
    if (!advanceTask.isLoading.value) {
        console.log(Object.assign({}, cachedData.data.value));

        advanceTask.mutate({
            _verdict: "accept",
            ...Object.assign({}, cachedData.data.value),
        });
    }
}

function onReject() {
    if (!advanceTask.isLoading.value) {
        advanceTask.mutate({
            _verdict: "reject",
        });
    }
}

function onIgnore() {
    if (!advanceTask.isLoading.value) {
        advanceTask.mutate({
            _verdict: "ignore",
        });
    }
}
</script>

<template>
    <div class="w-full max-w-3xl absolute bottom-4 left-1/2 transform -translate-x-1/2 space-x-2">
        <button @click="onAccept" class="text-gray-900 font-bold">Accept</button>
        <button @click="onReject" class="text-red-600 font-bold">Reject</button>
        <button @click="onIgnore" class="text-gray-600">Ignore</button>
    </div>
</template>
