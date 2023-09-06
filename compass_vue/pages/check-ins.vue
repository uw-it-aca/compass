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
import CheckInTableLoading from "@/components/checkin-table-loading.vue";
import CheckInTableDisplay from "@/components/checkin-table-display.vue";

import Layout from "@/layout.vue";
import dataMixin from "@/mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "table-loading": CheckInTableLoading,
    "table-display": CheckInTableDisplay,
  },
  data() {
    return {
      pageTitle: "Contacts",
      isLoading: true,
      contacts: [],
      today: "",
      userNetId: document.body.getAttribute("data-user-override")
        ? document.body.getAttribute("data-user-override")
        : document.body.getAttribute("data-user-netid"),
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
    setTimeout(() => {
      this.loadAdviserContactsList(this.userNetId);
    }, 2000);
  },
};
</script>

<style lang="scss">
.table {
  tbody tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
