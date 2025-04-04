<template>
  <BCard
    class="bg-body-tertiary rounded-3 d-flex flex-fill small"
    border-variant="0"
  >
    <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-3">
      Affiliations
    </div>

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

    <template v-if="affiliations.length">
      <ul class="list-unstyled mb-0">
        <li v-for="(a, index) in affiliations" :key="index" class="mb-1">
          <strong>{{ a.affiliation.name }}</strong
          ><span
            v-for="(c, index2) in a.cohorts"
            :key="index2"
            class="ms-2 text-nowrap"
            >{{ c.start_year }}-{{ c.end_year }}</span
          >
        </li>
      </ul>
    </template>
  </BCard>
</template>

<script>
import KeyValue from "@/components/_common/key-value.vue";
import { getStudentAffiliations } from "@/utils/data";
import { BCard } from "bootstrap-vue-next";

export default {
  components: { BCard, KeyValue },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      getStudentAffiliations,
    };
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
          if (response) {
            this.affiliations = response;
          }
        }
      );
    },
  },
};
</script>
