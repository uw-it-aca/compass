// about.vue

<template>
  <layout
    v-if="person.display_name !== undefined"
    :page-title="person.display_name"
  >
    <template #title>
      <h1 v-if="$route.params.id" class="visually-hidden">
        {{ person.display_name }}
      </h1>
      <h1 v-else>Student</h1>
    </template>
    <template #content>
      <div v-if="$route.params.id">
        <div class="row my-4">
          <div class="col">
            <div class="bg-gray p-4 rounded-3">
              <div class="row">
                <div class="col-lg-6 pe-4 d-flex small">
                  <div>
                    <div
                      :class="priorityRing"
                      class="rounded-circle border border-4"
                      style="width: 140px"
                    >
                      <img
                        v-if="person.gender === 'F'"
                        src="https://randomuser.me/api/portraits/women/4.jpg"
                        class="
                          img-fluid
                          rounded-circle
                          border border-light border-3
                        "
                      />
                      <img
                        v-else
                        src="https://randomuser.me/api/portraits/men/4.jpg"
                        class="
                          img-fluid
                          rounded-circle
                          border border-gray border-3
                        "
                      />
                    </div>
                  </div>
                  <div class="flex-fill ps-4 mb-4">
                    <div class="h3 text-dark axdd-font-encode-sans">
                      <template v-if="person.preferred_first_name">
                        {{ person.preferred_first_name }}
                      </template>
                      <template v-else> {{ person.first_name }} </template
                      >&nbsp;
                      <template v-if="person.preferred_surname">
                        {{ person.preferred_surname }}
                      </template>
                      <template v-else>
                        {{ person.surname }}
                      </template>
                    </div>
                    <div class="h5">
                      {{ person.student.student_number }},
                      <small>{{ person.uwnetid }}</small>
                    </div>
                    <p>
                      <span
                        class="
                          badge
                          rounded-pill
                          border border-muted
                          text-dark
                          me-1
                        "
                        >{{ person.gender }}</span
                      >
                      <span
                        class="badge rounded-pill border border-muted text-dark"
                      >
                        {{ person.pronouns }}
                      </span>
                    </p>
                    <div v-if="person.student.sports.length > 0">
                      <i class="bi bi-trophy-fill text-purple"></i> Sport:
                      <span
                        v-for="(sport, index) in person.student.sports"
                        :key="sport.code"
                      >
                        {{ sport.sport_code }}
                        <span v-if="index + 1 < person.student.sports.length"
                          >,
                        </span>
                      </span>
                    </div>
                  </div>
                </div>
                <div class="col-6 col-lg-3 px-4 small">
                  <ul class="list-unstyled m-0">
                    <li>
                      Preferred name: {{ person.preferred_first_name }}
                      {{ person.preferred_middle_name }}
                      {{ person.preferred_last_name }}
                    </li>
                    <li>
                      Ethnicity: {{ person.student.assigned_ethnic_desc }}
                    </li>
                    <li>Citizenship: {{ person.student.resident_desc }}</li>
                    <li>DOB: {{ person.student.birthdate }}</li>
                  </ul>
                </div>
                <div class="col-6 col-lg-3 ps-4 small">
                  <ul class="list-unstyled m-0">
                    <li>UW Email: {{ person.student.student_email }}</li>
                    <li>Personal email: {{ person.student.personal_email }}</li>
                    <li>
                      Local Phone: {{ person.student.local_phone_number }}
                    </li>
                    <li class="mt-2">
                      Perm Address:<br />
                      {{ person.student.perm_addr_line1 }}<br />
                      {{ person.student.perm_addr_line2 }}<br />
                      {{ person.student.perm_addr_city }},
                      {{ person.student.perm_addr_state }}
                      {{ person.student.perm_addr_5digit_zip }}-{{
                        person.student.perm_addr_4digit_zip
                      }}, {{ person.student.perm_addr_country }}
                    </li>
                    <li class="mt-2">
                      Local Address: tbd<br />
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-xl-9">
            <StudentContact></StudentContact>
            <StudentSchedule></StudentSchedule>
            <StudentHistory :person="person"></StudentHistory>
          </div>
          <div class="col-xl-3">
            <StudentAdviser
              v-for="adviser in person.student.advisers"
              :key="adviser.id"
              :person="adviser"
            ></StudentAdviser>
            <StudentPrograms :person="person"></StudentPrograms>
            <StudentAcademics :person="person"></StudentAcademics>
          </div>
        </div>
      </div>
      <div v-else>No student</div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";
import StudentContact from "../components/student/contact.vue";
import StudentSchedule from "../components/student/schedule.vue";
import StudentHistory from "../components/student/history.vue";
import StudentAdviser from "../components/student/adviser.vue";
import StudentPrograms from "../components/student/programs.vue";
import StudentAcademics from "../components/student/academics.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    StudentContact,
    StudentSchedule,
    StudentHistory,
    StudentAdviser,
    StudentPrograms,
    StudentAcademics,
  },
  created: function () {
    this.loadStudent(this.$route.params.id);
  },
  data() {
    return {
      person: {},
    };
  },
  computed: {
    studentAddress: function () {
      let addr = "";
      if (this.student.perm_addr_line1)
        addr += this.student.perm_addr_line1 + " ";
      if (this.student.perm_addr_line2)
        addr += this.student.perm_addr_line2 + " ";
      if (this.student.perm_addr_city) addr += this.student.perm_addr_city;
      if (this.student.perm_addr_state)
        addr += ", " + this.student.perm_addr_state;
      if (this.student.perm_addr_line1)
        addr += " " + this.student.perm_addr_postal_code;
      if (addr) return addr;
      else return "N/A";
    },
  },
  methods: {
    loadStudent: function (studentNumber) {
      let _this = this;
      this.getStudentDetail(studentNumber).then((response) => {
        if (response.data) {
          _this.person = response.data;
        }
      });
    },
  },
};
</script>

<style lang="scss">
.table {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
