<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import KeyboardJS from "keyboardjs";

import Container from "../Container.vue";

const checked = ref([]);

onMounted(() => {
    new Array(10).fill(null).forEach((_, i) => {
        KeyboardJS.bind(String(i), handleKeyboardShortcut);
    });
});

onBeforeUnmount(() => {
    new Array(10).fill(null).forEach((_, i) => {
        KeyboardJS.unbind(String(i), handleKeyboardShortcut);
    });
});

function handleKeyboardShortcut(e) {
    const key = Number(e.key) === 0 ? 10 : Number(e.key);
    return toggleOption(key - 1);
}

function toggleOption(id) {
    checked.value = id;
}
</script>

<template>
    <Container>
        <template #body="bodyProps">
            <span>{{ bodyProps.data.text }}</span>

            <div class="space-y-2 my-4">
                <div
                    @click="toggleOption(index)"
                    :class="{ 'bg-gray-100': checked === index }"
                    class="border border-gray-200 rounded px-2 py-1 relative select-none"
                    v-for="(choice, index) in bodyProps.data.options"
                >
                    <input type="radio" class="mr-2" :checked="checked === index" />

                    {{ choice.text }}

                    <!-- prettier-ignore -->
                    <div class="w-6 h-6 text-sm bg-white border border-gray-200 rounded p-1 flex items-center justify-center absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-1/2" >
                        {{ index + 1 }}
                    </div>
                </div>
            </div>
        </template>
    </Container>
</template>
