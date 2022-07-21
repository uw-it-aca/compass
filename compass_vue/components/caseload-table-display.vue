<template>
  <div class="table-responsive">
    <table v-if="persons.length > 0" class="table mb-0">
      <thead class="small">
        <tr>
          <th scope="col" class="ps-0">Student</th>
          <th scope="col">Class</th>
          <th scope="col">Campus</th>
          <th scope="col" class="text-nowrap">Enrollment Status</th>
          <th scope="col">Adviser</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="person in persons"
          :key="person.uwnetid"
          class="bg-light-hover"
        >
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
    <div v-else>no students in {{ adviserNetId }}'s caseload</div>
  </div>
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
