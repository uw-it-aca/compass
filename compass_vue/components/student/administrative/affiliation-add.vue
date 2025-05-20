<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#addAffiliationsModal'"
    class="btn text-nowrap"
    :class="[
      buttonType === 'button'
        ? 'btn-sm btn-secondary rounded-3 px-3 py-2'
        : 'small p-0 btn-sm btn-link',
    ]"
  >
    <slot>Add Affiliation</slot>
  </a>

  <!-- contact modal -->
  <div
    :id="'addAffiliationsModal'"
    ref="addAffiliationsModal"
    class="modal fade text-start"
    tabindex="-1"
    aria-labelledby="affiliationsModalLabelAdd"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <form ref="form" @submit="saveAffiliation">
          <div class="modal-header">
            <h5 class="modal-title h6 m-0 fw-bold">Add Affiliation</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <!-- body -->
          <div class="modal-body">
            <div class="row mb-3">
              <div class="col">
                <label class="form-label small fw-bold me-2">
                  Affiliation
                </label>
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
            </div>

            <div class="mb-3">
              <label class="form-label small fw-bold me-2">Status</label>
              <p>User will be set to active status</p>
            </div>

            <div class="mb-3">
              <label class="form-label small fw-bold me-2">Cohort</label>
              <div class="cohort-list overflow-auto">
                <ul class="list-group">
                  <li
                    v-for="(cohort, index) in allCohorts"
                    :key="index"
                    :value="index"
                    class="list-group-item"
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
                value="Add Affiliation"
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
import { saveStudentAffiliation, saveStudentContact } from "@/utils/data";

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
    affiliations: {
      type: Object,
      required: true,
    },
    studentAffiliations: {
      type: Object,
      required: true,
    },
  },
  emits: ["affiliationsUpdated", "push"],
  setup() {
    return {
      saveStudentAffiliation,
      saveStudentContact,
    };
  },
  data() {
    return {
      affiliationId: null,
      is_active: true,
      actively_advised: true,
      cohorts: [],
      notes: "",
      allCohorts: getCohorts(5),
      formErrors: {},
      updatePermissionDenied: false,
      errorResponse: "",
    };
  },
  computed: {
    invalidForm() {
      return !(this.cohorts.length > 0 && this.notes.length > 0);
    },
  },
  created() {},
  mounted() {
    this.$refs.addAffiliationsModal.addEventListener(
      "shown.bs.modal",
      this.clearFormErrors
    );
    this.$refs.addAffiliationsModal.addEventListener(
      "hidden.bs.modal",
      this.resetForm
    );
  },
  methods: {
    isCurrentAffiliation(affiliation) {
      let is_current = false;
      this.studentAffiliations.forEach((item) => {
        if (affiliation.id == item.affiliation.id) is_current = true;
      });

      return is_current;
    },
    saveAffiliation() {
      let affiliationData = {
        studentAffiliationId: null,
        affiliationId: this.affiliationId,
        cohorts: this.cohorts,
        actively_advised: true,
      };

      event.preventDefault();
      this.saveStudentAffiliation(
        this.person.student.system_key,
        affiliationData
      )
        .then((response) => {
          this.saveStudentContact(this.person.student.system_key, {
            contact_type: "Admin",
            contact_method: "Internal",
            contact_topics: ["Other"],
            notes: this.notes,
          })
            .then(() => {
              this.updateStudentAffiliations(response);
              this.$emit("affiliationsUpdated");
              this.hideModal();
            })
            .catch((error) => {
              if (error.startsWith("401")) {
                this.updatePermissionDenied = true;
                this.errorResponse = error;
                setTimeout(() => (this.updatePermissionDenied = false), 3000);
              } else {
                this.formErrors.notes = error;
              }
            });
        })
        .catch((error) => {
          if (error.startsWith("401")) {
            this.updatePermissionDenied = true;
            this.errorResponse = error;
            setTimeout(() => (this.updatePermissionDenied = false), 3000);
          } else {
            this.formErrors.affiliation = error;
          }
        });
    },
    updateStudentAffiliations(newAffiliation) {
      // this.studentAffiliations.push(newAffiliation);
      this.$emit("push", newAffiliation);
    },
    hideModal() {
      var addAffiliationsModal = Modal.getInstance(
        document.getElementById("addAffiliationsModal")
      );

      addAffiliationsModal.hide();
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
