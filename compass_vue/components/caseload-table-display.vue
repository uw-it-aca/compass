<template>
  <div v-if="persons.length > 0" class="table-responsive m-n3">
    <table class="table m-0">
      <thead class="table-light text-muted small">
        <tr>
          <th scope="col" style="width: 33%" class="ps-3">Student</th>
          <th scope="col">Class</th>
          <th scope="col">Campus</th>
          <th scope="col" class="text-nowrap">Enrollment Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="person in persons" :key="person.uwnetid">
          <td class="ps-3">
            <profile-mini :person="person"></profile-mini>
          </td>
          <td>{{ person.student.class_desc }}</td>
          <td>{{ person.student.campus_desc }}</td>
          <td>
            <ul>
              <li>
                Special Program:
                <!-- show N/A when student isn't in any special program -->

                <span
                  v-if="
                    person.student.special_program_code === '1' ||
                    person.student.special_program_code === '2' ||
                    person.student.special_program_code === '13'
                  "
                  class="badge text-bg-success"
                >
                  {{ person.student.special_program_code }},
                  {{ person.student.special_program_desc }}
                </span>
                <span v-else class="badge text-bg-light-gray"> N/A</span>
              </li>
              <li>
                Registered in quarter:
                <span
                  class="badge"
                  :class="
                    !person.student.registered_in_quarter
                      ? 'text-bg-danger'
                      : 'text-bg-light-gray'
                  "
                >
                  {{ person.student.registered_in_quarter }}
                </span>
              </li>
              <li>
                Enrollment Status Code: {{ person.student.enroll_status_code }}
              </li>
              <li>
                Registration Hold:
                <span
                  class="badge"
                  :class="
                    person.student.registration_hold_ind
                      ? 'text-bg-danger'
                      : 'text-bg-light-gray'
                  "
                  >{{ person.student.registration_hold_ind }}
                </span>
              </li>
            </ul>
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
