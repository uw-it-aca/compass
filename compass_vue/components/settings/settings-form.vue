<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">{{ settingLabel }}</axdd-card-heading>
    </template>
    <template #body>
      <div
        v-if="updateSuccessful"
        class="alert alert-success py-2 small"
        role="alert"
      >
        Update successful!
      </div>

      <ul class="list-unstyled mb-4">
        <li v-for="setting in settings" :key="setting.name" class="mb-1">
          <div class="input-group input-group-sm">
            <input
              type="text"
              :value="setting.name"
              class="form-control"
              :aria-label="setting.name"
            />
            <button
              @click="toggleSettingVisibility(setting)"
              class="btn btn-outline-secondary"
              type="button"
            >
              <i v-if="setting.active" class="bi bi-eye-fill"></i>
              <i v-else class="bi bi-eye-slash-fill"></i>
            </button>
          </div>
        </li>
      </ul>
      <div class="input-group input-group-sm">
        <input
          type="text"
          class="form-control"
          :placeholder="'Add new ' + settingLabel + '...'"
          aria-label="Topic label"
          aria-describedby="button-addon2"
        />
        <button
          class="btn btn-outline-secondary"
          type="button"
          id="button-addon2"
        >
          <i class="bi bi-plus-square-fill"></i>
        </button>
      </div>

      <div class="d-grid gap-1 d-md-flex justify-content-end mt-4">
        <button
          @click="loadSettings"
          class="btn btn-sm btn-light me-1"
          type="button"
        >
          Cancel
        </button>
        <button
          @click="submitSettingsForm"
          class="btn btn-sm btn-purple"
          type="button"
        >
          Save
        </button>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from "axdd-components";
import dataMixin from "../../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  props: {
    settingLabel: {
      type: String,
      required: true,
    },
    settingType: {
      type: String,
      required: true,
    },
    accessGroup: {
      type: Object,
      required: true,
    },
  },
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
  data() {
    return {
      settings: {},
      updateSuccessful: false,
    };
  },
  created() {
    this.loadSettings();
  },
  methods: {
    loadSettings() {
      this.getSettings(this.accessGroup.access_group_id, this.settingType).then(
        (response) => {
          if (response.data) {
            this.settings = response.data;
          }
        }
      );
    },
    submitSettingsForm() {
      this.saveSettings(
        this.accessGroup.access_group_id,
        this.settingType
      ).then((response) => {
        if (response.data) {
          // show and update successful message for 3 seconds
          this.updateSuccessful = true;
          setTimeout(() => (this.updateSuccessful = false), 3000);
        }
      });
    },
    toggleSettingVisibility(setting) {
      setting.active = !setting.active;
    },
  },
};
</script>
