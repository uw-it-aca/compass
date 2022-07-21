<template>
  <div v-if="contacts.length > 0" class="table-responsive border rounded-3">
    <table class="table mb-0">
      <thead class="small bg-light text-secondary">
        <tr>
          <th class="ps-3" style="width: 33%" scope="col">Student</th>
          <th scope="col">Date</th>
          <th scope="col">Time</th>
          <th scope="col">Contact Type</th>
          <th scope="col">Meeting With</th>
          <th scope="col">Assigned Adviser</th>
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
          <td>
            <ul class="list-unstyled">
              <li
                v-for="(adviser, index) in contact.student.student.advisers"
                :key="index"
              >
                {{ adviser.uwnetid }}
              </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else class="mt-5 text-secondary">No students to meet with.</div>
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
