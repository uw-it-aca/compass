<template>
  <BCard
    class="shadow-sm rounded- mt-4"
    header-class="p-3 d-flex align-items-center justify-content-between"
    header-bg-variant="transparent"
  >
    <template #header
      ><div class="fs-6 fw-bold">
        Sign-In Data
        <button
          tabindex="0"
          role="button"
          class="btn btn-link m-0 p-0"
          data-bs-toggle="popover"
          data-bs-trigger="focus"
          data-bs-placement="top"
          title="Sign-In Data"
          data-bs-content="Sign in data from UW IdP"
        >
          <i class="bi bi-info-circle-fill"></i>
        </button>
      </div>
    </template>

    <template v-if="analyticsNotFound">
      <p>Sign-in data not found</p>
    </template>
    <template v-else>
      <AnalyticsChart
        v-if="dataReady"
        :data-series="formattedData"
        :show-only-latest="true"
      ></AnalyticsChart>
    </template>
  </BCard>
</template>

<script>
import { Popover } from "bootstrap";
import { BCard } from "bootstrap-vue-next";
import { useAnalyticsStore } from "@/stores/analytics.js";
import AnalyticsChart from "@/components/student/analytics/chart.vue";

export default {
  name: "SignInChart",
  components: {
    BCard,
    AnalyticsChart,
  },
  setup() {
    const storeAnalytics = useAnalyticsStore();
    return { storeAnalytics };
  },
  props: {
    uwnetid: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      rawSigninAnalytics: undefined,
      analyticsNotFound: false,
      dataReady: false,
      currentQuarterColor: "#0732de",
      previousQuarterColors: [
        "#aeafb0",
        "#a1beed",
        "#dec799",
        "#fc6f7d",
        "#6ffc9c",
        "#cb6ffc",
        "#d7fc6f",
        "#a7fcff",
        "#17acff",
      ],
      latestYear: undefined,
      latestQuarter: undefined,
      formattedData: [],
    };
  },
  mounted() {
    // enable popovers everywhere
    // https://getbootstrap.com/docs/5.1/components/popovers/#example-enable-popovers-everywhere
    var popoverTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new Popover(popoverTriggerEl);
    });

    this.loadStudentCourseAnalytics();
  },
  watch: {
    rawSigninAnalytics: function () {
      this.setLatest(this.rawSigninAnalytics);
      this.formatData();
      this.dataReady = true;
    },
  },

  methods: {
    formatData() {
      let formatted_data = [],
        signin_data = this.rawSigninAnalytics;
      for (let year in signin_data) {
        for (let quarter in signin_data[year]) {
          let data_array = Array(10).fill(null);
          for (let week_id in signin_data[year][quarter]) {
            data_array[week_id - 1] = signin_data[year][quarter][week_id];
          }
          let is_latest =
              year == this.latestYear && quarter == this.latestQuarter,
            color = this.getBackgroundColor(is_latest);
          formatted_data.push({
            year: year,
            quarter: quarter,
            label: `${this.capitalizeFirstLetter(quarter)} ${year}`,
            data: data_array,
            backgroundColor: color,
            borderColor: color,
            isLatest: is_latest,
          });
        }
      }
      formatted_data.sort((a, b) => {
        if (a.year == b.year) {
          return (
            this.getQuarterIndex(b.quarter) - this.getQuarterIndex(a.quarter)
          );
        }
        return b.year - a.year;
      });
      this.formattedData = formatted_data;
    },
    getBackgroundColor(is_latest) {
      if (is_latest) {
        return this.currentQuarterColor;
      } else {
        if (this.previousQuarterColors.length === 0) {
          // In case we run out of colors start picking at random
          return (
            "#" +
            ((Math.random() * 0xffffff) << 0).toString(16).padStart(6, "0")
          );
        }
        let color = this.previousQuarterColors.pop();
        return color;
      }
    },
    setLatest(signin_data) {
      let latest_year = 0,
        latest_quarter = 0;
      for (let year in signin_data) {
        for (let quarter in signin_data[year]) {
          if (year > latest_year) {
            latest_year = year;
            latest_quarter = this.getQuarterIndex(quarter);
          } else if (year == latest_year) {
            if (
              this.getQuarterIndex(quarter) >
              this.getQuarterIndex(latest_quarter)
            ) {
              latest_quarter = this.getQuarterIndex(quarter);
            }
          }
        }
      }
      this.latestYear = latest_year;
      this.latestQuarter = this.getQuarterFromIndex(latest_quarter);
    },

    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    getQuarterIndex(quarter) {
      let quarters = ["autumn", "winter", "spring", "summer"];
      return quarters.indexOf(quarter);
    },
    getQuarterFromIndex(index) {
      let quarters = ["autumn", "winter", "spring", "summer"];
      return quarters[index];
    },
    loadStudentCourseAnalytics: function () {
      this.storeAnalytics
        .fetchStudentSigninAnalytics(this.uwnetid)
        .then(() => {
          this.rawSigninAnalytics =
            this.storeAnalytics.signinAnalyticsData[this.uwnetid].data;
        })
        .catch((e) => {
          this.analyticsNotFound = true;
        });
    },
  },
};
</script>
