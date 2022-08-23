<template>
  <div class="text-light">
    <p
      v-show="$route.path == '/'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>check-ins</strong>. View upcoming student appointments.
    </p>

    <p
      v-show="$route.path == '/caseload'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>caseloads</strong>. View all students in your current
      caseload.
    </p>
    <p
      v-show="$route.path == '/settings'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>settings</strong>. Manage your teams form options.
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>
