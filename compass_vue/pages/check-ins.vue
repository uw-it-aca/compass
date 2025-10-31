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
            header-bg-variant="transparent"
            header-class="p-3"
            body-class="p-0"
          >
            <template #header>
              <div class="fs-6 fw-bold">
                Recent Check-Ins
                <span v-if="!isLoading && !errorResponse">
                  for {{ adviser.display_name }}
                </span>
                ({{ selectedInterval }} days)
              </div>
              <BDropdown
                size="sm"
                variant="outline-primary"
                text="Check-In History"
                class=""
                toggle-class="rounded-2"
              >
                <BDropdownItemButton
                  v-for="(interval, index) in checkInIntervals"
                  :key="index"
                  :value="interval"
                  @click.prevent="checkInIntervalSelected(interval)"
                  >{{ interval }}&nbsp;days
                </BDropdownItemButton>
              </BDropdown>
            </template>
            <CheckInTableLoading v-if="isLoading" />
            <CheckInTableDisplay v-else
              :contacts="contacts"
              :adviser="adviser"
              :error="errorResponse"
            />
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

import { BCard, BDropdown, BDropdownItemButton } from "bootstrap-vue-next";

export default {
  components: {
    BCard,
    BDropdown,
    BDropdownItemButton,
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
      checkInIntervals: ["3", "7", "14", "30", "60", "90"],
      selectedInterval: "3",
      contacts: [],
      adviser:  null,
      today: "",
      adviserNetId: this.$route.params.id
        ? this.$route.params.id
        : document.body.getAttribute("data-user-override")
          ? document.body.getAttribute("data-user-override")
          : document.body.getAttribute("data-user-netid"),
      errorResponse: null,
    };
  },
  mounted() {
    setTimeout(() => {
      this.loadAdviserCheckInsList();
    }, 2000);
  },
  methods: {
    checkInIntervalSelected: function (interval) {
      if (this.selectedInterval !== interval) {
        this.selectedInterval = interval;
        this.loadAdviserCheckInsList();
      }
    },
    loadAdviserCheckInsList: function () {
      this.errorResponse = null;
      this.isLoading = true;
      this.getAdviserCheckIns(this.adviserNetId, this.selectedInterval)
        .then((data) => {
          this.errorResponse = null;
          this.adviser = data.adviser;
          this.contacts = data.contacts;
        })
        .catch((error) => {
          this.errorResponse = error.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
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
