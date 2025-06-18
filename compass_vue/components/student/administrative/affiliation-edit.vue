<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#editAffiliationsModal' + studentAffiliation.id"
    class="btn btn-sm fs-9 btn-outline-danger rounded-3 px-2 py-1"
  >
    <slot>Edit Affiliation</slot>
  </a>

  <div
    :id="'editAffiliationsModal' + studentAffiliation.id"
    ref="affiliationsModal"
    class="modal fade text-start"
    tabindex="-1"
    aria-labelledby="editAffiliationsModalLabel{{ this.studentAffiliation.id }}"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <form ref="form" @submit="updateAffiliation">
          <div class="modal-header">
            <h5 class="modal-title h6 m-0 fw-bold">Edit Affiliation</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="col mb-3">
              <label class="form-label small fw-bold me-2">Affiliation</label>
              <select v-model="affiliationId" class="form-select" required>
                <option
                  v-for="(a, index) in affiliations"
                  :key="index"
                  :value="a.id"
                  :disabled="isCurrentAffiliation(a)"
                >
                  {{ a.name }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <div class="form-label small fw-bold me-2">Status</div>
              <div class="form-check form-switch">
                <input
                  id="activeSwitch"
                  v-model="isActive"
                  class="form-check-input"
                  type="checkbox"
                />
                <label class="form-check-label" for="activeSwitch"
                  >Set user as active</label
                >
              </div>
            </div>

            <div class="row mb-3">
              <div class="col">
                <label class="form-label small fw-bold me-2">Cohort</label>
                <div class="cohort-list overflow-auto">
                  <ul class="list-group">
                    <li
                      v-for="(cohort, index) in allCohorts"
                      :key="index"
                      class="list-group-item"
                      :value="index"
                    >
                      <label
                        ><input
                          v-model="cohorts"
                          class="form-check-input me-1"
                          type="checkbox"
                          :value="cohort"
                        />
                        {{ cohort.start_year }}-{{ cohort.end_year }}</label
                      >
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label small fw-bold me-2">Admin Note</label>
              <textarea
                v-model.trim="notes"
                :class="
                  formErrors.notes ? 'is-invalid form-control' : 'form-control'
                "
                rows="3"
                required
              ></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <div class="text-end">
              <input
                type="button"
                class="btn btn-secondary me-2"
                data-bs-dismiss="modal"
                value="Cancel"
              />
              <input
                type="submit"
                class="btn btn-primary bg-purple"
                value="Save Changes"
                :disabled="invalidForm"
              />
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from "bootstrap";
import { getCohorts } from "@/utils/cohorts";
import {
  clearOverride,
  saveStudentAffiliation,
  saveStudentContact,
} from "@/utils/data";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
    studentAffiliation: {
      type: Object,
      required: true,
    },
    studentAffiliations: {
      type: Object,
      required: true,
    },
    affiliations: {
      type: Object,
      required: true,
    },
  },
  emits: ["affiliationsUpdated"],
  setup() {
    return {
      clearOverride,
      saveStudentAffiliation,
      saveStudentContact,
    };
  },
  data() {
    return {
      affiliationId: null,
      isActive: null,
      cohorts: [],
      notes: "",
      allCohorts: getCohorts(20),
      formErrors: {},
      updatePermissionDenied: false,
      errorResponse: null,
    };
  },
  computed: {
    invalidForm() {
      return !(this.cohorts.length > 0 && this.notes.length > 0);
    },
  },
  created() {},
  mounted() {
    this.$refs.affiliationsModal.addEventListener(
      "shown.bs.modal",
      this.formShown
    );
    this.$refs.affiliationsModal.addEventListener(
      "hidden.bs.modal",
      this.resetForm
    );
  },

  methods: {
    isCurrentAffiliation(affiliation) {
      let is_current = false;
      this.studentAffiliations.forEach((item) => {
        if (affiliation.id == item.affiliation.id)
          is_current =
            affiliation.id !== this.studentAffiliation.affiliation.id;
      });

      return is_current;
    },
    updateAffiliation(event) {
      let affiliationData = {
        studentAffiliationId: this.studentAffiliation.id,
        affiliationId: this.affiliationId,
        cohorts: this.cohorts,
        actively_advised: this.isActive,
      };

      event.preventDefault();

      this.saveStudentAffiliation(
        this.person.student.system_key,
        affiliationData
      )
        .then(() => {
          // write Contact Note from advisor type Admin
          this.saveStudentContact(this.person.student.system_key, {
            contact_type: "Admin",
            contact_method: "Internal",
            contact_topics: ["Other"],
            notes: this.notes,
          })
            .then(() => {
              this.updateStudentAffiliation();
              this.$emit("affiliationsUpdated");
              this.hideModal();
            })
            .catch((error) => {
              if (error.data.status === 401) {
                this.updatePermissionDenied = true;
                this.errorResponse = error.data;
                setTimeout(() => (this.updatePermissionDenied = false), 3000);
              } else {
                this.formErrors.notes = error.data.message;
              }
            });
        })
        .catch((error) => {
          if (error.data.status === 401) {
            this.updatePermissionDenied = true;
            this.errorResponse = error.data;
            setTimeout(() => (this.updatePermissionDenied = false), 3000);
          } else {
            this.formErrors.affiliation = error.data.message;
          }
        });
    },
    hideModal() {
      var editAffiliationsModal = Modal.getInstance(
        document.getElementById(
          "editAffiliationsModal" + this.studentAffiliation.id
        )
      );

      editAffiliationsModal.hide();
    },
    updateStudentAffiliation() {
      this.studentAffiliations.forEach((item) => {
        if (item.id == this.studentAffiliation.id) {
          item.actively_advised = this.isActive;
          item.cohorts = this.cohorts;
          this.affiliations.forEach((affiliation) => {
            if (this.affiliationId == affiliation.id)
              item.affiliation = affiliation;
          });
        }
      });
    },
    formShown() {
      this.affiliationId = this.studentAffiliation.affiliation.id;
      this.isActive = this.studentAffiliation.actively_advised;
      this.cohorts = this.studentAffiliation.cohorts;
      this.notes = "";
      this.clearFormErrors();
    },
    clearFormErrors() {
      this.formErrors = {};
    },
    resetForm() {
      this.clearFormErrors();
    },
  },
};
</script>

<style lang="scss" scoped>
.cohort-list {
  height: 250px;
}
</style>
