<template>
  <div v-if="persons.length > 0" class="table-responsive m-n3">
    <table class="table m-0">
      <thead class="table-light text-muted small">
        <tr>
          <th scope="col" style="width: 34%" class="ps-3">Student</th>
          <th scope="col">Class</th>
          <th scope="col">Campus</th>
          <th scope="col" style="width: 45%" class="text-nowrap">Status</th>
        </tr>
      </thead>
      <tbody>
        <Pagination
          :itemCount="persons.length"
          :itemsPerPage="itemsPerPage"
          :currentPage="currentPage"
          @changePage="changePage"
        >
          <!-- MARK: add paginated template as a slot -->
          <tr v-for="(person, index) in displayedItems" :key="index">
            <td class="ps-3">
              <profile-mini :person="person"></profile-mini>
            </td>
            <td class="small">{{ person.student.class_desc }}</td>
            <td class="small">{{ person.student.campus_desc }}</td>
            <td class="small">
              <ul class="list-inline d-flex m-0">
                <li class="list-inline-item d-none">
                  Special Program:
                  <!-- show N/A when student isn't in any special program -->

                  <span
                    v-if="person.student.special_program_code === '0'"
                    class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1 text-bg-secondary"
                  >
                    N/A</span
                  >
                  <span v-else class="badge text-bg-success">
                    {{ person.student.special_program_code }},
                    {{ person.student.special_program_desc }}
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
                  <div>Scholarship</div>
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
                      !person.student.registered_in_quarter
                        ? 'text-bg-danger'
                        : 'text-bg-secondary'
                    "
                  >
                    {{
                      translateTrueFalse(person.student.registered_in_quarter)
                    }}
                  </span>
                </li>
                <li class="list-inline-item d-none">
                  Enrollment Status Code:
                  {{ person.student.enroll_status_code }}
                </li>
                <li class="list-inline-item flex-fill w-25">
                  <div>Holds</div>
                  <span
                    class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1"
                    :class="
                      person.student.registration_hold_ind
                        ? 'text-bg-danger'
                        : 'text-bg-secondary'
                    "
                  >
                    {{
                      translateTrueFalse(person.student.registration_hold_ind)
                    }}
                  </span>
                </li>
              </ul>
            </td>
          </tr>
          <!-- END slot -->
        </Pagination>
      </tbody>
    </table>
  </div>
  <div v-else>no students in {{ adviserNetId }}'s caseload</div>
</template>

<script>
import { ref, computed } from "vue";
import ProfileMini from "@/components/student/profile-mini.vue";
import Pagination from "@/components/_solstice/pagination.vue";
import { translateTrueFalse } from "@/utils/translations";

export default {
  components: {
    "profile-mini": ProfileMini,
    Pagination,
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
  setup(props) {
    // basic setup for pagination component
    const currentPage = ref(1);
    const itemsPerPage = ref(1); // set ref to number to be shown

    const displayedItems = computed(() => {
      const startIndex = (currentPage.value - 1) * itemsPerPage.value;
      const endIndex = startIndex + itemsPerPage.value;
      // return sliced data object to be paginated
      return props.persons.slice(startIndex, endIndex);
    });

    //pass this function to pagination component
    function changePage(pageNumber) {
      currentPage.value = pageNumber;
    }

    return {
      currentPage,
      displayedItems,
      itemsPerPage,
      changePage,
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
          scholarship_type: person.student.transcripts[0].scholarship_type,
          scholarship_desc: person.student.transcripts[0].scholarship_desc,
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
          degree_desc: person.student.degrees[0].degree_status_desc,
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
