<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#affiliationsModal'"
    class="btn text-nowrap"
    @click="getAffiliations()"
    :class="[
      buttonType === 'button'
        ? 'btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2'
        : 'small p-0 btn-sm btn-link',
    ]"
  >
    <slot>Edit Affiliation</slot>
  </a>

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
          <h5 class="modal-title h6 m-0 fw-bold">Edit Affiliation</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body" v-if="affiliations"></div>

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
              Save Changes
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
      affiliations: this.getStudentAffiliations(),
      formErrors: {},
      updatePermissionDenied: false,
      errorResponse: "",
    };
  },
  created() {},
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
    getAffiliations() {
      /*
      this.getStudentAffiliations(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            let newAffiliations;
            // update the current affiliations
            this.affiliations = newAffiliations;
          }
        }
      );*/
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
      //this.affiliations = this.getStudentAffiliations();
    },
  },
};
</script>
