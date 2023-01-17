<script setup>
import Container from "../Container.vue";

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
        <template #body="bodyProps">
            <template v-for="span in tokenize(bodyProps.data.text, bodyProps.data.spans)">
                <span v-if="span.type == 'span'">{{ span.text }}</span>
                <mark v-if="span.type == 'annotation'" class="annotation group">
                    <span class="group-hover:line-through">{{ span.text }}</span>
                    <span class="annotation_label">{{ span.value.label }}</span>
                </mark>
            </template>
        </template>
    </Container>
</template>

<style scoped>
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
