<template>
  <div v-if="contacts.length > 0" class="table-responsive m-n3">
    <table class="table m-0">
      <thead class="table-light text-muted small">
        <tr>
          <th class="ps-3" style="width: 33%" scope="col">Student</th>
          <th scope="col">Check-in Date</th>
          <th scope="col">Contact Type</th>
          <th scope="col">Meeting With</th>
          <th scope="col">Assigned Adviser</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="contact in contacts" :key="contact.id">
          <td class="ps-3">
            <profile-mini :person="contact.student"></profile-mini>
          </td>
          <td>{{ contact.checkin_date }}</td>
          <td>{{ contact.contact_type.name }}</td>
          <td>{{ contact.app_user.uwnetid }}</td>
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
  <div v-else>No students to meet with.</div>
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
