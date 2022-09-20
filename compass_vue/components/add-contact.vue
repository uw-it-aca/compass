<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#contactModal' + contactId"
    class="btn text-nowrap"
    @click="getFormData()"
    :class="[
      buttonType === 'button'
        ? 'btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2'
        : 'small p-0 btn-sm btn-link',
    ]"
  >
    <slot>Add Contact</slot>
  </a>

  <!-- contact modal -->
  <div
    ref="contactModal"
    class="modal fade text-start"
    :id="'contactModal' + contactId"
    tabindex="-1"
    aria-labelledby="contactModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="contactModalLabel">Record a contact</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body" v-if="contact">
          <div class="row">
            <div class="col">
              <div
                class="alert alert-danger py-2 small"
                role="alert"
                v-show="updatePermissionDenied"
              >
                You don't have permission to create or update contacts.
              </div>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="checkin_date" class="form-label">Checkin Date:</label>
              <input
                type="datetime-local"
                id="checkin_date"
                v-model="contact.checkin_date"
                :class="
                  formErrors.checkin_date
                    ? 'is-invalid form-control'
                    : 'form-control'
                "
              />
              <span class="text-danger" v-if="formErrors.checkin_date">
                required
              </span>
            </div>
            <div class="col">
              <label class="form-label">Contact type:</label>
              <select
                aria-label="Contact type"
                v-model="contact.contact_type"
                :class="
                  formErrors.time ? 'is-invalid form-select' : 'form-select'
                "
              >
                <option selected disabled :value="undefined">
                  Choose one...
                </option>
                <option
                  v-for="contactType in contactTypes"
                  :key="contactType.id"
                  :value="contactType.id"
                >
                  {{ contactType.name }}
                </option>
              </select>
              <span class="text-danger" v-if="formErrors.contact_type">
                required
              </span>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Topics Covered:</label>
            <span class="text-danger" v-if="formErrors.contact_topics">
              required
            </span>
            <div style="column-count: 3">
              <div
                class="form-check"
                v-for="topic in contactTopics"
                :key="topic.id"
              >
                <input
                  type="checkbox"
                  v-model="contact.contact_topics"
                  :class="
                    formErrors.contact_topics
                      ? 'is-invalid form-check-input'
                      : 'form-check-input'
                  "
                  :value="topic.id"
                  :id="topic.id"
                />
                <label class="form-check-label" :for="topic.id">{{
                  topic.name
                }}</label>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label for="notesTextarea" class="form-label">Notes</label>
            <textarea
              :class="
                formErrors.notes ? 'is-invalid form-control' : 'form-control'
              "
              id="notesTextarea"
              rows="3"
              v-model="contact.notes"
            ></textarea>
            <span class="text-danger" v-if="formErrors.notes"> required </span>
          </div>

          <div class="mb-3">
            <label for="actionsAndRecomendationsTextarea" class="form-label"
              >Actions and Recommmendations</label
            >
            <textarea
              class="form-control"
              id="actionsAndRecomendationsTextarea"
              rows="3"
              v-model="contact.actions"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer text-end">
          <div>
            <button
              type="button"
              class="btn btn-secondary me-2"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="saveContact()"
            >
              Save contact
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- end visit modal -->
</template>

<script>
import dataMixin from "../mixins/data_mixin.js";
import { Modal } from "bootstrap";

export default {
  mixins: [dataMixin],
  emits: ["contactUpdated"],
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
  data() {
    return {
      contactTopics: [],
      contactTypes: [],
      contact: this.getDefaultContact(),
      formErrors: {},
      updatePermissionDenied: false,
    };
  },
  created() {
    this.getContactTopics();
    this.getContactTypes();
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
      var contactModal = Modal.getInstance(
        document.getElementById("contactModal" + this.contactId)
      );
      this.saveStudentContact(this.person.student.system_key, this.contact)
        .then(() => {
          this.$emit("contactUpdated");
          contactModal.hide();
        })
        .catch((error) => {
          if (error.response.status == 401) {
            this.updatePermissionDenied = true;
            setTimeout(() => (this.updatePermissionDenied = false), 3000);
          } else {
            this.formErrors = error.response.data;
          }
        });
    },
    getDefaultContact() {
      var today = new Date();

      function zPad(value) {
        if (value <= 9) value = "0" + value;
        return value;
      }

      function getCurrentDateStr() {
        let curMonth = zPad(today.getMonth() + 1);
        let curDay = zPad(today.getDate());
        return today.getFullYear() + "-" + curMonth + "-" + curDay;
      }

      function getCurrentTimeStr() {
        let curHour = zPad(today.getHours());
        let curMinutes = zPad(today.getMinutes());
        let curSeconds = zPad(today.getSeconds());
        return curHour + ":" + curMinutes + ":" + curSeconds;
      }

      return {
        contact_topics: [],
        date: getCurrentDateStr(),
        time: getCurrentTimeStr(),
      };
    },
    getContact(contactId) {
      this.getStudentContact(contactId).then((response) => {
        if (response.data) {
          // we need to map the contact type and topic ids to the data object
          let newContact = response.data;
          newContact.contact_type = newContact.contact_type.id;
          newContact.contact_topics = newContact.contact_topics.map(
            (ct) => ct.id
          );
          // update the current contact
          this.contact = newContact;
        }
      });
    },
    getContactTopics() {
      this.getStudentContactTopics().then((response) => {
        if (response.data) {
          this.contactTopics = response.data;
        }
      });
    },
    getContactTypes() {
      this.getStudentContactTypes().then((response) => {
        if (response.data) {
          this.contactTypes = response.data;
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
