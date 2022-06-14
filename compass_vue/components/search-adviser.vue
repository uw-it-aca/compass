<template>
  <div class="input-group">
    <input
      type="text"
      class="form-control form-control-sm"
      placeholder="Adviser netid..."
      aria-label="Recipient's username"
      aria-describedby="button-addon2"
    />
    <button
      class="btn btn-sm btn-outline-dark-beige"
      type="button"
      @click="findStudent"
    >
      Search
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>
