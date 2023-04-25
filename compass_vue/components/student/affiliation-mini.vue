<template>
  <axdd-card
    v-if="
      Object.keys(affiliations.group).length || affiliations.external.length
    "
  >
    <template #heading>
      <axdd-card-heading :level="2">Affiliations</axdd-card-heading>
    </template>
    <template #body>
      <div v-if="Object.keys(affiliations.group).length">
        <template
          v-for="(alist, groupName, index) in affiliations.group"
          :key="index"
        >
          <div class="mb-2 fs-8 fw-bold text-uppercase">{{ groupName }}</div>
          <ul class="list-unstyled">
            <li
              v-for="(a, index) in alist"
              :key="index"
              class="d-flex justify-content-between"
            >
              <span>{{ a.affiliation.name }}</span>
              <span
                v-for="(c, index) in a.cohorts"
                :key="index"
                class="text-muted"
              >
                {{ c.start_year }}-{{ c.end_year }}
              </span>
            </li>
          </ul>
        </template>
      </div>

      <div v-if="affiliations.external.length">
        <div class="mb-2 fs-8 fw-bold text-uppercase">Other</div>
        <ul class="list-unstyled">
          <li
            v-for="(a, index) in affiliations.external"
            :key="index"
            class="d-flex justify-content-between"
          >
            <span>{{ a.affiliation.name }}</span>
            <span
              v-for="(c, index) in a.cohorts"
              :key="index"
              class="text-muted"
            >
              {{ c.start_year }}-{{ c.end_year }}
            </span>
          </li>
        </ul>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {},
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      affiliations: { group: {}, external: [] },
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
