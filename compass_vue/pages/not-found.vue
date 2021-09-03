// about.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1>Page Not Found</h1>
    </template>

    <template #content>
      <div class="row">
        <div class="col">
          page not found asldfj asdflkj
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';

export default {
  components: {
    layout: Layout
  },
  data() {
    return {
      pageTitle: 'Page not found',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
