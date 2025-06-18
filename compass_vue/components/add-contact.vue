<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#contactModal' + contactId"
    class="btn text-nowrap"
    :class="[
      buttonType === 'button'
        ? 'btn-sm btn-secondary rounded-3 px-3 py-2'
        : 'btn btn-sm fs-9 btn-outline-danger rounded-3 px-2 py-1 ms-1',
    ]"
    @click="getFormData()"
  >
    <slot>Add Contact</slot>
  </a>

  <!-- add/edit contact modal -->
  <div
    :id="'contactModal' + contactId"
    ref="contactModal"
    class="modal fade text-start"
    tabindex="-1"
    aria-labelledby="contactModalLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 id="contactModalLabel" class="modal-title h6 m-0 fw-bold">
            Record a contact
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div
                v-show="updatePermissionDenied"
                class="alert alert-danger py-2 small"
                role="alert"
              >
                {{ errorResponsePermission }}
              </div>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="checkin_date" class="form-label small fw-bold me-2"
                >Checkin Date</label
              >
              <span v-if="formErrors.checkin_date" class="text-danger">
                required
              </span>
              <input
                id="checkin_date"
                v-model="contact.checkin_date"
                type="datetime-local"
                :class="
                  formErrors.checkin_date
                    ? 'is-invalid form-control form-control-sm'
                    : 'form-control '
                "
              />
            </div>

            <div class="col">
              <label class="form-label small fw-bold me-2">
                Contact types
              </label>
              <span v-if="formErrors.contact_type" class="text-danger">
                required
              </span>
              <!-- MARK: disable editing contact_type if either qq/appointment (1,2) for Advisers -->
              <select
                v-model="contact.contact_type"
                aria-label="Contact type"
                :class="
                  formErrors.time ? 'is-invalid form-select' : 'form-select'
                "
                :disabled="
                  (userRoles.includes(Role.User) &&
                    contact.contact_type == 1) ||
                  (userRoles.includes(Role.Student) &&
                    contact.contact_type == 1) ||
                  (userRoles.includes(Role.User) &&
                    contact.contact_type == 2) ||
                  (userRoles.includes(Role.Student) &&
                    contact.contact_type == 2)
                "
              >
                <option selected disabled :value="undefined">
                  Choose one...
                </option>
                <template
                  v-for="contactType in contactTypes"
                  :key="contactType.id"
                >
                  <!-- MARK: disable contact_type if either qq/appointment for Advisers -->
                  <option
                    :disabled="
                      (userRoles.includes(Role.User) &&
                        contactType.slug == 'quick-question') ||
                      (userRoles.includes(Role.Student) &&
                        contactType.slug == 'quick-question') ||
                      (userRoles.includes(Role.User) &&
                        contactType.slug == 'appointment') ||
                      (userRoles.includes(Role.Student) &&
                        contactType.slug == 'appointment')
                    "
                    :value="contactType.id"
                  >
                    {{ contactType.name }}
                  </option>
                </template>
              </select>
            </div>

            <div class="col">
              <label class="form-label small fw-bold me-2"
                >Contact method:</label
              >
              <span v-if="formErrors.contact_method" class="text-danger">
                required
              </span>
              <select
                v-model="contact.contact_method"
                aria-label="Contact method"
                :class="
                  formErrors.time ? 'is-invalid form-select' : 'form-select'
                "
              >
                <option selected disabled :value="undefined">
                  Choose one...
                </option>

                <template
                  v-for="contactMethod in contactMethods"
                  :key="contactMethod.id"
                >
                  <option :value="contactMethod.id">
                    {{ contactMethod.name }}
                  </option>
                </template>
              </select>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label small fw-bold me-2">Topics Covered</label>
            <span class="small text-muted">(choose all that apply)</span>
            <span v-if="formErrors.contact_topics" class="text-danger">
              required
            </span>
            <ul class="list-inline">
              <template v-for="topic in contactTopics" :key="topic.id">
                <li
                  v-if="topic.slug !== 'none'"
                  class="list-inline-item mb-1 me-1"
                >
                  <input
                    :id="'#contactModal' + contactId + 'Topic' + topic.id"
                    v-model="contact.contact_topics"
                    type="checkbox"
                    class="btn-check"
                    :class="formErrors.contact_topics ? 'is-invalid' : ''"
                    :value="topic.id"
                    autocomplete="off"
                  />
                  <label
                    class="btn btn-sm btn-outline-dark-beige fs-9 rounded-pill"
                    :for="'#contactModal' + contactId + 'Topic' + topic.id"
                    >{{ topic.name }}</label
                  >
                </li>
              </template>
            </ul>
          </div>
          <div class="mb-3">
            <label for="notesTextarea" class="form-label small fw-bold me-2"
              >Notes</label
            >
            <span v-if="formErrors.notes" class="text-danger"> required </span>
            <textarea
              id="notesTextarea"
              v-model="contact.notes"
              rows="3"
              :class="
                formErrors.notes ? 'is-invalid form-control' : 'form-control'
              "
            ></textarea>
          </div>
          <div class="mb-3">
            <label
              for="actionsAndRecomendationsTextarea"
              class="form-label small fw-bold me-2"
              >Actions and Recommmendations</label
            >
            <textarea
              id="actionsAndRecomendationsTextarea"
              v-model="contact.actions"
              rows="3"
              class="form-control"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <div class="text-end">
            <button
              type="button"
              class="btn btn-sm btn-outline-primary rounded-3 px-3 py-2 me-2"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn-sm btn-primary rounded-3 px-3 py-2"
              @click="saveContact()"
            >
              Save contact
            </button>
            <p>
              <span v-if="errorResponse" class="text-danger">{{
                errorResponse
              }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- end visit modal -->
</template>

<script>
import { useContactStore } from "@/stores/contact";
import {
  getStudentContact,
  saveStudentContact,
  updateStudentContact,
} from "@/utils/data";
import { Modal } from "bootstrap";
import { Role } from "@/utils/roles";

export default {
  props: {
    buttonType: {
      type: String,
      required: true,
    },
    person: {
      type: Object,
      required: true,
    },
    contactId: {
      type: Number,
      default: null,
    },
  },
  emits: ["contactUpdated"],
  setup() {
    const storeContact = useContactStore();
    return {
      storeContact,
      getStudentContact,
      saveStudentContact,
      updateStudentContact,
    };
  },
  data() {
    return {
      contact: this.getDefaultContact(),
      formErrors: {},
      updatePermissionDenied: false,
      errorResponsePermission: "",
      errorResponse: "",
      userRoles: document.body.getAttribute("data-user-role").split(","),
      Role: Role,
      submitAttempted: false,
    };
  },
  computed: {
    contactTopics() {
      return this.storeContact.contactTopics;
    },
    contactTypes() {
      return this.storeContact.contactTypes;
    },
    contactMethods() {
      return this.storeContact.contactMethods;
    },
  },
  watch: {
    contact: {
      handler: function () {
        // Don't show 'required' errors until the user has tried to submit
        // then update on every form edit
        if (this.submitAttempted) {
          this.validateContactForm();
        }
      },
      deep: true,
    },
  },
  mounted() {
    this.$refs.contactModal.addEventListener(
      "shown.bs.modal",
      this.clearFormErrors
    );
    this.$refs.contactModal.addEventListener("hidden.bs.modal", this.resetForm);
  },
  methods: {
    getFormData() {
      if (this.contactId != null) {
        this.getContact(this.contactId);
      }
    },
    saveContact() {
      this.submitAttempted = true;
      if (!this.validateContactForm()) {
        return;
      }
      var contactModal = Modal.getInstance(
        document.getElementById("contactModal" + this.contactId)
      );
      if (this.contact.id !== undefined) {
        this.updateStudentContact(this.contact)
          .then(() => {
            this.$emit("contactUpdated");
            contactModal.hide();
          })
          .catch((error) => {
            if (error.data.status === 401) {
              this.updatePermissionDenied = true;
              this.errorResponsePermission = error;
              setTimeout(() => (this.updatePermissionDenied = false), 3000);
            } else {
              this.errorResponse = error.data;
            }
          });
      } else {
        this.saveStudentContact(this.person.student.system_key, this.contact)
          .then(() => {
            this.$emit("contactUpdated");
            contactModal.hide();
          })
          .catch((error) => {
            if (error.data.status === 401) {
              this.updatePermissionDenied = true;
              this.errorResponsePermission = error;
              setTimeout(() => (this.updatePermissionDenied = false), 3000);
            } else {
              this.errorResponse = error.data;
            }
          });
      }
    },
    validateContactForm() {
      let is_invalid = false;
      // date widget returns empty string if invalid
      if (this.contact.checkin_date === "") {
        this.formErrors.checkin_date = true;
        is_invalid = true;
      } else {
        this.formErrors.checkin_date = false;
      }
      if (this.contact.contact_type === undefined) {
        this.formErrors.contact_type = true;
        is_invalid = true;
      } else {
        this.formErrors.contact_type = false;
      }
      if (this.contact.contact_method === undefined) {
        this.formErrors.contact_method = true;
        is_invalid = true;
      } else {
        this.formErrors.contact_method = false;
      }
      if (this.contact.contact_topics.length > 0) {
        this.formErrors.contact_topics = false;
      } else {
        this.formErrors.contact_topics = true;
        is_invalid = true;
      }

      return !is_invalid;
    },
    getDefaultContact() {
      var today = new Date();

      function zPad(value) {
        if (value <= 9) value = "0" + value;
        return value;
      }

      function getCurrentDateTimeStr() {
        let curMonth = zPad(today.getMonth() + 1);
        let curDay = zPad(today.getDate());
        let curHour = zPad(today.getHours());
        let curMinutes = zPad(today.getMinutes());
        return (
          today.getFullYear() +
          "-" +
          curMonth +
          "-" +
          curDay +
          "T" +
          curHour +
          ":" +
          curMinutes
        );
      }

      return {
        contact_topics: [],
        checkin_date: getCurrentDateTimeStr(),
      };
    },
    getContact(contactId) {
      this.getStudentContact(contactId).then((response) => {
        if (response) {
          // we need to map the contact type and topic ids to the data object
          let newContact = response;
          // convert date to local and format for datetime-local input
          newContact.checkin_date = new Date(newContact.checkin_date)
            .toLocaleString("sv-SE", {
              year: "numeric",
              month: "2-digit",
              day: "2-digit",
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            })
            .replace(" ", "T");
          newContact.contact_type = newContact.contact_type.id;
          if (newContact.contact_method != null) {
            newContact.contact_method = newContact.contact_method.id;
          } else {
            newContact.contact_method = undefined;
          }

          newContact.contact_topics = newContact.contact_topics.map(
            (ct) => ct.id
          );
          // update the current contact
          this.contact = newContact;
        }
      });
    },
    clearFormErrors() {
      this.formErrors = {};
    },
    resetForm() {
      this.clearFormErrors();
      this.contact = this.getDefaultContact();
    },
  },
};
</script>
