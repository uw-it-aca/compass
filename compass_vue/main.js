import { createApp } from "vue";
import { createPinia } from "pinia";
import VueGtag from "vue-gtag-next";
import { Vue3Mq } from "vue3-mq";

import App from "@/app.vue";
import router from "@/router";

// bootstrap js + bootstrap-icons
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";

// solstice bootstrap theme
import "solstice-theme/dist/solstice.scss";

// solstice-vue comps
import "solstice-vue/dist/style.css";

// bootstrap-vue-next css
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";

const app = createApp(App);
app.config.productionTip = false;

// vue-gtag-next
const gaCode = document.body.getAttribute("data-google-analytics");
const debugMode = document.body.getAttribute("data-django-debug");

app.use(VueGtag, {
  isEnabled: debugMode == "false",
  property: {
    id: gaCode,
    params: {
      anonymize_ip: true,
      // user_id: 'provideSomeHashedId'
    },
  },
});

// vue-mq (media queries)
app.use(Vue3Mq, {
  preset: "bootstrap5",
});

// pinia (vuex) state management
const pinia = createPinia();
app.use(pinia);

// vue-router
app.use(router);

app.mount("#app");
