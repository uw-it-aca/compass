<template>
  <div class="alert alert-success py-2 small" role="alert">Add successful!</div>

  <ul class="list-unstyled mb-4">
    <li class="mb-1">
      <div class="input-group input-group-sm">
        <input
          type="text"
          value="Hello"
          class="form-control"
          aria-label="tbd"
        />
        <button class="btn btn-outline-secondary" type="button">
          <i class="bi bi-eye-slash-fill"></i>
        </button>
      </div>
    </li>
    <li class="mb-1">
      <div class="input-group input-group-sm">
        <input
          disabled
          type="text"
          value="World"
          class="form-control"
          aria-label="tbd"
        />
        <button class="btn btn-outline-secondary" type="button">
          <i class="bi bi-eye-fill"></i>
        </button>
      </div>
    </li>
    <li class="mb-1">
      <div class="input-group input-group-sm">
        <input
          type="text"
          value="Goodbye"
          class="form-control"
          aria-label="tbd"
        />
        <button class="btn btn-outline-secondary" type="button">
          <i class="bi bi-eye-slash-fill"></i>
        </button>
      </div>
    </li>
  </ul>
  <div class="input-group input-group-sm">
    <input
      type="text"
      class="form-control"
      :placeholder="'Add new ' + fieldType + '...'"
      aria-label="Topic label"
      aria-describedby="button-addon2"
    />
    <button class="btn btn-outline-secondary" type="button" id="button-addon2">
      <i class="bi bi-plus-square-fill"></i>
    </button>
  </div>

  <div class="d-grid gap-1 d-md-flex justify-content-end mt-4">
    <button class="btn btn-sm btn-light me-1" type="button">Cancel</button>
    <button class="btn btn-sm btn-purple" type="button">Save</button>
  </div>
</template>

<script>
export default {
  props: {
    fieldType: {
      type: String,
      required: true,
    },
  },
  components: {},
  data() {
    return {};
  },
};
</script>
