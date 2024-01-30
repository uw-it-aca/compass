<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#editSpecialProgramModal'"
    class="btn text-nowrap btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2"
  >
    <slot>Add Program Date</slot>
  </a>

  <div
    ref="specialProgramModal"
    class="modal fade text-start"
    :id="'editSpecialProgramModal'"
    tabindex="-1"
    aria-labelledby="editSpecialProgramModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-md">
      <div class="modal-content">
        <form ref="form" @submit="editSpecialProgram">
          <div class="modal-header">
            <h5 class="modal-title h6 m-0 fw-bold">
              Add Special Programs Date
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
              <lable class="form-label small fw-bold"
                >Specify date below.</lable
              >
              <input
                type="date"
                id="affiliation_date"
                :value="program_date"
                @input="
                  program_date = new Date($event.target.valueAsDate)
                    .toISOString()
                    .slice(0, 10)
                "
                class="form-control form-control-sm"
              />
            </div>
            <div v-if="this.errorResponse" class="text-danger">
              Problem Changing Date: {{ this.errorResponse.statusText }} ({{
                this.errorResponse.data
              }})
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
                value="Save"
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
import { getToday } from "@/utils/dates";
import {
  saveStudentSpecialProgram,
  updateStudentSpecialProgram,
} from "@/utils/data";

export default {
  emits: ["specialProgramUpdated"],
  props: {
    person: {
      type: Object,
      required: true,
    },
    program_data: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      saveStudentSpecialProgram,
      updateStudentSpecialProgram,
      getToday,
    };
  },
  data() {
    return {
      updatePermissionDenied: false,
      errorResponse: null,
      formErrors: null,
      program_date: this.program_data.program_date
        ? new Date(this.program_data.program_date).toISOString().slice(0, 10)
        : this.getToday().format("YYYY-MM-DD"),
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
    editSpecialProgram() {
      let store = this.program_data.hasOwnProperty("program_code")
          ? this.updateStudentSpecialProgram
          : this.saveStudentSpecialProgram,
        program_data_copy = JSON.parse(JSON.stringify(this.program_data));

      program_data_copy.program_date = this.program_date;

      event.preventDefault();
      store(
        this.person.student.system_key,
        this.person.student.special_program_code,
        program_data_copy
      )
        .then(() => {
          this.program_data.program_date = this.program_date;
          this.$emit("specialProgramUpdated");
          this.hideModal();
        })
        .catch((error) => {
          this.errorResponse = error.response;
        });
    },
    hideModal() {
      var editSpecialProgramModal = Modal.getInstance(
        document.getElementById("editSpecialProgramModal")
      );

      editSpecialProgramModal.hide();
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
