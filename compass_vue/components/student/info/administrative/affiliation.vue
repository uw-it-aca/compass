<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Affiliations</axdd-card-heading>
      <!-- need to change the button -->
      <AffiliationAdd
        :button-type="'button'"
        :person="person"
        :affiliations="affiliations"
        :studentAffiliations="studentAffiliations"
        >Add Affiliation</AffiliationAdd
      >
    </template>
    <template #body>
      <div class="table-responsive m-n3">
        <table class="table m-0">
          <thead class="table-light text-muted small">
            <tr>
              <th class="ps-3">Affiliation</th>
              <th>Cohort</th>
              <th>Active</th>
              <th>Edit</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="aff in studentAffiliations" class="border border-white">
              <td scope="row" class="ps-3">{{ aff.affiliation.name }}</td>
              <td scope="row" class="ps-3">
                <div v-for="cohort in aff.cohorts">
                  {{ cohort.start_year }} - {{ cohort.end_year }}
                </div>
              </td>
              <td v-if="aff.actively_advised">
                <i class="py-0 bi bi-check-lg"></i>
              </td>
              <td v-else><i class="py-0 bi bi-x-circle"></i></td>
              <td>
                <AffiliationEdit
                  :button-type="'button'"
                  :person="person"
                  :affiliations="affiliations"
                  :studentAffiliation="aff"
                  :studentAffiliations="studentAffiliations"
                >
                  <i class="py-0 bi bi-pencil-square"></i
                ></AffiliationEdit>
                <AffiliationDelete
                  :button-type="'button'"
                  :person="person"
                  :studentAffiliation="aff"
                  :studentAffiliations="studentAffiliations"
                >
                  <i class="bi bi-trash3"></i>
                </AffiliationDelete>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../../../mixins/data_mixin.js";
import AffiliationAdd from "./affiliation-add.vue";
import AffiliationDelete from "./affiliation-delete.vue";
import AffiliationEdit from "./affiliation-edit.vue";
import { useAffiliationStore } from "../../../../stores/affiliations";

export default {
  mixins: [dataMixin],
  components: {
    AffiliationAdd,
    AffiliationEdit,
    AffiliationDelete,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      studentAffiliations: [],
      affiliations: [],
      userName: document.body.getAttribute("data-user-netid"),
      userOverride: document.body.getAttribute("data-user-override"),
    };
  },
  created() {
    this.loadAffiliationData();
  },
  setup() {
    const storeAffiliations = useAffiliationStore();
    return { storeAffiliations };
  },
  methods: {
    loadAffiliationData() {
      this.getStudentAffiliations(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            this.studentAffiliations = response.data;
          }
        }
      );

      this.storeAffiliations.getAffiliations.then(() => {
        this.affiliations = this.storeAffiliations.affiliations.data;
      });
    },
  },
};
</script>

<style lang="scss" scoped>
tbody {
  td {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
  }

  i.bi-check-lg {
    color: green;
  }
}
</style>
