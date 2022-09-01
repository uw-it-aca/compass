<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Academics</axdd-card-heading>
    </template>
    <template #body>
      <div class="d-flex justify-content-between">
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
          <li>GPA: {{ person.student.cumulative_gpa }}</li>
          <li>
            Current Majors:
            <ul>
              <li v-for="(major, index) in person.student.majors" :key="index">
                {{ major.major_abbr_code }}, {{ major.major_name }}
              </li>
            </ul>
          </li>
        </ul>

        <ul class="list-unstyled">
          <li>
            Desired Majors (upon admission):
            <ul>
              <li
                v-for="(intendedMajor, index) in person.student.intended_majors"
                :key="index"
              >
                {{ intendedMajor.major_abbr_code }},
                {{ intendedMajor.major_name }}
              </li>
            </ul>
          </li>
        </ul>

        <ul class="list-unstyled">
          <li>Total Credits: {{ person.student.total_credits }}</li>
          <li>Total UW Credits: {{ person.student.total_uw_credits }}</li>
          <li>
            Total Deductible Credits:
            {{ person.student.total_deductible_credits }}
          </li>
          <li>
            Total Extension Credits:
            {{ person.student.total_extension_credits }}
          </li>
          <li>
            Total Non-Graded Credits:
            {{ person.student.total_non_graded_credits }}
          </li>
          <li>
            Total Registered Credits:
            {{ person.student.total_registered_credits }}
          </li>
          <li>
            Total Transfer Credits:
            {{ person.student.total_transfer_credits }}
          </li>
          <li>
            Total Lower Division Transfer Credits:
            {{ person.student.total_lower_div_transfer_credits }}
          </li>
          <li>
            Total Upper Division Transfer Credits:
            {{ person.student.total_upper_div_transfer_credits }}
          </li>
        </ul>
      </div>
    </template>
  </axdd-card>
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
