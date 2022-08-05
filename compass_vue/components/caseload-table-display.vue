<template>
  <div v-if="persons.length > 0" class="table-responsive mx-n3 mb-n3">
    <table class="table table-striped table-borderless m-0">
      <thead class="table-light">
        <tr>
          <th scope="col" style="width: 33%" class="ps-3">Student</th>
          <th scope="col">Class</th>
          <th scope="col">Campus</th>
          <th scope="col" class="text-nowrap">Enrollment Status</th>
          <th scope="col">Adviser</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="person in persons" :key="person.uwnetid">
          <td>
            <profile-mini :person="person"></profile-mini>
          </td>
          <td>{{ person.student.class_desc }}</td>
          <td>{{ person.student.campus_desc }}</td>
          <td>{{ person.student.enrollment_status_desc }}</td>
          <td>
            <div v-for="adviser in person.student.advisers" :key="adviser.id">
              {{ adviser.uwnetid }}
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else>no students in {{ adviserNetId }}'s caseload</div>
</template>

<script>
import ProfileMini from "../components/student/profile-mini.vue";

export default {
  components: {
    "profile-mini": ProfileMini,
  },
  props: {
    adviserNetId: {
      type: String,
      required: true,
    },
    persons: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
