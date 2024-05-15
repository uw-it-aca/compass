<template>
  <!-- layout.vue: this is where you override the layout -->
  <axdd-sidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #profile>
      <axdd-profile
        v-if="userName != userOverride"
        :user-netid="userName"
        :user-override="userOverride"
      >
        <button
          class="btn btn-link btn-sm text-danger p-0 m-0 border-0"
          value="Clear override"
          @click="clearUserOverride()"
        >
          Clear
        </button>
      </axdd-profile>
      <axdd-profile v-else :user-netid="userName">
        <a :href="signOutUrl" class="text-white">Sign out</a>
      </axdd-profile>
    </template>
    <template #navigation>
      <NavMenu :user-roles="userRoles" />
    </template>
    <template #aside>
      <QuarterWeek :term-data="termData" />
      <NavMessage v-if="persMsg && persMsg.length > 0" :messages="persMsg" />
    </template>
    <template #main>
      <slot name="title">
        <h1 class="fw-bold">{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer></template>
  </axdd-sidebar>
</template>

<script>
import QuarterWeek from "@/components/_common/quarter-week.vue";
import NavMenu from "@/components/nav-menu.vue";
import NavMessage from "@/components/nav-message.vue";
import { clearOverride } from "@/utils/data";

export default {
  name: "CompassApp",
  components: {
    NavMenu,
    NavMessage,
    QuarterWeek,
  },
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  setup() {
    return {
      clearOverride,
    };
  },
  data() {
    return {
      // minimum application setup overrides
      appName: "Compass",
      appRootUrl: "/",
      userName: document.body.getAttribute("data-user-netid"),
      userOverride: document.body.getAttribute("data-user-override"),
      signOutUrl: document.body.getAttribute("data-signout-url"),
      userRoles: document.body.getAttribute("data-user-role").split(","),
      // automatically set year
      currentYear: new Date().getFullYear(),

      // get term_data from window context
      termData: window.term_data,

      // get persistent messages
      persMsg: window.persistent_msgs,
    };
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
  methods: {
    clearUserOverride: function () {
      // setup() exposed properties can be accessed on `this`
      this.clearOverride().then(() => {
        window.location.href = "/support";
      });
    },
  },
};
</script>
