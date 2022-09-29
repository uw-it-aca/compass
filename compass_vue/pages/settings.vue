<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1>Settings</h1>
    </template>
    <template #content>
      <div
        v-for="group in accessGroups"
        :key="group.access_group_id"
        class="row my-4"
      >
        <h2>{{ group.name }}</h2>
        <div class="col-xl-6">
          <SettingsForm
            settingLabel="program"
            settingType="program"
            :accessGroup="group"
          ></SettingsForm>
        </div>
        <div class="col-xl-6">
          <SettingsForm
            settingLabel="contact topic"
            settingType="contact_topic"
            :accessGroup="group"
          ></SettingsForm>
          <SettingsForm
            settingLabel="contact type"
            settingType="contact_type"
            :accessGroup="group"
          ></SettingsForm>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

import SettingsForm from "../components/settings/settings-form.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    SettingsForm,
  },
  data() {
    return {
      pageTitle: "Settings",
      isLoading: true,
      accessGroups: [],
    };
  },
  created: function () {
    this.loadAccessGroups();
  },
  methods: {
    loadAccessGroups: function () {
      this.getAccessGroups().then((response) => {
        if (response.data) {
          this.accessGroups = response.data;
        }
      });
    },
  },
};
</script>
