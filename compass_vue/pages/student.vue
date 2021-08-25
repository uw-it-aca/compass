// about.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #content>
      <div class="row">
        <div class="col">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Perferendis, ipsa officia.
          Tempore, laborum. Minima dolorum vero expedita saepe libero fuga quidem, tempore numquam
          eveniet, modi tenetur fugiat dolorem dignissimos ipsam.
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
      pageTitle: 'Student detail',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
