import { defineStore } from "pinia";

export const useTokenStore = defineStore({
  // id is required so that Pinia can connect the store to the devtools
  id: "token",
  state: () => ({
    name: "Vue",
    csrfToken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
  }),
  getters: {},
  actions: {},
});
