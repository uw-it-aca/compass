// active-visits.vue

<template>
  <template v-if="visitsLoaded">
    <visitlist
      :visits="pendingVerification"
      list-title="Active IC Visits"
      @visit-updated="handleVisitUpdated"
    />
    <template v-for="programAreaVisits in byProgramearea">
      <visitlist
        :visits="programAreaVisits"
        :list-title="programAreaVisits[0].program_area"
        @visit-updated="handleVisitUpdated"
      />
    </template>
  </template>
</template>

<script>
import { useICVisitsStore } from "@/stores/ic-visits";
import { getActiveICVisits } from "@/utils/data";
import VisitList from "@/components/ic-dashboard/visit-list.vue";

export default {
  name: "ActiveICVisits",
  setup: function () {
    return {
      getActiveICVisits,
    };
  },
  components: {
    visitlist: VisitList,
  },
  data() {
    return {
      activeVisits: null,
    };
  },
  computed: {
    visitsLoaded() {
      return this.activeVisits !== null;
    },
    activeICVisits() {
      return this.activeVisits;
    },
    pendingVerification() {
      if (this.activeVisits) {
        return this.activeVisits.pending_verification;
      }
    },
    byProgramearea() {
      if (this.activeVisits) {
        return this.activeVisits.by_programarea;
      }
    },
  },
  methods: {
    handleVisitUpdated() {
      this.activeVisits = null;
      this.getActiveICVisits().then((data) => {
        this.activeVisits = data;
      });
    },
  },
  mounted() {
    this.getActiveICVisits().then((data) => {
      this.activeVisits = data;
    });
  },
};
</script>
