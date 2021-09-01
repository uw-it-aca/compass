// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #content>
      <div class="row">
        <div class="col">
          <span>Find student by:</span>
          <div class="form-check form-check-inline" v-for="option in searchOptions" :key="option.value">
            <input class="form-check-input" type="radio" :id="option.id" :value="option.value">
            <label class="form-check-label" :for="option.id">{{option.label}}</label>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">

          <table class="table">
            <thead>
              <tr>
                <th scope="col">Student Name</th>
                <th scope="col">Student Number</th>
                <th scope="col">UW NetID</th>
                <th scope="col">Class</th>
                <th scope="col">Major</th>
                <th scope="col">Enroll Status</th>
                <th scope="col">Gender</th>
                <th scope="col">Adviser</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item,) in enrolledStudents" :key="item.SystemKey">
                <td>{{item.StudentName}}</td>
                <td><router-link to="/student">{{item.StudentNumber}}</router-link></td>
                <td>{{item.UWNetID}}</td>
                <td>{{item.ClassDesc}}</td>
                <td>{{item.MajorFullName}}</td>
                <td>{{item.EnrollStatusCode}}</td>
                <td>{{item.Gender}}</td>
                <td></td>
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
import dataMixin from '../mixins/data_mixin.js';

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: 'Home',
      enrolledStudents: [],
      searchOptions: [
        {
          id: "student_number_radio",
          value: false,
          label: "Number"
        },
        {
          id: "student_name_radio",
          value: false,
          label: "Name"
        },
        {
          id: "student_email_radio",
          value: false,
          label: "Email"
        },
      ]
    };
  },
  created: function() {
    this.loadEnrolledStudents();
  },
  methods: {
    loadEnrolledStudents: function() {
      let _this = this;
      this.getEnrolledStudentsList().then(response => {
        if (response.data) {
          _this.enrolledStudents = response.data;
        }
      });
    }
  },
};
</script>

<style lang="scss"></style>
