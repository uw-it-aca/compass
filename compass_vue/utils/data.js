import "regenerator-runtime/runtime";
//import { useTokenStore } from "@/stores/token";
import { useCustomFetch } from "@/composables/customFetch";

/*
async function customFetch(url, options = {}) {
  const tokenStore = useTokenStore();

  // Set default headers
  const defaultHeaders = {
    "Access-Control-Allow-Origin": "*",
    "X-CSRFToken": tokenStore.csrfToken,
    "X-Requested-With": "XMLHttpRequest",
  };

  // Merge default headers with any provided in options
  options.headers = {
    ...defaultHeaders,
    ...options.headers,
  };

  try {
    const response = await fetch(url, options);

    // Handle expired session (403 status)
    if (response.status === 403) {
      alert(
        "Your session has expired. Refresh the page to start a new session."
      );
      return;
    }

    // Check if response is ok (status 2xx)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse and return JSON response
    return response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
}
  */

async function getStudentDetail(uwnetid) {
  const url = "/api/internal/student/" + uwnetid + "/";
  return useCustomFetch(url);
}

async function saveStudent(systemkey, uwnetid, programs) {
  const url = "/api/internal/student/" + uwnetid + "/";
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      system_key: systemkey,
      programs: programs,
    }),
  });
}

async function getEligibilities() {
  const url = "/api/internal/eligibility/";
  return useCustomFetch(url);
}

async function getStudentEligibility(systemkey) {
  const url = "/api/internal/student/" + systemkey + "/eligibility/";
  return useCustomFetch(url);
}

async function setStudentEligibility(systemkey, eligibility_type_id) {
  const url = "/api/internal/student/" + systemkey + "/eligibility/";
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      system_key: systemkey,
      eligibility_type_id: eligibility_type_id,
    }),
  });
}

async function getAffiliations() {
  const url = "/api/internal/accessgroup/affiliations/";
  return useCustomFetch(url);
}

async function getSettings(accessGroupPk, settingType) {
  const url =
    "/api/internal/accessgroup/" +
    accessGroupPk +
    "/settings/" +
    settingType +
    "/";
  return useCustomFetch(url);
}

async function saveSettings(accessGroupPk, settingType, settingValues) {
  const url =
    "/api/internal/accessgroup/" +
    accessGroupPk +
    "/settings/" +
    settingType +
    "/";
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      setting_type: settingType,
      setting_values: settingValues,
    }),
  });
}

async function getStudentSchedules(uwregid) {
  const url = "/api/internal/student/" + uwregid + "/schedules/";
  return useCustomFetch(url);
}

async function getStudentTranscripts(uwregid) {
  const url = "/api/internal/student/" + uwregid + "/transcripts/";
  return useCustomFetch(url);
}

async function saveStudentContact(systemkey, contact) {
  let url = "/api/internal/contact/";
  if (contact.id !== undefined) {
    url += contact.id + "/";
  }
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      contact: contact,
      system_key: systemkey,
    }),
  });
}

async function updateStudentContact(contact) {
  const url = "/api/internal/contact/" + contact.id + "/";
  return useCustomFetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      contact: contact,
    }),
  });
}

async function saveStudentAffiliation(systemkey, affiliation) {
  let url = "/api/internal/student/" + systemkey + "/affiliations/";
  if (affiliation.studentAffiliationId !== null) {
    url += affiliation.studentAffiliationId + "/";
  }
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      affiliation: affiliation,
    }),
  });
}

async function uploadStudentAffiliations(affiliation_id, file, cohort) {
  const url =
    "/api/internal/student/affiliations/" + affiliation_id + "/import/";
  let formData = new FormData();
  formData.append("file", file);
  formData.append("cohort", cohort);

  // Do not send a Content-Type header
  return useCustomFetch(url, {
    method: "POST",
    body: formData,
  });
}

async function deleteStudentAffiliation(systemkey, affiliation_id) {
  const url =
    "/api/internal/student/" +
    systemkey +
    "/affiliations/" +
    affiliation_id +
    "/";
  return useCustomFetch(url, {
    method: "DELETE",
  });
}

async function getStudentContacts(systemkey) {
  const url = "/api/internal/student/" + systemkey + "/contacts/";
  return useCustomFetch(url);
}

async function getStudentContact(contactId) {
  const url = "/api/internal/contact/" + contactId + "/";
  return useCustomFetch(url);
}

async function getStudentContactTopics() {
  const url = "/api/internal/contact/topics/";
  return useCustomFetch(url);
}

async function getStudentContactTypes() {
  const url = "/api/internal/contact/types/";
  return useCustomFetch(url);
}

async function getStudentContactMethods() {
  const url = "/api/internal/contact/methods/";
  return useCustomFetch(url);
}

async function deleteStudentContact(contactId) {
  const url = "/api/internal/contact/" + contactId + "/";
  return useCustomFetch(url, {
    method: "DELETE",
  });
}

async function getStudentAffiliations(systemkey, affiliation_id) {
  const url =
    "/api/internal/student/" +
    systemkey +
    "/affiliations/" +
    (affiliation_id !== undefined ? affiliation_id : "");
  return useCustomFetch(url);
}

async function getStudentVisits(systemkey) {
  const url = "/api/internal/student/" + systemkey + "/visits/";
  return useCustomFetch(url);
}

async function getStudentSpecialProgram(systemkey) {
  const url = "/api/internal/student/" + systemkey + "/special_program/";
  return useCustomFetch(url);
}

async function saveStudentSpecialProgram(systemkey, data) {
  const url = "/api/internal/student/" + systemkey + "/special_program/";
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      special_program: data,
    }),
  });
}

async function updateStudentSpecialProgram(systemkey, data) {
  const url = "/api/internal/student/" + systemkey + "/special_program/";
  return useCustomFetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      special_program: data,
    }),
  });
}

async function deleteStudentSpecialProgram(systemkey) {
  const url = "/api/internal/student/" + systemkey + "/special_program/";
  return useCustomFetch(url, {
    method: "DELETE",
  });
}

async function getAdviserCaseload(adviserNetId) {
  const url = "/api/internal/adviser/" + adviserNetId + "/caseload/";
  return useCustomFetch(url);
}

async function getAdviserCheckIns(adviserNetId) {
  const url = "/api/internal/adviser/" + adviserNetId + "/checkins/";
  return useCustomFetch(url);
}

async function getAccessGroups() {
  const url = "/api/internal/accessgroup/";
  return useCustomFetch(url);
}

async function clearOverride() {
  const url = "/api/internal/support/";
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({ clear_override: true }),
  });
}

async function savePreferences(preferences) {
  const url = "/api/internal/userprefs/";
  return useCustomFetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify(preferences),
  });
}

async function getStudentCourseAnalytics(uwnetid, year, quarter, course_id) {
  const url =
    "/api/internal/student/" +
    uwnetid +
    "/course_analytics/" +
    year +
    "/" +
    quarter +
    "/" +
    course_id +
    "/";
  return useCustomFetch(url);
}

async function getStudentSigninAnalytics(uwnetid) {
  const url = "/api/internal/student/" + uwnetid + "/signin_analytics/";
  return useCustomFetch(url);
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
  uploadStudentAffiliations,
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
  savePreferences,
  getStudentCourseAnalytics,
  getStudentSigninAnalytics,
};
