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
    getStudentList: async function (paginationOptions, searchOptions) {
      let options = Object.assign({}, paginationOptions, searchOptions);
      return axios.get(
        "/api/internal/student/",
        { params: options },
        this._getAxiosConfig()
      );
    },
    getStudentDetail: async function (uwnetid) {
      return axios.get(
        "/api/internal/student/" + uwnetid + "/",
        {},
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
    getStudentPrograms: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/programs/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentSpecialPrograms: async function (systemkey) {
      return axios.get(
        "/api/internal/student/" + systemkey + "/specialprograms/",
        {},
        this._getAxiosConfig()
      );
    },
    getPrograms: async function () {
      return axios.get("/api/internal/programs/", {}, this._getAxiosConfig());
    },
    getSpecialPrograms: async function () {
      return axios.get(
        "/api/internal/specialprograms/",
        {},
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
    saveStudentContact: async function (systemkey, contact) {
      return axios.post(
        "/api/internal/contact/save/",
        { contact: contact, system_key: systemkey },
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
    getStudentContactTopics: async function (systemkey) {
      return axios.get(
        "/api/internal/contact/topics/",
        {},
        this._getAxiosConfig()
      );
    },
    getStudentContactTypes: async function (systemkey) {
      return axios.get(
        "/api/internal/contact/types/",
        {},
        this._getAxiosConfig()
      );
    },
    getAdviserList: async function () {
      return axios.get("/api/internal/adviser/", {}, this._getAxiosConfig());
    },
  },
};

export default dataMixin;
