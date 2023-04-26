import "regenerator-runtime/runtime";
import axios from "axios";
import { useTokenStore } from "../stores/token";

const dataMixin = {
  methods: {
    _getAxiosConfig: function () {
      //const csrfToken = this.$store.state.csrfToken;

      const tokenStore = useTokenStore();

      const axiosConfig = {
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
          "Access-Control-Allow-Origin": "*",
          "X-CSRFToken": tokenStore.csrfToken,
        },
      };
      return axiosConfig;
    },
    getStudentDetail: async function (uwnetid) {
      return axios.get(
        "/api/internal/student/" + uwnetid + "/",
        {},
        this._getAxiosConfig()
      );
    },
    saveStudent: async function (systemkey, uwnetid, programs) {
      return axios.post(
        "/api/internal/student/" + uwnetid + "/",
        {
          system_key: systemkey,
          programs: programs,
        },
        this._getAxiosConfig()
      );
    },
    getPrograms: async function (accessGroupPk) {
      return axios.get(
        "/api/internal/accessgroup/" + accessGroupPk + "/affiliations/",
        {},
        this._getAxiosConfig()
      );
    },
    getSettings: async function (accessGroupPk, settingType) {
      return axios.get(
        "/api/internal/accessgroup/" +
          accessGroupPk +
          "/settings/" +
          settingType +
          "/",
        {},
        this._getAxiosConfig()
      );
    },
    saveSettings: async function (accessGroupPk, settingType, settingValues) {
      return axios.post(
        "/api/internal/accessgroup/" +
          accessGroupPk +
          "/settings/" +
          settingType +
          "/",
        {
          setting_type: settingType,
          setting_values: settingValues,
        },
        this._getAxiosConfig()
      );
    },
    getStudentSchedules: async function (uwregid) {
      return axios.get(
        "/api/internal/student/" + uwregid + "/schedules/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentTranscripts: async function (uwregid) {
      return axios.get(
        "/api/internal/student/" + uwregid + "/transcripts/",
        {},
        this._getAxiosConfig()
      );
    },
    saveStudentContact: async function (systemkey, contact) {
      let postUrl = "/api/internal/contact/";
      if (contact.id != undefined) {
        postUrl += contact.id + "/";
      }
      return axios.post(
        postUrl,
        { contact: contact, system_key: systemkey },
        this._getAxiosConfig()
      );
    },
    getStudentAffiliations: async function (systemkey) {
      return true;
    },
    saveStudentAffiliations: async function (systemkey) {
      return true;
    },
    getStudentContacts: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/contacts/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentContact: async function (contactId) {
      return axios.get(
        "/api/internal/contact/" + contactId + "/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentContactTopics: async function () {
      return axios.get(
        "/api/internal/contact/topics/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentContactTypes: async function () {
      return axios.get(
        "/api/internal/contact/types/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentContactMethods: async function () {
      return axios.get(
        "/api/internal/contact/methods/",
        {},
        this._getAxiosConfig()
      );
    },
    getAdviserCaseload: async function (adviserNetId) {
      return axios.get(
        "/api/internal/adviser/" + adviserNetId + "/caseload/",
        {},
        this._getAxiosConfig()
      );
    },
    getAdviserContacts: async function (adviserNetId) {
      return axios.get(
        "/api/internal/adviser/" + adviserNetId + "/contacts/",
        {},
        this._getAxiosConfig()
      );
    },
    getAccessGroups: async function () {
      return axios.get(
        "/api/internal/accessgroup/",
        {},
        this._getAxiosConfig()
      );
    },
    clearOverride: async function () {
      return axios.post(
        "/api/internal/support/",
        { clear_override: true },
        this._getAxiosConfig()
      );
    },
  },
};

export default dataMixin;
