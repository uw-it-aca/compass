<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Topics</axdd-card-heading>
    </template>
    <template #body>
      <div class="alert alert-success py-2 small" role="alert">Added!</div>
      <ul class="list-unstyled border-bottom pb-3">
        <li class="mb-1">
          <div class="input-group input-group-sm">
            <input
              type="text"
              value="Hello"
              class="form-control"
              aria-label="tbd"
            />
            <button class="btn btn-outline-purple" type="button">
              <i class="bi bi-trash-fill"></i>
            </button>
            <button class="btn btn-outline-purple" type="button">
              <i class="bi bi-save-fill"></i>
            </button>
          </div>
        </li>
        <li class="mb-1">
          <div class="input-group input-group-sm">
            <input
              type="text"
              value="World"
              class="form-control"
              aria-label="tbd"
            />
            <button class="btn btn-outline-purple" type="button">
              <i class="bi bi-trash-fill"></i>
            </button>
            <button class="btn btn-outline-purple" type="button">
              <i class="bi bi-save-fill"></i>
            </button>
          </div>
        </li>
      </ul>

      <div class="input-group input-group-sm">
        <input
          type="text"
          class="form-control"
          placeholder="Add new contact topic..."
          aria-label="Topic label"
          aria-describedby="button-addon2"
        />
        <button class="btn btn-purple" type="button" id="button-addon2">
          Add
        </button>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from "axdd-components";

export default {
  props: {
    student: {
      type: Object,
      required: true,
    },
  },
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
  data() {
    return {};
  },
};
</script>
