import { createApp } from "vue";
import { VueQueryPlugin } from "@tanstack/vue-query";

import "./style.css";

import App from "./app.vue";

const app = createApp(App);

app.use(VueQueryPlugin);

app.mount("#app");
