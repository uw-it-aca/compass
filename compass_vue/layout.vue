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
        :user-netid="userName + ' (' + userRoles + ')'"
        :signout-url="signOutUrl"
      ></axdd-profile>
    </template>
    <template #navigation>
      <NavMenu :user-roles="userRoles" />
    </template>
    <template #aside>
      <NavMessage />
    </template>
    <template #main>
      <slot name="title">
        <h1 class="visually-hidden">{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer></template>
  </axdd-sidebar>
</template>

<script>
import { Sidebar, Profile } from "axdd-components";
import NavMenu from "./components/nav-menu.vue";
import NavMessage from "./components/nav-message.vue";

export default {
  name: "CompassApp",
  components: {
    "axdd-sidebar": Sidebar,
    "axdd-profile": Profile,
    NavMenu,
    NavMessage,
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
      signOutUrl: document.body.getAttribute("data-signout-url"),
      userRoles: document.body.getAttribute("data-user-role").split(','),
      // automatically set year
      currentYear: new Date().getFullYear(),
    };
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>
