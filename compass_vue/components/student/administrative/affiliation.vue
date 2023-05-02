<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Affiliations</axdd-card-heading>
      <!-- need to change the button -->
      <AffiliationAdd :button-type="'button'" :person="person"
        >Add Affiliation</AffiliationAdd
      >
    </template>
    <template #body>
      <div class="table-responsive m-n3">
        <table class="table m-0">
          <thead class="table-light text-muted small">
            <tr>
              <th class="ps-3">Programs</th>
              <th>Cohort</th>
              <th>Active</th>
              <th>Edit</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border border-white">
              <td scope="row" class="ps-3">Trio</td>
              <td></td>
              <td></td>

              <td>
                <AffiliationEdit :button-type="'button'" :person="person">
                  <i class="py-0 bi bi-pencil-square"></i
                ></AffiliationEdit>
                <AffiliationDelete :button-type="'button'" :person="person">
                  <i class="bi bi-trash3"></i>
                </AffiliationDelete>
              </td>
            </tr>
          </tbody>
          <thead class="table-light text-muted small">
            <tr>
              <th class="ps-3">Others</th>
              <th>Cohort</th>
              <th>Active</th>
              <th>Edit</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border border-white">
              <td scope="row" class="ps-3">Brotherhood Initiative Scholar</td>
              <td>2022-2023</td>
              <td>Yes</td>
              <td>
                <AffiliationEdit :button-type="'button'" :person="person">
                  <i class="py-0 bi bi-pencil-square"></i
                ></AffiliationEdit>
                <AffiliationDelete :button-type="'button'" :person="person">
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
import dataMixin from "../../../mixins/data_mixin.js";

import AffiliationAdd from "./affiliation-add.vue";
import AffiliationDelete from "./affiliation-delete.vue";
import AffiliationEdit from "./affiliation-edit.vue";

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
      contacts: {},
      userName: document.body.getAttribute("data-user-netid"),
      userOverride: document.body.getAttribute("data-user-override"),
    };
  },
  created() {
    this.loadStudentContacts();
  },
  methods: {
    loadStudentContacts: function () {
      this.getStudentContacts(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            this.contacts = response.data;
          }
        }
      );
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
}
</style>
