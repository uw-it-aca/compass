<template>
  <axdd-card v-if="Object.keys(affiliations.group).length || affiliations.external.length">
    <template #heading>
      <axdd-card-heading :level="2">Affiliations</axdd-card-heading>
    </template>
    <template #body>
      <div>
        <div v-if="Object.keys(affiliations.group).length">
          <div v-for="(alist, groupName) in affiliations.group" class="fs-7 text fw-bold text-secondary">
             {{groupName}}

             <div v-for="a in alist">
               {{a.affiliation.name}}
               <ul>
                <li v-for="c in a.cohorts">{{c.start_year}}-{{c.end_year}}</li>
               </ul>
             </div>
          </div>
        </div>
        <div v-if="affiliations.external.length" class="fs-7 text fw-bold text-secondary">
          External
          <div v-for="a in affiliations.external">
            {{a.affiliation.name}}
            <ul>
              <li v-for="c in a.cohorts">{{c.start_year}}-{{c.end_year}}</li>
            </ul>
          </div>
        </div>
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
        affiliations: {'group': {}, 'external': []}
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
  }
};
</script>
