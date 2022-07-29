<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1>Settings</h1>
    </template>
    <template #content>
      <div v-for="(item, group) in settings" :key="group" class="row my-4">
        <h2>{{ group }}</h2>
        <div class="col-xl-6">
          <SettingsForm
            :items="item.programs"
            :updateSuccessful="false"
            modelLabel="program"
          ></SettingsForm>
        </div>
        <div class="col-xl-6">
          <SettingsForm
            :items="item.contact_topics"
            :updateSuccessful="false"
            modelLabel="contact topic"
          ></SettingsForm>
          <SettingsForm
            :items="item.contact_types"
            :updateSuccessful="false"
            modelLabel="contact type"
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
      settings: {},
    };
  },
  created() {
    this.loadSettings();
  },
  methods: {
    loadSettings: function () {
      this.getSettings().then((response) => {
        if (response.data) {
          this.settings = response.data;
        }
      });
    },
  },
};
</script>

<style lang="scss"></style>
