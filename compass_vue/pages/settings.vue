// settings.vue

<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1>Settings</h1>
    </template>
    <template #content>
      <p>need to handle IF user belongs to multiple advising groups!</p>
      <div class="row my-4">
        <div class="col-xl-6">
          <SettingsPrograms></SettingsPrograms>
          <p>batch assignment</p>
        </div>
        <div class="col-xl-6">
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
import SettingsPrograms from "../components/settings/programs.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    SettingsTopics,
    SettingsTypes,
    SettingsPrograms,
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
