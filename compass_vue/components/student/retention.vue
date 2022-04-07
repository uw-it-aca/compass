<template>
  <div class="card border-light-gray shadow-sm rounded-3 mb-4">
    <div class="card-header bg-white border-0 p-4 pb-0">
      <h2
        class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
      >Retention</h2>
    </div>
    <div class="card-body p-4">
      <ul>
        <li>
          Priority:
          <span class="fw-bold">{{ student.retention.priority }}</span>
        </li>
        <li>Sign-ins: {{ student.retention.sign_in }}</li>
        <li>Activity: {{ student.retention.activity }}</li>
        <li>Assignments: {{ student.retention.assignment }}</li>
        <li>Grades: {{ student.retention.grade }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    student: {
      type: Object,
      required: true,
    },
  },
  components: {
  },
  data() {
    return {};
  },
}
</script>
