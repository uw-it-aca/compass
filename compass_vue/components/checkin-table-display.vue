<template>
  <div v-if="contacts.length > 0" class="table-responsive m-n3">
    <table class="table m-0">
      <thead class="text-muted small">
        <tr>
          <th class="bg-body-secondary ps-3" style="width: 25%" scope="col">
            Student
          </th>
          <th scope="col" style="width: 15%">Check-in Date</th>
          <th scope="col" style="width: 15%">Source</th>
          <th scope="col" style="width: 15%">Contact Type</th>
          <th scope="col" style="width: 15%">Meeting With</th>
          <th scope="col" class="text-nowrap">Assigned Adviser</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="contact in contacts" :key="contact.id">
          <td class="ps-3">
            <profile-mini :person="contact.student"></profile-mini>
          </td>
          <td>
            {{ formatDate(contact.checkin_date_str, "LLL") }}
          </td>
          <td>{{ contact.source }} -- {{ contact.trans_id }}</td>
          <td>{{ contact.contact_type__name }}</td>
          <td>{{ contact.app_user__uwnetid }}</td>
          <td>
            <ul class="list-unstyled">
              <li
                v-for="(uwnetid, index) in contact.student.adviser_uwnetids"
                :key="index"
              >
                {{ uwnetid }}
              </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else class="p-3">You have not met with any students recently.</div>
</template>

<script>
import ProfileMini from "@/components/student/profile-mini.vue";
import { formatDate } from "@/utils/dates";

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
  setup() {
    return {
      formatDate,
    };
  },
  data() {
    return {};
  },
};
</script>
