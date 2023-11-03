// session-expired.vue

<template>
  <div
    v-if="sessionExpired"
    class="small alert alert-danger border-0 mt-3 sticky-top"
    role="alert"
  >
    <strong>Your session has expired.</strong> Refresh the page to start a new
    session.
  </div>
</template>

<script>
export default {
  name: "SessionExpired",
  data() {
    return {
      sessionExpired: false,
    };
  },
  methods: {},
  mounted() {
    // use settimeout to simulate an expired session after 5 seconds
    setTimeout(() => (this.sessionExpired = true), 5000);
  },
};
</script>
