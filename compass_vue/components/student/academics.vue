<template>
  <div class="row mb-4">
    <h2 class="h6 m-0 fw-bold mb-4">Academic Summary</h2>
    <div class="col-xl-3">
      <div class="alert alert-gray d-flex flex-column flex-fill m-0 small">
        <div class="flex-fill">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">Status</p>
          <ul class="list-unstyled">
            <li>
              <KeyValue>
                <template #key>Enrollment Status</template>
                <template #value>
                  <template v-if="person.student.registered_in_quarter">
                    Registered
                  </template>
                  <template v-else> Unregistered </template
                  >{{ person.student.enrollment_desc }}
                </template>
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
    <div class="col-xl-3">
      <div class="alert alert-gray d-flex flex-column flex-fill m-0 small">
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
                  <li v-if="person.student.intended_major1_code">
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
    <div class="col-xl-3">
      <div class="alert alert-gray d-flex flex-column flex-fill m-0 small">
        <div class="flex-fill">
          <p class="text-uppercase text-dark-beige fs-8 fw-bold">Programs</p>

          <div>
            <KeyValue>
              <template #key> Special Programs </template>
              <template #value>
                <ul class="list-unstyled">
                  <!-- show N/A when student isn't in any special program -->
                  <span v-if="person.student.special_program_code === '0'">
                    N/A</span
                  >
                  <span v-else>
                    <li>
                      {{ person.student.special_program_code }},
                      {{ person.student.special_program_desc }}
                    </li>
                  </span>
                </ul>
              </template>
            </KeyValue>
          </div>
          <!-- show N/A when student isn't in any honors program -->
          <div>
            <KeyValue>
              <template #key> Honors </template>
              <template #value>
                <ul class="list-unstyled">
                  <span v-if="person.student.honors_program_code === '0'"
                    >N/A</span
                  >
                  <span v-else>
                    <li>
                      {{ person.student.honors_program_code }},
                      {{ person.student.honors_program_ind }}
                    </li></span
                  >
                </ul>
              </template>
            </KeyValue>
          </div>
        </div>
      </div>
    </div>
    <div class="col-xl-3">
      <div class="alert alert-gray d-flex flex-column flex-fill m-0 small">
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
import { Card, CardHeading } from "axdd-components";
import KeyValue from "../../components/_common/key-value.vue";
import dataMixin from "../../mixins/data_mixin.js";

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
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    KeyValue,
  },
  data() {
    return {};
  },
  created() {},
  methods: {},
};
</script>
