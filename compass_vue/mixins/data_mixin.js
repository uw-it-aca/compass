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
    dateMMDDYYYY: function (date) {
        return ((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + date.getFullYear();
    },
    dateHHMMampm: function (date) {
      var hours = date.getHours(),
          minutes = date.getMinutes(),
          ampm = hours >= 12 ? 'pm' : 'am';
      hours = hours % 12;
      hours = hours ? hours : 12;
      minutes = minutes < 10 ? '0' + minutes : minutes;
      return hours + ':' + minutes + ampm;
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
    getAffiliations: async function (accessGroupPk) {
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
    getStudentAffiliations: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/affiliations/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentVisits: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/visits/",
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
