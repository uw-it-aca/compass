<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Affiliations</axdd-card-heading>
      <!-- need to change the button -->
      <axdd-card-action>
        <EditAffiliation
          :button-type="'button'"
          :person="person"
          @contactUpdated="loadStudentContacts()"
          >Record new contact</EditAffiliation
        >
      </axdd-card-action>
    </template>
    <template #body>
      <div class="table-responsive m-n3">
        <table class="table m-0">
          <thead class="table-light text-muted small">
            <tr>
              <th class="ps-3">Type</th>
              <th colspan="2">Detials</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td scope="row" class="ps-3" style="width: 25%">Cohort</td>
              <td colspan="2">
                <span
                  class="badge rounded-pill alert alert-dark-purple border-0 px-2 py-1 m-0 me-1"
                  >2022-2023</span
                >
              </td>
            </tr>
            <tr>
              <td scope="row" class="ps-3" style="width: 25%">Program</td>
              <td colspan="2">
                <span
                  class="badge rounded-pill alert alert-dark-purple border-0 px-2 py-1 m-0 me-1"
                  >CHAMPION</span
                >
              </td>
            </tr>
            <tr>
              <td scope="row" class="ps-3" style="width: 25%">Affiliations</td>
              <td colspan="2">
                <li
                  class="badge rounded-pill alert alert-dark-beige border-0 px-2 py-1 mb-0 me-1"
                >
                  EIO
                </li>
              </td>
            </tr>
            <tr>
              <td scope="row" class="ps-3" style="width: 25%">Notes</td>
              <td style="width: 20%">Date</td>
              <td>Notes</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";
import { Card, CardHeading, CardAction } from "axdd-components";
import EditAffiliation from "../edit-affiliation.vue";

export default {
  mixins: [dataMixin],
  components: {
    EditAffiliation,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-card-action": CardAction,
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
