import "regenerator-runtime/runtime";
import axios from "axios";
import { useTokenStore } from "@/stores/token";

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
    _handleError: function (error) {
      if (error.response) {
        if (error.response.status === 302) {
          // Expired Session
          alert("Your session has expired. Refresh the page to start a new session.");
        } else {
          console.log(error.response);
        }
      } else if (error.request) {
        console.log(error.request);
      } else {
        console.log('Error', error.message);
      }
    },
    getStudentDetail: async function (uwnetid) {
      return axios.get(
        "/api/internal/student/" + uwnetid + "/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    saveStudent: async function (systemkey, uwnetid, programs) {
      return axios.post(
        "/api/internal/student/" + uwnetid + "/",
        {
          system_key: systemkey,
          programs: programs,
        },
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getEligibilities: async function () {
      return axios.get(
        "/api/internal/eligibility/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentEligibility: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/eligibility/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    setStudentEligibility: async function (systemkey, eligibility_type_id) {
      return axios.post(
        "/api/internal/student/" + systemkey + "/eligibility/",
        {
          system_key: systemkey,
          eligibility_type_id: eligibility_type_id,
        },
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getAffiliations: async function () {
      return axios.get(
        "/api/internal/accessgroup/affiliations/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
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
      ).catch(this._handleError);
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
      ).catch(this._handleError);
    },
    getStudentSchedules: async function (uwregid) {
      return axios.get(
        "/api/internal/student/" + uwregid + "/schedules/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentTranscripts: async function (uwregid) {
      return axios.get(
        "/api/internal/student/" + uwregid + "/transcripts/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
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
      ).catch(this._handleError);
    },
    saveStudentAffiliation: async function (systemkey, affiliation) {
      let postUrl = "/api/internal/student/" + systemkey + "/affiliations/";
      if (affiliation.studentAffiliationId != undefined) {
        postUrl += affiliation.studentAffiliationId + "/";
      }
      return axios.post(
        postUrl,
        { affiliation: affiliation },
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    deleteStudentAffiliation: async function (systemkey, affiliation_id) {
      let deleteUrl =
        "/api/internal/student/" +
        systemkey +
        "/affiliations/" +
        affiliation_id +
        "/";
      return axios.delete(
        deleteUrl, this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentContacts: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/contacts/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentContact: async function (contactId) {
      return axios.get(
        "/api/internal/contact/" + contactId + "/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentContactTopics: async function () {
      return axios.get(
        "/api/internal/contact/topics/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentContactTypes: async function () {
      return axios.get(
        "/api/internal/contact/types/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentContactMethods: async function () {
      return axios.get(
        "/api/internal/contact/methods/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentAffiliations: async function (systemkey, affiliation_id) {
      return axios.get(
        "/api/internal/student/" +
          systemkey +
          "/affiliations/" +
          (affiliation_id !== undefined ? affiliation_id : ""),
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getStudentVisits: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/visits/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getAdviserCaseload: async function (adviserNetId) {
      return axios.get(
        "/api/internal/adviser/" + adviserNetId + "/caseload/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getAdviserContacts: async function (adviserNetId) {
      return axios.get(
        "/api/internal/adviser/" + adviserNetId + "/contacts/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    getAccessGroups: async function () {
      return axios.get(
        "/api/internal/accessgroup/",
        {},
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
    clearOverride: async function () {
      return axios.post(
        "/api/internal/support/",
        { clear_override: true },
        this._getAxiosConfig()
      ).catch(this._handleError);
    },
  },
};

export default dataMixin;
