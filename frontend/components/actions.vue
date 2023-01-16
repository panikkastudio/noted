<script setup>
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { advanceCurrentTask } from '../base/fetchers'

const queryClient = useQueryClient()

const advanceTask = useMutation({
    mutationFn: advanceCurrentTask,
    onSuccess: () => {
        queryClient.invalidateQueries({
            queryKey: ['current_task']
        })
    },
})

function onAccept() {
    advanceTask.mutate({
        verdict: 'accept'
    })
}
</script>

<template>
    <div class="w-full max-w-3xl absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <button @click="onAccept">Accept</button>
        <button>Reject</button>
        <button>Ignore</button>
    </div>
</template>