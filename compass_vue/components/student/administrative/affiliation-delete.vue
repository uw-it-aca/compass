<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#deleteAffiliationsModal' + this.studentAffiliation.id"
    class="btn text-nowrap"
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
    :id="'deleteAffiliationsModal' + this.studentAffiliation.id"
    tabindex="-1"
    aria-labelledby="deleteAffiliationsModalLabel{{ this.studentAffiliation.id }}"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <form ref="form" @submit="deleteAffiliation">
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
                v-model.trim="notes"
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
                class="btn btn-primary bg-danger"
                value="Delete"
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
import dataMixin from "@/mixins/data_mixin.js";
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
    studentAffiliation: {
      type: Object,
      required: true,
    },
    studentAffiliations: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      notes: "",
      formErrors: {},
      updatePermissionDenied: false,
      errorResponse: "",
    };
  },
  created() {},
  mounted() {},
  computed: {
    invalidForm() {
      return !(this.notes.length > 0);
    },
  },
  methods: {
    deleteAffiliation() {
      event.preventDefault();

      this.deleteStudentAffiliation(
        this.person.student.system_key,
        this.studentAffiliation.id
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
              if (error.response.status == 401) {
                this.updatePermissionDenied = true;
                this.errorResponse = error.response.data;
                setTimeout(() => (this.updatePermissionDenied = false), 3000);
              } else {
                this.formErrors.notes = error.response.data;
              }
            });
        })
        .catch((error) => {
          if (error.response.status == 401) {
            this.updatePermissionDenied = true;
            this.errorResponse = error.response.data;
            setTimeout(() => (this.updatePermissionDenied = false), 3000);
          } else {
            this.formErrors.notes = error.response.data;
          }
        });
    },
    updateStudentAffiliation() {
      let deleteIndex = null;

      this.studentAffiliations.forEach((item, index) => {
        if (this.studentAffiliation.id == item.id) deleteIndex = index;
      });

      this.studentAffiliations.splice(deleteIndex, 1);
    },
    hideModal() {
      var deleteAffiliationsModal = Modal.getInstance(
        document.getElementById(
          "deleteAffiliationsModal" + this.studentAffiliation.id
        )
      );

      deleteAffiliationsModal.hide();
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
