import { createApp } from "vue";
import App from "./app.vue";
import router from "./router";
import store from "./store";

import VueGtag from "vue-gtag";
import { Vue3Mq, MqResponsive } from "vue3-mq";

// bootstrap js
import "bootstrap";

// custom bootstrap theming
import "./css/custom.scss";

const app = createApp(App);

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute("data-google-analytics");
const debugMode = document.body.getAttribute("data-django-debug");

app.config.productionTip = false;

// vue-router
app.use(router);

// vue-gtag (w/ vue-router auto-tracking)
app.use(
  VueGtag,
  {
    isEnabled: debugMode == "false",
    property: {
      id: gaCode,
      params: {
        anonymize_ip: true,
      },
    },
  },
  router
);

// vue-mq (media queries)
app.use(Vue3Mq, {
  preset: "bootstrap5",
});
app.component("mq-responsive", MqResponsive);

// vuex state management
app.use(store);

app.mount("#app");
