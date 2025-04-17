import { defineStore } from "pinia";
import {
  getStudentContactTopics,
  getStudentContactTypes,
  getStudentContactMethods,
} from "@/utils/data";

export const useContactStore = defineStore("contact", {
  state: () => {
    return {
      _contactTopics: {},
      _contactMethods: {},
      _contactTypes: {},
    };
  },
  getters: {
    contactTopics(state) {
      if (
        !Object.prototype.hasOwnProperty.call(this._contactTopics, "request")
      ) {
        this._contactTopics.request = getStudentContactTopics().then(
          (response) => {
            this._contactTopics.data = response;
          }
        );
      }
      return this._contactTopics.data;
    },
    contactTypes(state) {
      if (
        !Object.prototype.hasOwnProperty.call(this._contactTypes, "request")
      ) {
        this._contactTypes.request = getStudentContactTypes().then(
          (response) => {
            this._contactTypes.data = response;
          }
        );
      }
      return this._contactTypes.data;
    },
    contactMethods(state) {
      if (
        !Object.prototype.hasOwnProperty.call(this._contactMethods, "request")
      ) {
        this._contactMethods.request = getStudentContactMethods().then(
          (response) => {
            this._contactMethods.data = response;
          }
        );
      }
      return this._contactMethods.data;
    },
  },
  actions: {},
});
