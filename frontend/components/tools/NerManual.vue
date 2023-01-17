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

function getSelectedRegion(data) {
    const { anchorNode, focusNode, anchorOffset, focusOffset } = window.getSelection();

    if (anchorOffset === focusOffset && anchorNode.parentElement.id === focusNode.parentElement.id) {
        console.log("click event");
        return;
    }

    const range = [Number(anchorNode.parentElement.id), Number(focusNode.parentElement.id)].sort();

    const tokens = data.tokens.slice(range[0], range[1] + 1);

    console.log({ tokens });
}

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

function tokenize(text, tokens, spans) {
    const result = [];
    const punc = /[~`!@#$%^&*(){}\[\];:"'<,.>?\/\\|_+=-]/g;
    const hasSpaceToItsLeft = (charAt) => charAt !== 0 && text[charAt - 1] !== " ";

    let currentSpanIDX = 0;
    let currentSpan = spans[currentSpanIDX];
    let tokensWithinCurrentSpan = [];

    for (const token of tokens) {
        // TODO: Find the corresponting token in the text and add spaces 'IF' it has spaces in the
        //  text itself.
        // const type = token.text.match(punc) && token.text.length === 1 ? "punc" : "word";
        const type = hasSpaceToItsLeft(token.start) ? "punc" : "word";

        if (token.id >= currentSpan?.token_start && token.id < currentSpan?.token_end) {
            tokensWithinCurrentSpan.push({ type, value: token });
            continue;
        }

        if (token.id === currentSpan?.token_end) {
            result.push({ type: "mark", value: currentSpan, tokens: tokensWithinCurrentSpan });
            tokensWithinCurrentSpan = [];

            currentSpanIDX++;
            currentSpan = spans[currentSpanIDX];
        }

        result.push({ type, value: token });
    }

    console.log(tokensWithinCurrentSpan);
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
            <div class="w-full h-full body_container" @mouseup="getSelectedRegion(bodyProps.data)">
                <template v-for="token in tokenize(bodyProps.data.text, bodyProps.data.tokens, bodyProps.data.spans)">
                    <span v-if="token.type !== 'mark'" class="token" :id="token.value.id" :class="{ token_punc: token.type === 'punc' }">
                        {{ token.value.text }}
                    </span>

                    <mark v-if="token.type === 'mark'" class="annotation group">
                        <span
                            :id="_token.value.id"
                            v-for="_token in token.tokens"
                            class="token group-hover:line-through"
                            :class="{ token_punc: _token.type === 'punc' }"
                        >
                            {{ _token.value.text }}
                        </span>
                        <span class="annotation_label">
                            {{ token.value.label }}
                        </span>
                    </mark>
                </template>
            </div>
        </template>
    </Container>
</template>

<style scoped>
.body_container {
    word-wrap: pre-word;
    white-space: pre-wrap;
}
.token {
    margin: 0 2px;
    display: inline-block;
}

.token_punc {
    margin-left: -2px !important;
}

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
    color: #6f5604;
}
</style>
