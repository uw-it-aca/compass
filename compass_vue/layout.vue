<template>
  <!-- layout.vue: this is where you override the layout -->
  <axdd-sidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #navigation>
      <navigation></navigation>
    </template>
    <template #main>

      <div class="toast show w-100 mt-3 bg-danger text-white border-0 shadow-none">
        <div class="toast-header bg-danger text-white">
          <strong class="me-auto">System Message</strong>
          <small>11 mins ago, June 20, 2022</small>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="toast"
            aria-label="Close"
          ></button>
        </div>
        <div class="toast-body">
          Hello, world! This is a toast message. Lorem, ipsum dolor sit amet
          consectetur adipisicing elit. Nisi, accusamus! Consectetur hic ex esse
          ipsam veniam, est commodi doloribus, quas nostrum tenetur, accusamus
          eveniet voluptas laboriosam amet quam quibusdam libero.
        </div>
      </div>

      <slot name="title">
        <h1 class="visually-hidden">{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer></template>
  </axdd-sidebar>
</template>

<script>
import { Sidebar } from "axdd-components";
import Nav from "./components/nav.vue";

export default {
  name: "Compass",
  components: {
    "axdd-sidebar": Sidebar,
    navigation: Nav,
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
