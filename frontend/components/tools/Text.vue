<script setup>
import Container from "../Container.vue";
</script>

<template>
    <Container>
        <template #body="bodyProps">
            <span>{{ bodyProps.data.text }}</span>
        </template>
    </Container>
</template>
