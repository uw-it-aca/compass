// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-gray p-4 rounded-3">
            <div class="row">
              <div class="col-3">
                <div class="fw-bold lh-lg">Filter by adviser:</div>
                <div>
                  <search-adviser></search-adviser>
                </div>
              </div>
              <div class="col-6">
                <div class="fw-bold lh-lg">Last updated:</div>
                <div class="h4">Today, {{ getToday() }}</div>
              </div>
              <div class="col-3 border-start ms-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <search-student></search-student>
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
              <axdd-card-heading :level="2"
                >Recent Check-Ins (3 days)</axdd-card-heading
              >
            </template>
            <template #body>
              <axdd-tabs :tabs-id="'checkins'">
                <template #items>
                  <axdd-tab-item
                    :tabs-id="'checkins'"
                    :panel-id="'group'"
                    :active-tab="true"
                    >All</axdd-tab-item
                  >
                  <axdd-tab-item :tabs-id="'checkins'" :panel-id="'mine'"
                    >My Check-ins</axdd-tab-item
                  >
                </template>
                <template #panels>
                  <axdd-tab-panel :panel-id="'group'" :active-panel="true">
                    <table-loading v-if="isLoading"></table-loading>
                    <table-display v-else :persons="persons"></table-display>
                  </axdd-tab-panel>

                  <axdd-tab-panel :panel-id="'mine'">
                    <table-loading v-if="isLoading"></table-loading>
                    <table-display v-else :persons="persons"></table-display>
                  </axdd-tab-panel>
                </template>
              </axdd-tabs>

              <div class="mt-5 text-secondary">No students to meet with.</div>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import {
  Card,
  CardHeading,
  CardAction,
  Tabs,
  TabItem,
  TabPanel,
} from "axdd-components";
import SearchAdviser from "../components/search-adviser.vue";
import SearchStudent from "../components/search-student.vue";
import TableLoading from "../components/table-loading.vue";
import TableDisplay from "../components/table-display.vue";

import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";
import { getToday, getYesterday } from "../helpers/utils";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "search-adviser": SearchAdviser,
    "search-student": SearchStudent,
    "table-loading": TableLoading,
    "table-display": TableDisplay,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-tabs": Tabs,
    "axdd-tab-item": TabItem,
    "axdd-tab-panel": TabPanel,
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
