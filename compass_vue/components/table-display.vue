<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-50">Student</th>
        <th scope="col">Date</th>
        <th scope="col">Time</th>
        <th scope="col">Contact Type</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="person in persons" :key="person.id">
        <td>
          <profile-mini :person="person"></profile-mini>
        </td>
        <td>May 26, 2022</td>
        <td>2:30pm</td>
        <td>Appointment</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import ProfileMini from "../components/student/profile-mini.vue";

export default {
  components: {
    "profile-mini": ProfileMini,
  },
  props: {
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
