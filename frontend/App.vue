<script setup>
import Classification from './components/classification.vue';
import Actions from './components/actions.vue'
</script>

<template>
    <div class="h-screen w-screen bg-gray-100">
        <div class="pt-12">
            <Classification />
        </div>

        <Actions />
    </div>
</template>

<style scoped>
.logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
}

.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
