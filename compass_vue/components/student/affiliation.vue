<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Affiliations</axdd-card-heading>
      <!-- need to change the button -->
      <axdd-card-action>
        <AddAffiliation :button-type="'button'" :person="person"
          >Add Affiliation</AddAffiliation
        >
      </axdd-card-action>
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
                <EditAffiliation :button-type="'button'">
                  <i class="bi bi-pencil-square"></i
                ></EditAffiliation>
                <button class="btn py-0">
                  <i class="bi bi-trash3"></i>
                </button>
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
                <button class="btn py-0">
                  <i class="bi bi-pencil-square"></i>
                </button>
                <button class="btn py-0">
                  <i class="bi bi-trash3"></i>
                </button>
              </td>
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
import AddAffiliation from "../add-affiliation.vue.js";
import EditAffiliation from "../edit-affiliation.vue.js";

export default {
  AddAffiliation,
  EditAffiliation,
  mixins: [dataMixin],
  components: {
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
