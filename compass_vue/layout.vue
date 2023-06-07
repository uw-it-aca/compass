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
      <NavMessage />
    </template>
    <template #main>
      <div
        v-if="persMsg && persMsg.length > 0"
        class="sticky-top alert alert-purple mt-3 border-0 small"
        role="alert"
      >
        <ul class="list-unstyled m-0">
          <li v-for="(msg, index) in persMsg" :key="index" v-html="msg"></li>
        </ul>
      </div>

      <slot name="title">
        <h1 class="visually-hidden">{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
  </axdd-sidebar>
</template>

<script>
import QuarterWeek from "./components/_common/quarter-week.vue";
import NavMenu from "./components/nav-menu.vue";
import NavMessage from "./components/nav-message.vue";
import dataMixin from "./mixins/data_mixin.js";

export default {
  name: "CompassApp",
  mixins: [dataMixin],
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
      this.clearOverride().then(() => {
        window.location.href = "/support";
      });
    },
  },
};
</script>
