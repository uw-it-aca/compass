<template>
  <div class="row mb-4">
    <h2 class="h6 m-0 fw-bold mb-4">Academic Summary</h2>

    <div
      class="col-xl-3 d-flex flex-column"
      :class="[mq.lgMinus ? 'mb-4' : '']"
    >
      <div
        class="bg-light-beige rounded-3 p-3 border-0 d-flex flex-column flex-fill m-0 small"
      >
        <div class="flex-fill">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">Status</p>
          <ul class="list-unstyled">
            <li>
              <KeyValue
                v-if="person.student.registration_hold_ind"
                class="text-danger"
              >
                <template #key>Holds</template>
                <template #value>Yes</template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Class standing</template>
                <template #value>{{ person.student.class_desc }}</template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Campus</template>
                <template #value>{{ person.student.campus_desc }}</template>
              </KeyValue>
            </li>
          </ul>
        </div>
        <div>
          <KeyValue>
            <template #key
              ><span class="fw-bold">Grade Point Average (GPA)</span></template
            >
            <template #value>{{ person.student.cumulative_gpa }}</template>
          </KeyValue>
        </div>
      </div>
    </div>
    <div
      class="col-xl-3 d-flex flex-column"
      :class="[mq.lgMinus ? 'mb-4' : '']"
    >
      <div
        v-if="person.student.degrees && person.student.degrees.length > 0"
        class="bg-light-beige rounded-3 p-3 border-0 d-flex flex-column flex-fill m-0 small"
      >
        <div class="flex-fill">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">Degrees</p>
          <div>
            <KeyValue
              variant="address"
              v-for="(degree, index) in person.student.degrees"
              :key="index"
            >
              <template #key
                ><span class="text-wrap">
                  {{ degree.degree_desc }}
                </span></template
              >
              <template #value>
                <p class="small" v-if="degree.degree_term">
                  {{ degree.degree_term.quarter_name }}
                  {{ degree.degree_term.year }}
                  ({{ degree.degree_status_desc }})
                </p>
                <p v-else class="small">{{ degree.degree_status_desc }}</p>
              </template>
            </KeyValue>
          </div>
        </div>
      </div>
      <div
        v-if="person.student.degrees && person.student.degrees.length == 0"
        class="bg-light-beige rounded-3 p-3 border-0 d-flex flex-column flex-fill m-0 small"
      >
        <div class="flex-fill">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">Majors</p>
          <!-- changed the formate into keyvalue -->
          <div>
            <KeyValue variant="address">
              <template #key>Current Majors</template>
              <template #value>
                <ul class="list-unstyled">
                  <p
                    v-for="(major, index) in person.student.majors"
                    :key="index"
                  >
                    {{ major.major_abbr_code }}, {{ major.major_name }}
                  </p>
                </ul>
              </template>
            </KeyValue>
          </div>
          <!-- changed the formate into keyvalue -->
          <div>
            <KeyValue variant="address">
              <template #key> Intended Majors (upon admission)</template>
              <template #value>
                <ol>
                  <li v-if="person.student.intended_major1_code">
                    {{ person.student.intended_major1_code }}
                  </li>
                  <li v-if="person.student.intended_major2_code">
                    {{ person.student.intended_major2_code }}
                  </li>
                  <li v-if="person.student.intended_major3_code">
                    {{ person.student.intended_major3_code }}
                  </li>
                </ol>
              </template>
            </KeyValue>
          </div>
        </div>
      </div>
    </div>
    <div
      class="col-xl-3 d-flex flex-column"
      :class="[mq.lgMinus ? 'mb-4' : '']"
    >
      <AffiliationSummary :person="person"></AffiliationSummary>
    </div>
    <div class="col-xl-3 d-flex flex-column">
      <div
        class="bg-light-beige rounded-3 p-3 border-0 d-flex flex-column flex-fill m-0 small"
      >
        <div class="flex-fill">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">Credits</p>
          <ul class="list-unstyled">
            <li>
              <KeyValue>
                <template #key>Total Extension Credits</template>
                <template #value>{{
                  person.student.total_extension_credits
                }}</template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Total Transfer Credits</template>
                <template #value>{{
                  person.student.total_transfer_credits
                }}</template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Total UW Credits</template>
                <template #value>{{
                  person.student.total_uw_credits
                }}</template>
              </KeyValue>
            </li>
          </ul>
        </div>
        <div>
          <KeyValue>
            <template #key><span class="fw-bold">Total Credits</span></template>
            <template #value>{{ person.student.total_credits }}</template>
          </KeyValue>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import KeyValue from "@/components/_common/key-value.vue";
import dataMixin from "@/mixins/data_mixin";
import AffiliationSummary from "@/components/student/affiliation-mini.vue";

import { translateTrueFalse } from "@/utils/translations";

export default {
  inject: ["mq"],
  mixins: [dataMixin],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {
    KeyValue,
    AffiliationSummary,
  },
  setup() {
    return {
      translateTrueFalse,
    };
  },
  data() {
    return {
      testObj: {},
    };
  },
  created() {},
  methods: {},
};
</script>
