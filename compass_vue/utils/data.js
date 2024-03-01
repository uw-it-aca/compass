import "regenerator-runtime/runtime";
import axios from "axios";
import { useTokenStore } from "@/stores/token";

// request interceptor
axios.interceptors.request.use(
  function (config) {
    const tokenStore = useTokenStore();

    config.headers["Content-Type"] = "application/json;charset=UTF-8";
    config.headers["Access-Control-Allow-Origin"] = "*";
    config.headers["X-CSRFToken"] = tokenStore.csrfToken;
    config.headers["X-Requested-With"] = "XMLHttpRequest";
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

// methods
function _handleError(error) {
  if (error.response) {
    if (error.response.status === 403) {
      // Expired Session
      return alert(
        "Your session has expired. Refresh the page to start a new session."
      );
    }
    throw error;
  }
}

async function getStudentDetail(uwnetid) {
  return axios
    .get("/api/internal/student/" + uwnetid + "/")
    .catch(_handleError);
}

async function saveStudent(systemkey, uwnetid, programs) {
  return axios
    .post("/api/internal/student/" + uwnetid + "/", {
      system_key: systemkey,
      programs: programs,
    })
    .catch(_handleError);
}

async function getEligibilities() {
  return axios.get("/api/internal/eligibility/");
}

async function getStudentEligibility(systemkey) {
  return axios.get("/api/internal/student/" + systemkey + "/eligibility/");
}

async function setStudentEligibility(systemkey, eligibility_type_id) {
  return axios
    .post("/api/internal/student/" + systemkey + "/eligibility/", {
      system_key: systemkey,
      eligibility_type_id: eligibility_type_id,
    })
    .catch(_handleError);
}

async function getAffiliations() {
  return axios.get("/api/internal/accessgroup/affiliations/");
}

async function getSettings(accessGroupPk, settingType) {
  return axios.get(
    "/api/internal/accessgroup/" +
      accessGroupPk +
      "/settings/" +
      settingType +
      "/"
  );
}

async function saveSettings(accessGroupPk, settingType, settingValues) {
  return axios
    .post(
      "/api/internal/accessgroup/" +
        accessGroupPk +
        "/settings/" +
        settingType +
        "/",
      { setting_type: settingType, setting_values: settingValues }
    )
    .catch(_handleError);
}

async function getStudentSchedules(uwregid) {
  return axios.get("/api/internal/student/" + uwregid + "/schedules/");
}

async function getStudentTranscripts(uwregid) {
  return axios.get("/api/internal/student/" + uwregid + "/transcripts/");
}
async function saveStudentContact(systemkey, contact) {
  let postUrl = "/api/internal/contact/";
  if (contact.id !== undefined) {
    postUrl += contact.id + "/";
  }
  return axios
    .post(postUrl, { contact: contact, system_key: systemkey })
    .catch(_handleError);
}

async function updateStudentContact(contact) {
  let putUrl = "/api/internal/contact/" + contact.id + "/";
  return axios.put(putUrl, { contact: contact }).catch(_handleError);
}

async function saveStudentAffiliation(systemkey, affiliation) {
  let postUrl = "/api/internal/student/" + systemkey + "/affiliations/";
  if (affiliation.studentAffiliationId !== null) {
    postUrl += affiliation.studentAffiliationId + "/";
  }
  return axios.post(postUrl, { affiliation: affiliation }).catch(_handleError);
}

async function deleteStudentAffiliation(systemkey, affiliation_id) {
  return axios
    .delete(
      "/api/internal/student/" +
        systemkey +
        "/affiliations/" +
        affiliation_id +
        "/"
    )
    .catch(_handleError);
}

async function getStudentContacts(systemkey) {
  return axios.get("/api/internal/student/" + systemkey + "/contacts/");
}

async function getStudentContact(contactId) {
  return axios.get("/api/internal/contact/" + contactId + "/");
}

async function getStudentContactTopics() {
  return axios.get("/api/internal/contact/topics/");
}

async function getStudentContactTypes() {
  return axios.get("/api/internal/contact/types/");
}

async function getStudentContactMethods() {
  return axios.get("/api/internal/contact/methods/");
}

async function deleteStudentContact(contactId) {
  return axios.delete("/api/internal/contact/" + contactId + "/");
}

async function getStudentAffiliations(systemkey, affiliation_id) {
  return axios.get(
    "/api/internal/student/" +
      systemkey +
      "/affiliations/" +
      (affiliation_id !== undefined ? affiliation_id : "")
  );
}

async function getStudentVisits(systemkey) {
  return axios.get("/api/internal/student/" + systemkey + "/visits/");
}

async function getStudentSpecialProgram(systemkey) {
  let getUrl = "/api/internal/student/" + systemkey + "/special_program/";

  return axios.get(getUrl);
}

async function saveStudentSpecialProgram(systemkey, data) {
  let postUrl = "/api/internal/student/" + systemkey + "/special_program/";

  return axios.post(postUrl, { special_program: data }).catch(_handleError);
}

async function updateStudentSpecialProgram(systemkey, data) {
  let putUrl = "/api/internal/student/" + systemkey + "/special_program/";

  return axios.put(putUrl, { special_program: data }).catch(_handleError);
}

async function deleteStudentSpecialProgram(systemkey) {
  let deleteUrl = "/api/internal/student/" + systemkey + "/special_program/";

  return axios.delete(deleteUrl);
}

async function getAdviserCaseload(adviserNetId) {
  return axios
    .get("/api/internal/adviser/" + adviserNetId + "/caseload/")
    .catch(_handleError);
}

async function getAdviserCheckIns(adviserNetId) {
  return axios
    .get("/api/internal/adviser/" + adviserNetId + "/checkins/")
    .catch(_handleError);
}

async function getAccessGroups() {
  return axios.get("/api/internal/accessgroup/").catch(_handleError);
}

async function clearOverride() {
  return axios.post("/api/internal/support/", { clear_override: true });
}

async function savePreferences(preferences) {
  return axios.put("/api/internal/userprefs/", preferences);
}

export {
  getStudentDetail,
  saveStudent,
  getEligibilities,
  getStudentEligibility,
  setStudentEligibility,
  getAffiliations,
  getSettings,
  saveSettings,
  getStudentSchedules,
  getStudentTranscripts,
  saveStudentContact,
  updateStudentContact,
  saveStudentAffiliation,
  deleteStudentAffiliation,
  getStudentContacts,
  getStudentContact,
  getStudentContactTopics,
  getStudentContactTypes,
  getStudentContactMethods,
  deleteStudentContact,
  getStudentAffiliations,
  getStudentVisits,
  getStudentSpecialProgram,
  saveStudentSpecialProgram,
  updateStudentSpecialProgram,
  deleteStudentSpecialProgram,
  getAdviserCaseload,
  getAdviserCheckIns,
  getAccessGroups,
  clearOverride,
  savePreferences
};
