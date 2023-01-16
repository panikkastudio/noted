<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import KeyboardJS from "keyboardjs";
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import { advanceCurrentTask } from "../base/fetchers";

const ready = ref(false);
const queryClient = useQueryClient();

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
    advanceTask.mutate({
        verdict: "accept",
    });
}

function onReject() {
    advanceTask.mutate({
        verdict: "reject",
    });
}

function onIgnore() {
    advanceTask.mutate({
        verdict: "ignore",
    });
}
</script>

<template>
    <div class="w-full max-w-3xl absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <button @click="onAccept">Accept</button>
        <button>Reject</button>
        <button>Ignore</button>
    </div>
</template>
