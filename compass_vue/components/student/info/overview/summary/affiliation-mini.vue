<template>
  <div
    class="bg-light-beige rounded-3 p-3 border-0 d-flex flex-column flex-fill m-0 small"
  >
    <div class="flex-fill">
      <p class="text-uppercase text-dark-beige fs-8 fw-bold">Affiliations</p>

      <KeyValue>
        <template #key> Special Programs </template>
        <template #value>
          <ul class="list-unstyled">
            <li>
              {{ person.student.special_program_code }} -
              {{ person.student.special_program_desc }}
            </li>
          </ul>
        </template>
      </KeyValue>

      <div v-if="affiliations.length">
        <ul class="list-unstyled mb-0">
          <li v-for="(a, index) in affiliations" :key="index" class="mb-1">
            <strong>{{ a.affiliation.name }}</strong
            ><span
              v-for="(c, index) in a.cohorts"
              :key="index"
              class="ms-2 text-nowrap"
              >{{ c.start_year }}-{{ c.end_year }}</span
            >
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import dataMixin from "../../../../../mixins/data_mixin.js";
import KeyValue from "../../../../../components/_common/key-value.vue";

export default {
  mixins: [dataMixin],
  components: { KeyValue },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      affiliations: [],
    };
  },
  created() {
    this.loadStudentAffiliations();
  },
  methods: {
    loadStudentAffiliations: function () {
      this.getStudentAffiliations(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            this.affiliations = response.data;
          }
        }
      );
    },
  },
};
</script>
