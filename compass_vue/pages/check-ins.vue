<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-light p-3 rounded-3">
            <div class="row">
              <div class="col-xl-4 me-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <search-student></search-student>
                </div>
              </div>
              <div class="col-xl-8">&nbsp;</div>
            </div>
          </div>
        </div>
      </div>

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
import SearchStudent from "@/components/search-student.vue";
import CheckInTableLoading from "@/components/checkin-table-loading.vue";
import CheckInTableDisplay from "@/components/checkin-table-display.vue";
import Layout from "@/layout.vue";
import { getAdviserCheckIns } from "@/utils/data";

export default {
  components: {
    layout: Layout,
    "search-student": SearchStudent,
    "table-loading": CheckInTableLoading,
    "table-display": CheckInTableDisplay,
  },
  setup() {
    return {
      getAdviserCheckIns,
    };
  },
  data() {
    return {
      pageTitle: "Check-Ins",
      isLoading: true,
      contacts: [],
      today: "",
      adviserNetId: this.$route.params.id
        ? this.$route.params.id
        : document.body.getAttribute("data-user-override")
        ? document.body.getAttribute("data-user-override")
        : document.body.getAttribute("data-user-netid"),
    };
  },
  computed: {},
  methods: {
    loadAdviserCheckInsList: function (netid) {
      let _this = this;
      // setup() exposed properties can be accessed on `this`
      this.getAdviserCheckIns(netid).then((response) => {
        if (response.data) {
          _this.contacts = response.data;
          _this.isLoading = false;
        }
      });
    },
  },
  mounted() {
    setTimeout(() => {
      this.loadAdviserCheckInsList(this.adviserNetId);
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
