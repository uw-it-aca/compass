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
        @affiliationsUpdated="loadAffiliationData()"
        ><i class="bi bi-people-fill text-dark me-2"></i>Add new
        affiliation</AffiliationAdd
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
              <th>&nbsp;</th>
            </tr>
          </thead>
          <tbody v-if="studentAffiliations.length !== 0">
            <tr
              v-for="(aff, index) in studentAffiliations"
              :key="index"
              class="border border-white"
            >
              <td scope="row" class="ps-3">{{ aff.affiliation.name }}</td>
              <td scope="row" class="ps-3">
                <div v-for="(cohort, index) in aff.cohorts" :key="index">
                  {{ cohort.start_year }} - {{ cohort.end_year }}
                </div>
              </td>
              <td v-if="aff.actively_advised">
                <i class="py-0 bi bi-check-lg"></i>
              </td>
              <td v-else><i class="py-0 bi bi-x-circle"></i></td>
              <td class="text-end">
                <AffiliationEdit
                  :button-type="'button'"
                  :person="person"
                  :affiliations="affiliations"
                  :studentAffiliation="aff"
                  :studentAffiliations="studentAffiliations"
                >
                  <i class="py-0 bi bi-pencil me-2"></i>Edit</AffiliationEdit
                >
                <AffiliationDelete
                  :button-type="'button'"
                  :person="person"
                  :studentAffiliation="aff"
                  :studentAffiliations="studentAffiliations"
                >
                  <i class="bi bi-trash me-2"></i>Delete
                </AffiliationDelete>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <td class="ps-3" colspan="4">no affiliations for this student</td>
          </tbody>
        </table>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import AffiliationAdd from "@/components/student/administrative/affiliation-add.vue";
import AffiliationDelete from "@/components/student/administrative/affiliation-delete.vue";
import AffiliationEdit from "@/components/student/administrative/affiliation-edit.vue";
import { useAffiliationStore } from "@/stores/affiliations";
import { getStudentAffiliations } from "@/utils/data";

export default {
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
  setup() {
    const storeAffiliations = useAffiliationStore();
    return { storeAffiliations, getStudentAffiliations };
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
  methods: {
    loadAffiliationData() {
      this.getStudentAffiliations(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            this.studentAffiliations = response.data;
          }
        }
      );

      this.storeAffiliations.fetchAffiliations.then(() => {
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
