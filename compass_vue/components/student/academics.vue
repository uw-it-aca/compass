<template>
  <div class="card border-light-gray shadow-sm rounded-3 mb-4">
    <div class="card-header bg-white border-0 p-4 pb-0">
      <h2
        class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
      >Academics</h2>
    </div>
    <div class="card-body p-4">
      <ul>
        <li>
          Registered:
          <template v-if="student.registered_in_quarter">
            <b>yes</b>/no
          </template>
          <template v-else>
            yes/
            <b>no</b>
          </template>
        </li>
        <li>Enrollment Status: {{ student.enrollment_desc }}</li>
        <li>Class standing: {{ student.class_desc }}</li>
        <li>Total Credits: {{ student.total_credits }}</li>
        <li>Total UW Credits: 170.00</li>
        <li>
          Transfer student:
          <b>yes</b>/no
        </li>
        <li>GPA: {{ student.gpa }}</li>
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
