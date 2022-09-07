<template>
  <div class="row mb-4">
    <h2 class="h6 m-0 fw-bold mb-4">Academic Summary</h2>
    <div class="col-3 d-flex flex-column">
      <div class="card shadow-sm flex-fill">
        <div class="card-body">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">
            Status
          </p>
          <ul class="list-unstyled">
            <li>
              Enrollment Status:
              <template v-if="person.student.registered_in_quarter">
                Registered
              </template>
              <template v-else> Unregistered </template
              >{{ person.student.enrollment_desc }}
            </li>
            <li>Class standing: {{ person.student.class_desc }}</li>
            <li>Campus: {{ person.student.campus_desc }}</li>
          </ul>
        </div>
        <div class="card-footer bg-white">
          <div class="d-flex justify-content-between">
            <span>Grade Point Average (GPA)</span>
            <span>{{ person.student.cumulative_gpa }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="col-3 d-flex flex-column">
      <div class="card p-3 shadow-sm flex-fill">
        <p class="text-uppercase text-dark-beige fs-8 fw-bold">Majors</p>

        <div>
          <p class="small text-uppercase text-muted mb-2">Current Majors</p>
          <ul class="list-unstyled">
            <li v-for="(major, index) in person.student.majors" :key="index">
              {{ major.major_abbr_code }}, {{ major.major_name }}
            </li>
          </ul>
        </div>

        <div>
          <p class="small text-uppercase text-muted mb-2">Intended Majors</p>
          <ul class="list-unstyled">
            <li
              v-for="(intendedMajor, index) in person.student.intended_majors"
              :key="index"
            >
              {{ intendedMajor.major_abbr_code }},
              {{ intendedMajor.major_name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="col-3 d-flex flex-column">
      <div class="card shadow-sm flex-fill">
        <div class="card-body">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">
            Programs
          </p>

          <div>
            <p class="small text-uppercase text-muted mb-2">Special Programs</p>
            <ul class="list-unstyled">
              <li>
                {{ person.student.special_program_code }},
                {{ person.student.special_program_desc }}
              </li>
            </ul>
          </div>

          <div>
            <p class="small text-uppercase text-muted mb-2">Honors</p>
            <ul class="list-unstyled">
              <li>
                {{ person.student.honors_program_code }},
                {{ person.student.honors_program_ind }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="col-3 d-flex flex-column">
      <div class="card shadow-sm flex-fill">
        <div class="card-body">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">
            Credits
          </p>
          <ul class="list-unstyled">
            <li>
              <div class="d-flex justify-content-between">
                <span>Total Extension Credits</span>
                <span>{{ person.student.total_extension_credits }}</span>
              </div>
            </li>
            <li>
              <div class="d-flex justify-content-between">
                <span>Total Transfer Credits</span>
                <span>{{ person.student.total_transfer_credits }}</span>
              </div>
            </li>
            <li>
              <div class="d-flex justify-content-between">
                <span>Total UW Credits</span>
                <span>{{ person.student.total_uw_credits }}</span>
              </div>
            </li>
          </ul>
        </div>
        <div class="card-footer bg-white">
          <div class="d-flex justify-content-between">
            <span>Total Credits</span>
            <span>{{ person.student.total_credits }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Card, CardHeading } from "axdd-components";
import dataMixin from "../../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
  data() {
    return {};
  },
  created() {},
  methods: {},
};
</script>
