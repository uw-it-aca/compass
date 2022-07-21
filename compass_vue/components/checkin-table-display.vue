<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-50">Student</th>
        <th scope="col">Date</th>
        <th scope="col">Time</th>
        <th scope="col">Contact Type</th>
        <th scope="col">Adviser</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="contact in contacts" :key="contact.id">
        <td>
          <profile-mini :person="contact.student"></profile-mini>
        </td>
        <td>{{ contact.date }}</td>
        <td>{{ contact.time }}</td>
        <td>{{ contact.contact_type.name }}</td>
        <td>{{ contact.author.uwnetid }}</td>
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
    contacts: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
