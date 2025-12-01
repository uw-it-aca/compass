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
              <div class="d-flex justify-content-between align-items-end">
                <div class="fs-6 fw-bold">{{ checkinHeaderText }}</div>
                <div class="text-end">
                  <BDropdown
                    size="sm"
                    class="d-inline-block"
                    :text="dropdownLabel"
                    variant="outline-primary"
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
                </div>
              </div>
            </template>
            <CheckInTableLoading v-if="isLoading" />
            <CheckInTableDisplay
              v-else
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
import { getAdviserCheckIns, savePreferences } from "@/utils/data";
import { formatAdviserName } from "@/utils/formats";
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
      savePreferences,
      formatAdviserName,
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
  computed: {
    dropdownLabel() {
      return "Check-In History (" + this.selectedInterval + " days)";
    },
    checkinHeaderText() {
      let txt = "Recent Check-Ins";
      if (!this.errorResponse && !this.isLoading) {
        if (this.contacts.length === 0) {
          txt = "There are no Check-Ins"
        } else if (this.contacts.length === 1) {
          txt = "There is one Check-In";
        } else {
          txt = "There are " + this.contacts.length + " Check-Ins";
        }
        txt += " for " + this.formatAdviserName(this.adviser);
      }
      return txt += " (" + this.selectedInterval + " days)";
    },
  },
  mounted() {
    this.loadFilterPreferences();
    setTimeout(() => {
      this.loadAdviserCheckInsList();
    }, 500);
  },
  methods: {
    checkInIntervalSelected: function (interval) {
      if (this.selectedInterval !== interval) {
        this.selectedInterval = interval;
        this.loadAdviserCheckInsList();
        this.saveFilterPreferences();
      }
    },
    loadFilterPreferences: function () {
      let user_prefs = window.userPreferences;
      if (user_prefs && user_prefs.checkin_filters) {
        this.selectedInterval = user_prefs.checkin_filters.interval;
      }
    },
    saveFilterPreferences: function () {
      this.savePreferences({
          checkin_filters: {
            interval: this.selectedInterval,
          },
        })
        .then((data) => {
          window.userPreferences.checkin_filters = {
            interval: this.selectedInterval,
          };
        })
        .catch((error) => {
          console.log("Error saving checkin preferences: " + error.data);
        });
    },
    loadAdviserCheckInsList: function () {
      this.errorResponse = null;
      this.isLoading = true;
      this.getAdviserCheckIns(this.adviserNetId, this.selectedInterval)
        .then((data) => {
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
