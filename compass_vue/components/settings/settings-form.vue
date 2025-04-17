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
        v-show="updatePermissionDenied"
        class="alert alert-danger py-2 small"
        role="alert"
      >
        You don't have permission to update {{ settingLabel }}s.
      </div>
      <ul class="list-unstyled mb-4">
        <li v-for="setting in settings" :key="setting.id" class="mb-1">
          <div class="input-group input-group-sm">
            <input
              v-model="setting.name"
              class="form-control"
              :aria-label="setting.name"
              :disabled="!setting.editable"
              type="text"
            />
            <button
              :disabled="!setting.editable"
              class="btn btn-secondary"
              type="button"
              @click="toggleSettingVisibility(setting)"
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
        />
        <button
          id="button-addon2"
          class="btn btn-secondary"
          type="button"
          @click="addSetting"
        >
          <i class="bi bi-plus-square-fill"></i>
        </button>
      </div>

      <div class="d-grid gap-1 d-md-flex justify-content-end mt-4">
        <button
          class="btn btn-sm btn-light me-1"
          type="button"
          @click="loadSettings"
        >
          Cancel
        </button>
        <button
          class="btn btn-sm btn-purple"
          type="button"
          @click="submitSettingsForm"
        >
          Save
        </button>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import { getSettings, saveSettings } from "@/utils/data";

export default {
  components: {},
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
  setup() {
    return {
      getSettings,
      saveSettings,
    };
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
      this.getSettings(this.accessGroup.id, this.settingType)
        .then((response) => {
          if (response) {
            this.settings = response;
          }
        })
        .catch((error) => {
          if (error.response.status == 401) {
            this.updatePermissionDenied = true;
          }
        });
    },
    submitSettingsForm() {
      this.saveSettings(this.accessGroup.id, this.settingType, this.settings)
        .then((response) => {
          if (response) {
            // show and update successful message for 3 seconds
            this.updateSuccessful = true;
            setTimeout(() => (this.updateSuccessful = false), 3000);
          }
        })
        .catch((error) => {
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
        setting.editable = true;
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
