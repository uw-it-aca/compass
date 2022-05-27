// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col">
          <div class="bg-gray p-4 rounded-3">
            <div class="row">
              <div class="col d-flex justify-content-between">
                <div classw="w-50">Today, {{ getToday() }}</div>
                <div>
                  <student-search></student-search>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2">Recent contacts</axdd-card-heading>
            </template>
            <template #body>
              <table-loading v-if="isLoading"></table-loading>
              <table-display v-else :persons="persons"></table-display>
              <div class="mt-5 text-secondary">No students to meet with.</div>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import { Card, CardHeading, CardAction } from "axdd-components";
import StudentSearch from "../components/student-search.vue";
import TableLoading from "../components/table-loading.vue";
import TableDisplay from "../components/table-display.vue";

import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";
import { getToday, getYesterday } from "../helpers/utils";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "student-search": StudentSearch,

    "table-loading": TableLoading,
    "table-display": TableDisplay,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-card-action": CardAction,
  },
  data() {
    return {
      pageTitle: "Contacts",
      isLoading: true,
      persons: [],
      today: "",
    };
  },
  computed: {},
  methods: {
    getToday,
    loadStudentList: function (studentNumber) {
      let _this = this;
      this.getStudentList().then((response) => {
        if (response.data) {
          _this.persons = response.data;
          _this.isLoading = false;
        }
      });
    },
  },
  mounted() {
    //this.loadStudentList()
    setTimeout(this.loadStudentList, 2000);
  },
};
</script>

<style lang="scss">
.table {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
