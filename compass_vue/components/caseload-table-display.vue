<template>
  <div v-if="persons.length > 0" class="table-responsive m-n3">
    <table class="table m-0">
      <thead class="table-light text-muted small">
        <tr>
          <th scope="col" style="width: 33%" class="ps-3">Student</th>
          <th scope="col">Class</th>
          <th scope="col">Campus</th>
          <th scope="col" style="width: 33%" class="text-nowrap">Status</th>
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
            <ul class="list-inline d-flex m-0">
              <li class="list-inline-item d-none">
                Special Program:
                <!-- show N/A when student isn't in any special program -->

                <span
                  v-if="person.student.special_program_code === '0'"
                  class="badge text-bg-light-gray"
                >
                  N/A</span
                >
                <span v-else class="badge text-bg-success">
                  {{ person.student.special_program_code }},
                  {{ person.student.special_program_desc }}
                </span>
              </li>
              <li class="list-inline-item flex-fill">
                <div>Registered</div>
                <span
                  class="small badge rounded-pill alert border-0 px-2 py-1 mb-0 me-1"
                  :class="
                    !person.student.registered_in_quarter
                      ? 'alert-danger'
                      : 'alert-secondary'
                  "
                >
                  {{ translateTrueFalse(person.student.registered_in_quarter) }}
                </span>
              </li>
              <li class="list-inline-item d-none">
                Enrollment Status Code: {{ person.student.enroll_status_code }}
              </li>
              <li class="list-inline-item flex-fill">
                <div>Registration Holds</div>
                <span
                  class="small badge rounded-pill alert border-0 px-2 py-1 mb-0 me-1"
                  :class="
                    person.student.registration_hold_ind
                      ? 'alert-danger'
                      : 'alert-secondary'
                  "
                  >{{
                    translateTrueFalse(person.student.registration_hold_ind)
                  }}
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
import { translateTrueFalse } from "../utils/translations";

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
  setup() {
    return {
      translateTrueFalse,
    };
  },
  data() {
    return {};
  },
};
</script>
