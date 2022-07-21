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
              <p>if manager... show all checkins, else, only show checkins assigned to logged in user.</p>
              <table-loading v-if="isLoading"></table-loading>
              <table-display v-else :contacts="contacts"></table-display>
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
  TabsList,
  TabsDisplay,
  TabsItem,
  TabsPanel,
} from "axdd-components";
import SearchStudent from "../components/search-student.vue";
import CheckInTableLoading from "../components/checkin-table-loading.vue";
import CheckInTableDisplay from "../components/checkin-table-display.vue";

import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
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
