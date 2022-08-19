<template>
  <div class="text-light">
    <p
      v-show="$route.path == '/'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>home</strong>... Lorem ipsum dolor, sit amet
      consectetur adipisicing elit. Cum voluptatibus, laborum inventore magni,
      dolore quod incidunt error reiciendis nesciunt ex atque, amet culpa quia
      ullam sit. Deleniti id at odit!
    </p>

    <p
      v-show="$route.path == '/caseload'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>caseloads</strong>... Lorem ipsum dolor, sit amet
      consectetur adipisicing elit. Cum voluptatibus, laborum inventore magni,
      dolore quod incidunt error reiciendis nesciunt ex atque, amet culpa quia
      ullam sit. Deleniti id at odit!
    </p>
  </div>
</template>

<script>
export default {
  props: {
    userRole: {
      type: String,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
