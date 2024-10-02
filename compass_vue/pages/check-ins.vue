<template>
  <Layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">

          <BCard class="bg-body-tertiary rounded-3" border-variant="0">
            <div class="row">
              <div class="col-xl-4 me-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <SearchStudent />
                </div>
              </div>
              <div class="col-xl-8">&nbsp;</div>
            </div>
          </BCard>

        </div>
      </div>

      <div class="row my-4">
        <div class="col">
          <BCard
            class="shadow-sm rounded-3"
            header-class="p-3"
            header="Default"
          >
            <template #header> Recent Check-Ins (3 days) </template>
            <CheckInTableLoading v-if="isLoading" />
            <CheckInTableDisplay v-else :contacts="contacts" />
          </BCard>
        </div>
      </div>
    </template>
  </Layout>
</template>

<script>
import SearchStudent from "@/components/search-student.vue";
import CheckInTableLoading from "@/components/checkin-table-loading.vue";
import CheckInTableDisplay from "@/components/checkin-table-display.vue";
import Layout from "@/layout.vue";
import { getAdviserCheckIns } from "@/utils/data";

import { BCard } from "bootstrap-vue-next";

export default {
  components: {
    BCard,
    Layout,
    SearchStudent,
    CheckInTableLoading,
    CheckInTableDisplay,
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
