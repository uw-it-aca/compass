import { defineStore } from "pinia";
import {
  getStudentContactTopics,
  getStudentContactTypes,
  getStudentContactMethods,
} from "@/utils/data";

export const useContactStore = defineStore({
  id: "contact",
  state: () => {
    return {
      getStudentContactTopics,
      getStudentContactTypes,
      getStudentContactMethods,
      contactTopics: {},
      contactMethods: {},
      contactTypes: {},
    };
  },
  getters: {},
  actions: {
    fetchStudentContactTopics() {
      if (!Object.prototype.hasOwnProperty.call(this.contactTopics, 'request')) {
        this.contactTopics.request = this.getStudentContactTopics().then(
          (response) => {
            this.contactTopics.data = response.data;
          });
      }
      return this.contactTopics.request;
    },
    fetchStudentContactTypes() {
      if (!Object.prototype.hasOwnProperty.call(this.contactTypes, 'request')) {
        this.contactTypes.request = this.getStudentContactTypes().then(
          (response) => {
            this.contactTypes.data = response.data;
          });
      }
      return this.contactTypes.request;
    },
    fetchStudentContactMethods() {
      if (!Object.prototype.hasOwnProperty.call(this.contactMethods, 'request')) {
        this.contactMethods.request = this.getStudentContactMethods().then(
          (response) => {
            this.contactMethods.data = response.data;
          });
      }
      return this.contactMethods.request;
    },
  },
});
