// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2"
                >Today, {{ getToday() }}</axdd-card-heading
              >
              <axdd-card-action>
                <student-search></student-search>
              </axdd-card-action>
            </template>
            <template #body>
              <table-loading v-if="isLoading"></table-loading>
              <table-display v-else></table-display>
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
      today: "",
    };
  },
  computed: {},
  methods: {
    getToday,
    showResults: function () {
      this.isLoading = false;
    },
  },
  mounted() {
    setTimeout(this.showResults, 4000);
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
