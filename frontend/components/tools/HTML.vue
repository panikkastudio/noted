<script setup>
import { inject } from "vue";
import Container from "../Container.vue";

const config = inject("app_config");

const theme = {
    largeText: "22",
};

function _component(data) {
    return {
        template: config.value.html_template,
        data() {
            return {
                ...data,
                theme,
            };
        },
    };
}
</script>

<template>
    <Container>
        <template #body="bodyProps">
            <component :is="_component(bodyProps.data)"></component>
        </template>
    </Container>
</template>
