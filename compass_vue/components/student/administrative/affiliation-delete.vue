<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#deleteAffiliationsModal' + studentAffiliation.id"
    class="btn btn-sm fs-9 btn-outline-danger rounded-3 px-2 py-1 ms-1"
  >
    <slot>Delete Affiliation</slot>
  </a>

  <div
    :id="'deleteAffiliationsModal' + studentAffiliation.id"
    ref="affiliationsModal"
    class="modal fade text-start"
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
              <div class="mb-3 text-light-emphasis">
                Warning: Consider carefully before deleting an affiliation as
                there is no way to undo this action.
              </div>
              <label class="form-label small fw-bold">Admin Note</label>
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
import { Modal } from "bootstrap";
import { deleteStudentAffiliation, saveStudentContact } from "@/utils/data";

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
  },
  emits: ["affiliationsUpdated"],
  setup() {
    return {
      deleteStudentAffiliation,
      saveStudentContact,
    };
  },
  data() {
    return {
      notes: "",
      formErrors: {},
      updatePermissionDenied: false,
      errorResponse: "",
    };
  },
  computed: {
    invalidForm() {
      return !(this.notes.length > 0);
    },
  },
  created() {},
  mounted() {},
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
            this.formErrors.notes = error;
          }
        });
    },
    updateStudentAffiliation() {
      let deleteIndex = null;

      this.studentAffiliations.forEach((item, index) => {
        if (this.studentAffiliation.id == item.id) deleteIndex = index;
      });

      // eslint-disable-next-line vue/no-mutating-props
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
