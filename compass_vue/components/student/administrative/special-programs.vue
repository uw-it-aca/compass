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
          <strong>Affiliation Date:</strong> January 17, 2024<br />
          <span class="text-muted">javereage</span>
        </div>
      </div>
      <!-- MARK: set affiliation date -->
      <div>
        <div class="mb-3">
          <label for="affiliation_date" class="form-label small fw-bold me-2"
            >Affiliation Date</label
          >
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
