<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#deleteAffiliationsModal'"
    class="btn text-nowrap"
    @click="loadAffiliations()"
    :class="[
      buttonType === 'button'
        ? 'rounded-3 px-3 py-0'
        : 'small p-0 btn-sm btn-link',
    ]"
  >
    <slot>Edit Affiliation</slot>
  </a>

  <div
    ref="affiliationsModal"
    class="modal fade text-start"
    :id="'deleteAffiliationsModal'"
    tabindex="-1"
    aria-labelledby="deleteAffiliationsModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title h6 m-0 fw-bold">Delete Affiliation</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <div class="mb-3 text-secondary">
              Warning: Consider carefully before deleting an affiliation as
              there is no way to undo this action.
            </div>
            <lable class="form-label small fw-bold">Admin Note</lable>
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
              class="btn btn-primary bg-danger"
              @click="saveAffiliations()"
            >
              Delete
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
import { useAffiliationStore } from "../../../stores/affiliations";

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
  setup() {
    const storeAffiliations = useAffiliationStore();
    return { storeAffiliations };
  },
  created() {
    this.loadAffiliations();
  },
  mounted() {
    /*
    this.$refs.editAffiliationsModal.addEventListener(
      "shown.bs.modal",
      this.clearFormErrors
    );
    this.$refs.editAffiliationsModal.addEventListener(
      "hidden.bs.modal",
      this.resetForm
    );
    */
  },
  methods: {
    loadAffiliations() {
      this.storeAffiliations.affiliationsPromise.then(
        (response) => {
          if (response.data) {
            this.affiliations = response.data;
          }
        }
      );
    },
    saveAffiliations() {
      var editAffiliationsModal = Modal.getInstance(
        document.getElementById("editAffiliationsModal")
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
