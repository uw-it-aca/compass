import { defineStore } from "pinia";
import { getAffiliations } from "@/utils/data";

export const useAffiliationStore = defineStore({
  id: "affiliation",
  state: () => {
    return {
      getAffiliations,
      affiliations: {},
      affiliationsLoaded: false,
    };
  },
  getters: {
    fetchAffiliations(state) {
      if (!state.affiliationsLoaded) {
        state.affiliations = {
          request: this.getAffiliations().then((response) => {
            state.affiliations.data = response;
          }),
        };
      }
      return state.affiliations.request;
    },
  },
  actions: {},
});
