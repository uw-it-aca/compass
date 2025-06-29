<template>
  <div v-if="persons.length > 0" class="table-responsive m-n3">
    <table class="table m-0">
      <thead class="text-muted small">
        <tr>
          <th scope="col" style="width: 34%" class="bg-body-tertiary ps-3">
            Student
          </th>
          <th scope="col" class="bg-body-tertiary">Class</th>
          <th scope="col" class="bg-body-tertiary">Campus</th>
          <th
            scope="col"
            style="width: 45%"
            class="text-nowrap bg-body-tertiary"
          >
            Status
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="person in persons" :key="person.uwnetid">
          <td class="ps-3">
            <profile-mini :person="person"></profile-mini>
          </td>
          <td class="small">{{ person.class_desc }}</td>
          <td class="small">{{ person.campus_desc }}</td>
          <td class="small">
            <ul class="list-inline d-flex m-0">
              <li class="list-inline-item d-none">
                Special Program:
                <!-- show N/A when student isn't in any special program -->

                <span
                  v-if="person.special_program_code === '0'"
                  class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1 text-bg-secondary"
                >
                  N/A</span
                >
                <span v-else class="badge text-bg-success">
                  {{ person.special_program_code }},
                  {{ person.special_program_desc }}
                </span>
              </li>
              <li class="list-inline-item flex-fill w-25">
                <div>Degree</div>
                <span
                  class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1 text-bg-secondary"
                >
                  {{ getDegreeData(person).degree_desc }}</span
                >
              </li>
              <li class="list-inline-item flex-fill w-25">
                <div>Acad. Standing</div>
                <span
                  class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1"
                  :class="
                    getScholarshipData(person).scholarship_type == 3 ||
                    getScholarshipData(person).scholarship_type == 4
                      ? 'text-bg-danger'
                      : 'text-bg-secondary'
                  "
                  >{{ getScholarshipData(person).scholarship_desc }}</span
                >
              </li>
              <li class="list-inline-item flex-fill w-25">
                <div>Registered</div>
                <span
                  class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1"
                  :class="
                    !person.registered_in_quarter
                      ? 'text-bg-danger'
                      : 'text-bg-secondary'
                  "
                >
                  {{ translateTrueFalse(person.registered_in_quarter) }}
                </span>
              </li>
              <li class="list-inline-item d-none">
                Enrollment Status Code: {{ person.enroll_status_code }}
              </li>
              <li class="list-inline-item flex-fill w-25">
                <div>Holds</div>
                <span
                  class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1"
                  :class="
                    person.registration_hold_ind
                      ? 'text-bg-danger'
                      : 'text-bg-secondary'
                  "
                >
                  {{ translateTrueFalse(person.registration_hold_ind) }}
                </span>
              </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else class="p-3">
    There are no students found in
    <strong>{{ adviserNetId }}&rsquo;s</strong> caseload.
  </div>
</template>

<script>
import ProfileMini from "@/components/student/profile-mini.vue";
import { translateTrueFalse } from "@/utils/translations";

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
  methods: {
    getScholarshipData: function (person) {
      try {
        return {
          scholarship_type: person.latest_transcript.scholarship_type,
          scholarship_desc: person.latest_transcript.scholarship_desc,
        };
      } catch (err) {
        return {
          scholarship_type: undefined,
          scholarship_desc: undefined,
        };
      }
    },
    getDegreeData: function (person) {
      try {
        return {
          degree_desc: person.latest_degree.degree_status_desc,
        };
      } catch (err) {
        return {
          degree_desc: "NONE",
        };
      }
    },
  },
};
</script>

<style lang="scss">
.table td {
  background: transparent !important;
}
</style>
