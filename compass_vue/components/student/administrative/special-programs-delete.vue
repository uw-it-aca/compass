<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#deleteSpecialProgramModal'"
    class="btn btn-sm fs-9 btn-outline-danger rounded-3 px-2 py-1 ms-1"
  >
    <slot>Delete Special Program Date</slot>
  </a>

  <div
    :id="'deleteSpecialProgramModal'"
    ref="specialProgramModal"
    class="modal fade text-start"
    tabindex="-1"
    aria-labelledby="deleteSpecialProgramModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-md">
      <div class="modal-content">
        <form ref="form" @submit="deleteSpecialProgram">
          <div class="modal-header">
            <h5 class="modal-title h6 m-0 fw-bold">
              Delete Special Programs Date
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <div class="mb-3 text-light-emphasis">
                Warning: Consider carefully before deleting Special Programs
                Code's Date value as there is no way to undo this action.
              </div>
            </div>
            <div v-if="errorResponse" class="text-danger">
              Problem Deleting Date: {{ errorResponse.message }}
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
                class="btn btn-primary bg-danger"
                value="Delete"
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
import { deleteStudentSpecialProgram } from "@/utils/data";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
    programData: {
      type: Object,
      required: true,
    },
  },
  emits: ["specialProgramUpdated"],
  setup() {
    return {
      deleteStudentSpecialProgram,
    };
  },
  data() {
    return {
      updatePermissionDenied: false,
      errorResponse: "",
    };
  },
  mounted() {
    this.$refs.specialProgramModal.addEventListener(
      "shown.bs.modal",
      this.formShown
    );
    this.$refs.specialProgramModal.addEventListener(
      "hidden.bs.modal",
      this.resetForm
    );
  },
  methods: {
    deleteSpecialProgram() {
      event.preventDefault();
      this.deleteStudentSpecialProgram(this.person.student.system_key)
        .then(() => {
          this.$emit("specialProgramUpdated");
          this.hideModal();
        })
        .catch((error) => {
          this.errorResponse = error.data;
        });
    },
    hideModal() {
      var deleteSpecialProgramModal = Modal.getInstance(
        document.getElementById("deleteSpecialProgramModal")
      );

      deleteSpecialProgramModal.hide();
    },
    formShown() {
      this.clearFormErrors();
    },
    clearFormErrors() {
      this.formErrors = null;
      this.errorResponse = null;
    },
    resetForm() {
      this.clearFormErrors();
    },
  },
};
</script>
