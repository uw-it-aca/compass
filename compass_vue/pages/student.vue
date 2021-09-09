// about.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>

      <div v-if="$route.params.id" class="row">
        <div class="col-sm-10">
          <h1 class="h3 text-uppercase">Average, John</h1>
          <h2>{{ $route.params.id }}</h2>
        </div>
        <div class="col-sm-2">
          <i class="bi bi-telephone"></i>
          <i class="bi bi-chat-right-text"></i>
        </div>
      </div>
      <h1 v-else>Student</h1>
    </template>

    <template #content>
      <div class="row">
        <div class="col">
          <div v-if="$route.params.id">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Perferendis, ipsa officia.
            Tempore, laborum. Minima dolorum vero expedita saepe libero fuga quidem, tempore numquam
            eveniet, modi tenetur fugiat dolorem dignissimos ipsam.
          </div>
          <div v-else>No student</div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import { Card } from 'axdd-components';
import Layout from '../layout.vue';
import HelloWorld from '../components/hello-world.vue';

export default {
  components: {
    layout: Layout,
    'hello-world': HelloWorld,
    'axdd-card': Card,
  },
  data() {
    return {
      pageTitle: 'Average, John #12345678',
    };
  },
  methods: {},
};
</script>

<style lang="scss">
</style>
