<script setup>
import { useQuery } from '@tanstack/vue-query'
import { getCurrentTask } from '../base/fetchers';

const { isLoading, isError, data, error } = useQuery({
    queryKey: ['current_task'],
    queryFn: getCurrentTask,
})
</script>

<template>
    <div class="rounded bg-white shadow-sm w-full max-w-3xl mx-auto min-h-[250px]">
        <span v-if="data">{{ data.text }}</span>
    </div>
</template>