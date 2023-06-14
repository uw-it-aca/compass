import {defineStore} from "pinia";
import dataMixin from "../mixins/data_mixin.js";

export const useAffiliationStore = defineStore({
  id: "affiliation",
  state: () => {
    return {
      affiliations: {},
      affiliationsLoaded: false,
    };
  },
  getters: {
    getAffiliations(state) {
      if (!state.affiliationsLoaded) {
        state.affiliations = {
          request: dataMixin.methods.getAffiliations().then((response) => {
            state.affiliations.data = response.data;
          }),
        };
      }
      return state.affiliations.request;
    },
  },
  actions: {},
});
