// active-visits.vue

<template>
<visitlist :visits="pendingVerification" list-title="Active IC Visits" />
<template v-for="programAreaVisits in byProgramearea">
  <visitlist :visits="programAreaVisits" :list-title="programAreaVisits[0].program_area" />
  </template>

</template>

<script>
import { useICVisitsStore } from "@/stores/ic-visits";
import VisitList from "@/components/ic-dashboard/visit-list.vue";

export default {
  name: "ActiveICVisits",
  components: {
    visitlist: VisitList,
  },
  data() {
    return {
      icVisitsStore: useICVisitsStore(),
    };
  },
  computed: {
    activeICVisits() {
      console.log(this.icVisitsStore.activeICVisits);
      return this.icVisitsStore.activeICVisits;
    },
    pendingVerification() {
      if(this.icVisitsStore.activeICVisits){
        return this.icVisitsStore.activeICVisits.pending_verification;
      }
    },
    byProgramearea() {
      if(this.icVisitsStore.activeICVisits){
        return this.icVisitsStore.activeICVisits.by_programarea;
      }
    },
  },
};
</script>
