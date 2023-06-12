import {defineStore} from "pinia";
import dataMixin from "../mixins/data_mixin.js";

export const useAffiliationStore = defineStore({
  id: "affiliation",
  state: () => {
    return {
      affiliations: [],
      affiliationsLoaded: false,
    };
  },
  getters: {
    getAffiliations(state) {
      if(state.affiliationsLoaded) {
        return new Promise((resolve) => {
          resolve({"data": state.affiliations});
        });
      } else {
        dataMixin.methods.getAffiliations().then((response) => {
          state.affiliations = response.data;
          state.affiliationsLoaded = true;
        });
        return new Promise((resolve) => {
          resolve({"data": state.affiliations});
        });
      }
    },
  },
  actions: {},
});
