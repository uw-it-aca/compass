import "regenerator-runtime/runtime";
import axios from "axios";

const dataMixin = {
  methods: {
    _getAxiosConfig: function () {
      const csrfToken = this.$store.state.csrfToken;
      const axiosConfig = {
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
          "Access-Control-Allow-Origin": "*",
          "X-CSRFToken": csrfToken,
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
    saveStudent: async function (systemkey, programs) {
      return axios.post(
        "/api/internal/student/save/",
        {
          system_key: systemkey,
          programs: programs,
        },
        this._getAxiosConfig()
      );
    },
    getPrograms: async function () {
      return axios.get("/api/internal/programs/", {}, this._getAxiosConfig());
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
      return axios.post(
        "/api/internal/contact/save/",
        { contact: contact, system_key: systemkey },
        this._getAxiosConfig()
      );
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
  },
};

export default dataMixin;
