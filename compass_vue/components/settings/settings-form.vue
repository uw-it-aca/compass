<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">{{ modelLabel }}</axdd-card-heading>
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
        <li v-for="item in items" :key="item.name" class="mb-1">
          <div class="input-group input-group-sm">
            <input
              type="text"
              :value="item.name"
              class="form-control"
              aria-label="tbd"
            />
            <button class="btn btn-outline-secondary" type="button">
              <i v-if="item.active" class="bi bi-eye-fill"></i>
              <i v-else class="bi bi-eye-slash-fill"></i>
            </button>
          </div>
        </li>
      </ul>
      <div class="input-group input-group-sm">
        <input
          type="text"
          class="form-control"
          :placeholder="'Add new ' + modelLabel + '...'"
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
        <button class="btn btn-sm btn-light me-1" type="button">Cancel</button>
        <button
          @click="saveSettings"
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

export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
    modelLabel: {
      type: String,
      required: true,
    },
    updateSuccessful: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
  data() {
    return {
      originalItems: this.items,
    };
  },
  methods: {
    saveSettings() {
      this.$emit("saveSettings", this.modelLabel);
    },
    clearSettings() {
      this.items = this.originalItems;
    },
  },
};
</script>
