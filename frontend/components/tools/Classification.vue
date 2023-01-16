<script setup>
import Container from "../Container.vue";
</script>

<template>
    <Container>
        <template #header="headerProps">
            <div class="flex items-center justify-center h-full">
                <span class="uppercase font-bold text-white">{{ headerProps.data.label }}</span>
            </div>
        </template>

        <template #body="bodyProps">
            <span>{{ bodyProps.data.text }}</span>
        </template>
    </Container>
</template>
