// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">{{ pageTitle }}</h1>
    </template>

    <template #content>
      <div class="row justify-content-between mt-5 mb-2">
        <div class="col-sm-4">
          <div class="small">
            <div class="d-inline me-3 text-nowrap">Find student by here:</div>
            <div class="d-inline text-nowrap">
              <div class="form-check form-check-inline" v-for="option in searchOptions" :key="option.id">
                <input class="form-check-input" type="radio" name="searchRadioOptions" :id="option.id" :value="option" v-model="searchOption">
                <label class="form-check-label" :for="option.id">{{option.label}}</label>
              </div>
            </div>
          </div>
          <div class="input-group input-group-sm mb-3">
            <input type="text" class="form-control" :placeholder="'Student ' + searchOption.label + ' Contains...'" :aria-label="'Student ' + searchOption.label + ' Contains...'" v-model="searchText" aria-describedby="button-addon2">
            <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="filterEnrolledStudents">GO</button>
          </div>
        </div>
        <div class="col-sm-4">
          <div class="small">Select advisor caseload:</div>
          <select class="form-select form-select-sm" aria-label="Default select example">
            <option selected>All advisers</option>
            <option value="1">Jon Average</option>
            <option value="2">April Foolery</option>
            <option value="3">Bob Samsonite</option>
          </select>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <table class="table table-striped table-hover border">
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
              <tr v-for="(item,) in enrolledStudents" :key="item.StudentNumber">
                <td>{{item.StudentName}}</td>
                <td><router-link to="/student">{{item.StudentNumber}}</router-link></td>
                <td>{{item.UWNetID}}</td>
                <td>{{item.ClassDesc}}</td>
                <td>{{item.MajorDesc}}</td>
                <td>{{item.EnrollStatusCode}}</td>
                <td>{{item.Gender}}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <paginate
            v-model="currentPage"
            :records="enrolledStudentsCount"
            :per-page="pageSize"
            @paginate="filterEnrolledStudents">
          </paginate>
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
  created: function() {
    let _this = this;
    this.getEnrolledStudentsCount().then(
      function(result) {
        _this.enrolledStudentsCount = result.data["enrolled_students_count"];
      }
    );
    this.loadEnrolledStudents({});
    this.searchOption = this.searchOptions[0];
  },
  data() {
    return {
      pageTitle: "Home",
      enrolledStudents: [],
      enrolledStudentsCount: 0,
      pageSize: 10,
      currentPage: 1,
      searchOption: null,
      searchText: "",
      searchOptions: [
        {
          id: "student-number",
          label: "Number"
        },
        {
          id: "student-name",
          label: "Name"
        },
        {
          id: "student-email",
          label: "Email"
        },
      ]
    };
  },
  computed: {
    searchFilters: function() {
      let searchFilterType = null;
      let searchFilterText = null;
      if (this.searchOption) {
        searchFilterType = this.searchOption.id;
        searchFilterText = this.searchText;
      }
      return {
        searchFilter: {
          filterType: searchFilterType,
          filterText: searchFilterText
        }
      };
    },
    numPages: function() {
      return Math.ceil(this.enrolledStudentsCount / this.pageSize)
    }
  },
  methods: {
    filterEnrolledStudents: function() {
      this.loadEnrolledStudents(this.searchFilters);
    },
    loadEnrolledStudents: function(filters) {
      let _this = this;
      this.getEnrolledStudentsList(filters).then(response => {
        if (response.data) {
          _this.enrolledStudents = response.data;
        }
      });
    }
  },
};
</script>

<style lang="scss"></style>
