// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">{{ pageTitle }}</h1>
    </template>

    <template #content>
      <div class="row justify-content-center my-5">
        <div class="col-8">
          <div class="bg-light p-3 text-center">placeholder search component</div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Student Name</th>
                <th scope="col">Student Number</th>
                <th scope="col">Data</th>
                <th scope="col">Data</th>
                <th scope="col">Data</th>
                <th scope="col">Data</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Average, Jon</td>
                <td><router-link to="/student/28376465">28376465</router-link></td>
                <td>afdas</td>
                <td>afdas</td>
                <td>asdfads</td>
                <td>asdfads</td>
              </tr>
              <tr>
                <td>Thompson, Timmy</td>
                <td><router-link to="/student/87634323">87634323</router-link></td>
                <td>asdfads</td>
                <td>asdfadsf</td>
                <td>afdas</td>
                <td>asdfsadfads</td>
              </tr>
              <tr>
                <td>Johnson, Jill</td>
                <td><router-link to="/student/29579067">29579067</router-link></td>
                <td>asdf</td>
                <td>asda</td>
                <td>afdas</td>
                <td>asfd</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';

export default {
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: 'Home',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
