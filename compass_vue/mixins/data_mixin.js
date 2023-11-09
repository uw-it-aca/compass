import "regenerator-runtime/runtime";
import axios from "axios";
import { useTokenStore } from "@/stores/token";

// Request interceptor
axios.interceptors.request.use(function (config) {
    const tokenStore = useTokenStore();

    config.headers['Content-Type'] = 'application/json;charset=UTF-8';
    config.headers['Access-Control-Allow-Origin'] = '*';
    config.headers["X-CSRFToken"] = tokenStore.csrfToken;
    return config;
  }, function (error) {
    return Promise.reject(error);
  });

const dataMixin = {
  methods: {
    _handleError: function (error) {
      if (error.response) {
        if (error.response.status === 302) {
          // Expired Session
          return alert("Your session has expired. Refresh the page to start a new session.");
        }
      }
    },
    getStudentDetail: async function (uwnetid) {
      return axios.get(
        "/api/internal/student/" + uwnetid + "/"
      ).catch(this._handleError);
    },
    saveStudent: async function (systemkey, uwnetid, programs) {
      return axios.post("/api/internal/student/" + uwnetid + "/",
        {system_key: systemkey, programs: programs}
      );
    },
    getEligibilities: async function () {
      return axios.get("/api/internal/eligibility/");
    },
    getStudentEligibility: async function (systemkey) {
      return axios.get("/api/internal/student/" + systemkey + "/eligibility/");
    },
    setStudentEligibility: async function (systemkey, eligibility_type_id) {
      return axios.post("/api/internal/student/" + systemkey + "/eligibility/",
        {system_key: systemkey, eligibility_type_id: eligibility_type_id}
      );
    },
    getAffiliations: async function () {
      return axios.get("/api/internal/accessgroup/affiliations/");
    },
    getSettings: async function (accessGroupPk, settingType) {
      return axios.get("/api/internal/accessgroup/" + accessGroupPk +
        "/settings/" + settingType + "/");
    },
    saveSettings: async function (accessGroupPk, settingType, settingValues) {
      return axios.post("/api/internal/accessgroup/" + accessGroupPk +
        "/settings/" + settingType + "/",
        {setting_type: settingType, setting_values: settingValues});
    },
    getStudentSchedules: async function (uwregid) {
      return axios.get("/api/internal/student/" + uwregid + "/schedules/");
    },
    getStudentTranscripts: async function (uwregid) {
      return axios.get("/api/internal/student/" + uwregid + "/transcripts/");
    },
    saveStudentContact: async function (systemkey, contact) {
      let postUrl = "/api/internal/contact/";
      if (contact.id !== undefined) {
        postUrl += contact.id + "/";
      }
      return axios.post(postUrl, {contact: contact, system_key: systemkey});
    },
    saveStudentAffiliation: async function (systemkey, affiliation) {
      let postUrl = "/api/internal/student/" + systemkey + "/affiliations/";
      if (affiliation.studentAffiliationId !== undefined) {
        postUrl += affiliation.studentAffiliationId + "/";
      }
      return axios.post(postUrl, {affiliation: affiliation});
    },
    deleteStudentAffiliation: async function (systemkey, affiliation_id) {
      return axios.delete("/api/internal/student/" + systemkey +
        "/affiliations/" + affiliation_id + "/");
    },
    getStudentContacts: async function (systemkey) {
      return axios.get("/api/internal/student/" + systemkey + "/contacts/");
    },
    getStudentContact: async function (contactId) {
      return axios.get("/api/internal/contact/" + contactId + "/");
    },
    getStudentContactTopics: async function () {
      return axios.get("/api/internal/contact/topics/");
    },
    getStudentContactTypes: async function () {
      return axios.get("/api/internal/contact/types/");
    },
    getStudentContactMethods: async function () {
      return axios.get("/api/internal/contact/methods/");
    },
    getStudentAffiliations: async function (systemkey, affiliation_id) {
      return axios.get("/api/internal/student/" + systemkey + "/affiliations/" +
        (affiliation_id !== undefined ? affiliation_id : ""));
    },
    getStudentVisits: async function (systemkey) {
      return axios.get("/api/internal/student/" + systemkey + "/visits/");
    },
    getAdviserCaseload: async function (adviserNetId) {
      return await axios.get(
        "/api/internal/adviser/" + adviserNetId + "/caseload/"
      ).catch(this._handleError);
    },
    getAdviserContacts: async function (adviserNetId) {
      return await axios.get(
        "/api/internal/adviser/" + adviserNetId + "/contacts/"
      ).catch(this._handleError);
    },
    getAccessGroups: async function () {
      return axios.get("/api/internal/accessgroup/");
    },
    clearOverride: async function () {
      return axios.post("/api/internal/support/", { clear_override: true });
    },
  },
};

export default dataMixin;
