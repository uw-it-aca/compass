<template>
  <SSidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #navigation>
      <NavMenu :user-roles="userRoles" />

      <QuarterWeek :term-data="termData" />

      <h3
        id="aat_navlink_header"
        class="fs-8 text-white text-opacity-50 text-uppercase"
      >
        Advising Resources
      </h3>
      <ul aria-labelledby="aat_navlink_header" class="list-unstyled mb-5 small">
        <li class="mb-2">
          <BLink
            href="https://sdb.admin.uw.edu/sisAdvising/securid/overview.aspx"
            class="link-light link-underline link-underline-opacity-0 link-underline-opacity-100-hover"
            title="View all cohorts"
          >
            Academic Records (EARS)
          </BLink>
        </li>
        <li class="mb-2">
          <BLink
            href="https://retention.uw.edu"
            class="link-light link-underline link-underline-opacity-0 link-underline-opacity-100-hover"
            title="View all majors"
          >
            Retention Analytics (RAD)
          </BLink>
        </li>
      </ul>
    </template>
    <template #aside>
      <NavMessage v-if="persMsg && persMsg.length > 0" :messages="persMsg" />
      <SProfile
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
      </SProfile>
      <SProfile v-else :user-netid="userName">
        <a :href="signOutUrl" class="text-white">Sign out</a>
      </SProfile>
      <div class="text-end text-white">
        <SColorMode></SColorMode>
      </div>
    </template>
    <template #main>
      <slot name="title">
        <h1 class="visually-hidden">{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer></template>
  </SSidebar>
</template>

<script>
import { BLink } from "bootstrap-vue-next";
import { SColorMode, SSidebar, SProfile } from "solstice-vue";
import QuarterWeek from "@/components/_common/quarter-week.vue";
import NavMenu from "@/components/nav-menu.vue";
import NavMessage from "@/components/nav-message.vue";
import { clearOverride } from "@/utils/data";

export default {
  name: "CompassApp",
  components: {
    BLink,
    NavMenu,
    NavMessage,
    QuarterWeek,
    SSidebar,
    SColorMode,
    SProfile,
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
