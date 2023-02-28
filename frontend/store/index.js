import { ref } from "vue";

const cachedData = ref();

export function useCachedData() {
    return {
        data: cachedData,
        updateData: (data) => {
            cachedData.value = data;
        },
    };
}
