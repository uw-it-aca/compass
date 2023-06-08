<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#affiliationsModal'"
    class="btn text-nowrap"
    @click="loadAffiliations()"
    :class="[
      buttonType === 'button'
        ? 'btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2'
        : 'small p-0 btn-sm btn-link',
    ]"
  >
    <slot>Add Affiliation</slot>
  </a>

  <!-- contact modal -->
  <div
    ref="affiliationsModal"
    class="modal fade text-start"
    :id="'affiliationsModal'"
    tabindex="-1"
    aria-labelledby="affiliationsModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
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
              <lable class="form-label small fw-bold me-2"> Program </lable>
            </div>
            <div class="col">
              <lable class="form-label small fw-bold me-2">External</lable>
            </div>
          </div>

          <div class="mb-3">
            <lable class="form-label small fw-bold me-2">Cohort</lable>
          </div>
          <div class="mb-3">
            <lable class="form-label small fw-bold me-2">Admin Note</lable>
            <textarea
              :class="
                formErrors.notes ? 'is-invalid form-control' : 'form-control'
              "
              rows="3"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <div class="text-end">
            <button
              type="button"
              class="btn btn-secondary me-2"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-primary bg-purple"
              @click="saveAffiliations()"
            >
              Add Affiliation
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import dataMixin from "../../../mixins/data_mixin.js";
import { Modal } from "bootstrap";

export default {
  mixins: [dataMixin],
  emits: ["affiliationsUpdated"],
  props: {
    buttonType: {
      type: String,
      required: true,
    },
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      affiliations: [],
      formErrors: {},
      updatePermissionDenied: false,
      errorResponse: "",
    };
  },
  created() {
    this.loadAffiliations();
  },
  mounted() {
    this.$refs.affiliationsModal.addEventListener(
      "shown.bs.modal",
      this.clearFormErrors
    );
    this.$refs.affiliationsModal.addEventListener(
      "hidden.bs.modal",
      this.resetForm
    );
  },
  methods: {
    loadAffiliations() {
      this.getAffiliations().then(
        (response) => {
          if (response.data) {
            this.affiliations = response.data;
          }
        }
      );
    },
    saveAffiliations() {
      var affiliationsModal = Modal.getInstance(
        document.getElementById("affiliationsModal")
      );
      /*
      this.saveStudentAffiliations(this.person.student.system_key)
        .then(() => {
          this.$emit("affiliationsUpdated");
          affiliationsModal.hide();
        })
        .catch((error) => {
          if (error.response.status == 401) {
            this.updatePermissionDenied = true;
            this.errorResponse = error.response.data;
            setTimeout(() => (this.updatePermissionDenied = false), 3000);
          } else {
            this.formErrors = error.response.data;
          }
        });
        */
    },
    clearFormErrors() {
      this.formErrors = {};
    },
    resetForm() {
      this.clearFormErrors();
      this.loadAffiliations();
    },
  },
};
</script>
