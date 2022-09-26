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
      <div
        class="alert alert-danger py-2 small"
        role="alert"
        v-show="updatePermissionDenied"
      >
        You don't have permission to update {{ settingLabel }}s.
      </div>
      <ul class="list-unstyled mb-4">
        <li v-for="setting in settings" :key="setting.id" class="mb-1">
          <div class="input-group input-group-sm">
            <input
              type="text"
              v-model="setting.name"
              class="form-control"
              :aria-label="setting.name"
              :disabled="!setting.editable"
            />
            <button
              @click="toggleSettingVisibility(setting)"
              class="btn btn-outline-secondary"
              type="button"
              :disabled="!setting.editable"
            >
              <i v-if="setting.active" class="bi bi-eye-fill"></i>
              <i v-else class="bi bi-eye-slash-fill"></i>
            </button>
          </div>
        </li>
      </ul>
      <div class="input-group input-group-sm">
        <input
          v-model="newSettingName"
          type="text"
          class="form-control"
          :placeholder="'Add new ' + settingLabel + '...'"
          aria-label="Topic label"
          aria-describedby="button-addon2"
          :disabled="!setting.editable"
        />
        <button
          @click="addSetting"
          class="btn btn-outline-secondary"
          type="button"
          id="button-addon2"
          :disabled="!setting.editable"
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
      settings: [],
      newSettingName: "",
      updateSuccessful: false,
      updatePermissionDenied: false,
    };
  },
  created() {
    this.loadSettings();
  },
  methods: {
    loadSettings() {
      this.getSettings(this.accessGroup.id, this.settingType).then(
        (response) => {
          if (response.data) {
            this.settings = response.data;
          }
        }
      ).catch((error) => {
        if (error.response.status == 401) {
          this.updatePermissionDenied = true;
        }
      });
    },
    submitSettingsForm() {
      this.saveSettings(
        this.accessGroup.id,
        this.settingType,
        this.settings
      ).then((response) => {
        if (response.data) {
          // show and update successful message for 3 seconds
          this.updateSuccessful = true;
          setTimeout(() => (this.updateSuccessful = false), 3000);
        }
      }).catch((error) => {
        if (error.response.status == 401) {
          this.updatePermissionDenied = true;
          setTimeout(() => (this.updatePermissionDenied = false), 3000);
        }
      });
    },
    addSetting() {
      if (this.newSettingName.length) {
        var setting = {};
        setting.id = null;
        setting.name = this.newSettingName;
        setting.active = true;
        setting.access_group = this.accessGroup;
        this.settings.push(setting);
        // clear the add new setting input
        this.newSettingName = "";
      }
    },
    toggleSettingVisibility(setting) {
      setting.active = !setting.active;
    },
  },
};
</script>
