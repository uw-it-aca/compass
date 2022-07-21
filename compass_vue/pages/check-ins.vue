<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2"
                >Recent Check-Ins (3 days)</axdd-card-heading
              >
            </template>
            <template #body>
              <axdd-tabs-list :tabs-id="'checkins'">
                <template #items>
                  <axdd-tabs-item
                    :tabs-id="'checkins'"
                    :panel-id="'group'"
                    :active-tab="true"
                    >All</axdd-tabs-item
                  >
                  <axdd-tabs-item :tabs-id="'checkins'" :panel-id="'mine'"
                    >My Check-ins</axdd-tabs-item
                  >
                </template>
              </axdd-tabs-list>
              <axdd-tabs-display :tabs-id="'checkins'">
                <template #panels>
                  <axdd-tabs-panel :panel-id="'group'" :active-panel="true">
                    <table-loading v-if="isLoading"></table-loading>
                    <table-display v-else :contacts="contacts"></table-display>
                  </axdd-tabs-panel>

                  <axdd-tabs-panel :panel-id="'mine'">
                    <table-loading v-if="isLoading"></table-loading>
                    <table-display v-else :contacts="contacts"></table-display>
                  </axdd-tabs-panel>
                </template>
              </axdd-tabs-display>

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
  TabsList,
  TabsDisplay,
  TabsItem,
  TabsPanel,
} from "axdd-components";
import SearchAdviser from "../components/search-adviser.vue";
import SearchStudent from "../components/search-student.vue";
import CheckInTableLoading from "../components/checkin-table-loading.vue";
import CheckInTableDisplay from "../components/checkin-table-display.vue";

import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";
import { getToday, getYesterday } from "../helpers/utils";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "search-adviser": SearchAdviser,
    "search-student": SearchStudent,
    "table-loading": CheckInTableLoading,
    "table-display": CheckInTableDisplay,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
  },
  data() {
    return {
      pageTitle: "Contacts",
      isLoading: true,
      contacts: [],
      today: "",
      userNetId: document.body.getAttribute("data-user-netid"),
    };
  },
  computed: {},
  methods: {
    getToday,
    loadAdviserContactsList: function (adviserNetId) {
      let _this = this;
      this.getAdviserContacts(adviserNetId).then((response) => {
        if (response.data) {
          _this.contacts = response.data;
          _this.isLoading = false;
        }
      });
    },
  },
  mounted() {
    this.loadAdviserContactsList(this.userNetId);
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
