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

      <h3 id="aat_navlink_header" class="fs-7 text-uppercase text-white">
        Advising Resources
      </h3>
      <ul aria-labelledby="aat_navlink_header" class="list-unstyled small mb-5">
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

      <div class="d-flex justify-content-between">
        <!-- user comp here -->
        <SUser
          :user-netid="userName"
          :user-override="userOverride !== userName ? userOverride : null"
        >
          <template v-if="userOverride !== userName">
            Welcome back, {{ userOverride }}!
          </template>
          <template v-else> Welcome back, {{ userName }}! </template>
          <template #action>
            <a
              v-if="userOverride !== userName"
              role="button"
              class="link-quiet-danger"
              @click="clearUserOverride()"
              ><i class="bi bi-x-circle me-2"></i>Clear override</a
            >

            <a v-else :href="signOutUrl" class="link-quiet-danger"
              ><i class="bi bi-box-arrow-left me-2"></i>Sign out</a
            >
          </template>
        </SUser>
        <SColorMode color-class="text-white" class="ms-2" />
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
  import { SColorMode, SSidebar, SProfile, SUser } from "solstice-vue";
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
      SUser,
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
