<script setup>
import { ref, inject, onMounted, onBeforeUnmount } from "vue";
import KeyboardJS from "keyboardjs";

import Container from "../Container.vue";

const config = inject("app_config");

const selectedLabelIndex = ref(0);

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

    if (key - 1 === selectedLabelIndex.value) {
        return;
    }

    if (key > config.value.labels.length) {
        return;
    }

    return changeActiveLabelIndex(key - 1);
}

function changeActiveLabelIndex(idx) {
    selectedLabelIndex.value = idx;
}

function tokenize(text, spans) {
    const result = [];

    let offset = 0;
    let remaning = text;

    for (const span of spans) {
        const start = remaning.slice(0, span.start - offset);
        const _span = remaning.substring(span.start - offset, span.end - offset);

        remaning = remaning.slice(-1 * (remaning.length - start.length - _span.length));
        offset = offset + start.length + _span.length;

        result.push({ type: "span", text: start });
        result.push({ type: "annotation", text: _span, value: span });
    }

    if (remaning) {
        result.push({ type: "span", text: remaning });
    }

    return result;
}
</script>

<template>
    <Container>
        <template #header>
            <div class="px-5 flex items-center text-white h-full space-x-2">
                <button
                    v-for="(label, index) in config.labels"
                    class="label"
                    :class="{ label_active: index === selectedLabelIndex }"
                    @click="changeActiveLabelIndex(index)"
                >
                    {{ label }}
                    <span class="label_ks">{{ index + 1 }}</span>
                </button>
            </div>
        </template>

        <template #body="bodyProps">
            <template v-for="span in tokenize(bodyProps.data.text, bodyProps.data.spans)">
                <span v-if="span.type == 'span'">{{ span.text }}</span>
                <span v-if="span.type == 'annotation'" class="annotation">
                    {{ span.text }}
                    <span class="annotation_label">{{ span.value.label }}</span>
                </span>
            </template>
        </template>
    </Container>
</template>

<style scoped>
.label {
    @apply border border-white rounded px-2.5 font-medium;
}

.label_active {
    @apply border border-white bg-white text-black;
}

.label_ks {
    @apply text-xs font-light ml-1;
}

.label_ks {
    @apply text-xs font-light ml-1;
}

.annotation {
    @apply rounded-sm py-1 px-2 font-semibold;

    background-color: #fae291;
    cursor: pointer;

    -webkit-box-decoration-break: clone;
    box-decoration-break: clone;
}

.annotation:hover {
    opacity: 0.8;
}

.annotation_label {
    @apply text-xs font-bold pl-1;
}
</style>
