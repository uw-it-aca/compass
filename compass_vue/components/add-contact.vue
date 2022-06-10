<template>
  <a
    href="#"
    role="button"
    data-bs-toggle="modal"
    data-bs-target="#contactModal"
    class="btn text-nowrap"
    :class="[
      buttonType === 'button'
        ? 'btn-sm btn-outline-dark-beige'
        : 'small p-0 btn-sm btn-link',
    ]"
  >
    <slot>Add Contact</slot>
  </a>

  <!-- contact modal -->
  <div
    ref="modal"
    class="modal fade text-start"
    id="contactModal"
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
        <div class="modal-body">
          <div class="row mb-3">
            <div class="col">
              <label for="date" class="form-label">Date:</label>
              <input
                type="date"
                id="date"
                v-model="contactModel.date"
                :class="
                  formErrors.date ? 'is-invalid form-control' : 'form-control'
                "
              />
              <small class="text-danger" v-if="formErrors.date">
                required
              </small>
            </div>
            <div class="col">
              <label class="form-label">Contact type:</label>
              <select
                aria-label="Contact type"
                v-model="contactModel.contact_type"
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
              <small class="text-danger" v-if="formErrors.contact_type">
                required
              </small>
            </div>
            <div class="col">
              <div class="row">
                <div class="col">
                  <label for="appt-time" class="form-label"
                    >Check in time:</label
                  >
                  <input
                    id="appt-time"
                    type="time"
                    name="appt-time"
                    v-model="contactModel.time"
                    :class="
                      formErrors.time
                        ? 'is-invalid form-control'
                        : 'form-control'
                    "
                  />
                  <small class="text-danger" v-if="formErrors.time">
                    required
                  </small>
                </div>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Topics Covered:</label>
            <small class="text-danger" v-if="formErrors.contact_topics">
              required
            </small>
            <div style="column-count: 3">
              <div
                class="form-check"
                v-for="topic in contactTopics"
                :key="topic.id"
              >
                <input
                  type="checkbox"
                  v-model="contactModel.contact_topics"
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
              v-model="contactModel.notes"
            ></textarea>
            <small class="text-danger" v-if="formErrors.notes">
              required
            </small>
          </div>

          <div class="mb-3">
            <label for="actionsAndRecomendationsTextarea" class="form-label"
              >Actions and Recommmendations</label
            >
            <textarea
              class="form-control"
              id="actionsAndRecomendationsTextarea"
              rows="3"
              v-model="contactModel.actions"
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

export default {
  mixins: [dataMixin],
  props: {
    buttonType: {
      type: String,
      required: true,
    },
    person: {
      type: Object,
      required: true,
    },
    contact: {
      type: Object,
      required: false,
      default: function () {
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
    },
  },
  data() {
    return {
      contactTopics: [],
      contactTypes: [],
      contactModel: this.contact,
      formErrors: {},
    };
  },
  created() {
    this.getContactTopics();
    this.getContactTypes();
  },
  mounted() {
    this.$refs.modal.addEventListener("shown.bs.modal", this.clearFormErrors);
    this.$refs.modal.addEventListener("hidden.bs.modal", this.clearFormErrors);
  },
  methods: {
    saveContact() {
      let _this = this;
      this.saveStudentContact(this.person.student.system_key, this.contactModel)
        .then(() => {
          _this.$refs.modal.style.display = "none";
        })
        .catch((error) => {
          _this.formErrors = error.response.data;
        });
    },
    getContactTopics() {
      let _this = this;
      this.getStudentContactTopics().then((response) => {
        if (response.data) {
          _this.contactTopics = response.data;
        }
      });
    },
    getContactTypes() {
      let _this = this;
      this.getStudentContactTypes().then((response) => {
        if (response.data) {
          _this.contactTypes = response.data;
        }
      });
    },
    clearFormErrors() {
      this.formErrors = {};
    },
  },
};
</script>
