import { defineStore } from "pinia";
import {
  getActiveICVisits,
} from "@/utils/data";

export const useICVisitsStore = defineStore("icVisits", {
  state: () => {
    return {

      _activeICVisits: {},

    };
  },
  getters: {
    activeICVisits(state) {
      if (
        !Object.prototype.hasOwnProperty.call(this._activeICVisits, "request")
      ) {
        this._activeICVisits.request = getActiveICVisits().then(
          (response) => {
            this._activeICVisits.data = response;
          }
        );
      }
      return this._activeICVisits.data;
    },
  },
  actions: {},
});
