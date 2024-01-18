<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Special Programs</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled">
        <li>
          Code: {{ person.student.special_program_code }} -
          {{ person.student.special_program_desc }}
        </li>
      </ul>
      <!-- MARK: if now affiliation date set -->
      <div class="mb-3">
        <div class="small">
          <strong>Affiliation Date:</strong>
          <span class="ms-2">January 17, 2024</span><br />
          Modified by: <span class="text-muted">javereage</span>
        </div>
        <div class="mt-2 text-end">
          <button
            type="button"
            class="btn btn-outline-gray btn-sm text-danger rounded-3 px-2 py-1 fs-9"
          >
            <i class="bi bi-pencil me-2"></i>Edit
          </button>
          <button
            type="button"
            class="btn btn-outline-gray btn-sm text-danger rounded-3 px-2 py-1 fs-9 ms-1"
          >
            <i class="bi bi-trash ms-e"></i>Delete
          </button>
        </div>
      </div>
      <!-- MARK: set affiliation date -->
      <div>
        <div class="mb-3">
          <label for="affiliation_date" class="form-label small fw-bold me-2"
            >Affiliation Date: --</label
          >
          <p class="small text-muted">
            No affiliation date has been set for this student. Specify a date
            below.
          </p>
          <input
            type="date"
            id="affiliation_date"
            class="form-control form-control-sm"
          />
        </div>
        <div class="text-end">
          <button
            type="button"
            class="btn btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2 me-2"
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-sm btn-purple rounded-3 px-3 py-2"
          >
            Save
          </button>
        </div>
      </div>
    </template>
  </axdd-card>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      userNetid: document.body.getAttribute("data-user-netid"),
      userRole: document.body.getAttribute("data-user-role"),
      affiliations_date: "",
    };
  },
  components: {},
};
</script>
