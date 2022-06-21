// settings.vue

<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1>Settings</h1>
    </template>
    <template #content>
      <div class="row my-4">
        <div class="col-xl-7">batch assignment</div>
        <div class="col-xl-5">
          <SettingsTopics></SettingsTopics>
          <SettingsTypes></SettingsTypes>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

import SettingsTopics from "../components/settings/topics.vue";
import SettingsTypes from "../components/settings/types.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    SettingsTopics,
    SettingsTypes,
  },
  data() {
    return {
      pageTitle: "Settings",
      isLoading: true,
    };
  },
};
</script>

<style lang="scss"></style>
