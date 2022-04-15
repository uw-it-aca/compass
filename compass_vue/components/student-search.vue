<template>
  <div class="input-group">
    <input
      type="text"
      class="form-control form-control-sm"
      placeholder="Search all students..."
      aria-label="Recipient's username"
      aria-describedby="button-addon2"
    />
    <button class="btn btn-sm btn-outline-dark-beige" type="button" @click="findStudent">Search</button>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    findStudent: function () {
      // push to search page
      this.$router.push('/student/1544522');
    },
  },
};
</script>
