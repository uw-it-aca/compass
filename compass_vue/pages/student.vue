// about.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <div v-if="$route.params.id" class="row border-bottom mb-3">
        <div class="col-10">
          <h1 class="h3 text-uppercase">Lastname, Firstname</h1>
          <h2 class="h3">{{ $route.params.id }}</h2>
        </div>
        <div class="col-2 text-end text-nowrap">
          <a class="btn btn-outline-light border text-secondary me-2" href="#" role="button" style="font-size: 20px;">
            <i class="bi bi-telephone"></i>
          </a>
          <a class="btn btn-outline-light border text-secondary" href="#" role="button" style="font-size: 20px;">
            <i class="bi bi-chat-right-text"></i>
          </a>
        </div>
      </div>
      <h1 v-else>Student</h1>
    </template>

    <template #content>
      <div v-if="$route.params.id">
        <div class="row">
          <div class="col-sm-8">
            <div class="card mb-3">
              <div class="row g-0">
                <div class="col-sm-4">
                  <svg class="bd-placeholder-img img-fluid rounded-start" width="100%" height="250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: Student Photo" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#868e96"></rect><text x="50%" y="50%" fill="#dee2e6" dy=".3em">Student Photo</text></svg>
                </div>
                <div class="col-sm-8">
                  <div class="card-body">
                    <h3 class="card-title">Profile</h3>
                    <ul>
                      <li>Preferred Name</li>
                      <li>Pronouns</li>
                      <li>UW NetId</li>
                      <li>DOB</li>
                      <li>Ethnicity</li>
                      <li>Gender</li>
                      <li>Citizenship</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="card mb-3">
              <div class="card-body">
                <h3 class="card-title">Contact</h3>
                <ul>
                  <li>UW Email</li>
                  <li>Personal email</li>
                  <li>Phone</li>
                  <li>Address</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-4">
            <div class="card mb-3">
              <div class="card-body">
                <h3 class="card-title">Standing</h3>
                <ul>
                  <li>Registered yes/no</li>
                  <li>Enrollment Status yes/no</li>
                  <li>Class standing (freshman, sophmore, etc.)</li>
                  <li>Total Credits</li>
                  <li>GPA</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="card mb-3">
              <div class="card-body">
                <h3 class="card-title">OMAD Specific?</h3>
                <ul>
                  <li>EOP - 13 yes/no</li>
                  <li>Pre-professional yes/no</li>
                  <li>IC Eligible yes/no</li>
                  <li>Special program yes/no</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="card mb-3">
              <div class="card-body">
                <h3 class="card-title">Academics</h3>
                <ul>
                  <li>Adviser Name</li>
                  <li>Active? yes/no</li>
                  <li>Desired Degree (as of quarter? timestamp)</li>
                  <li>Current Schedule (current quarter)</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>No student</div>
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
