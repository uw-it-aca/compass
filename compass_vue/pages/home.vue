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
              <div class="form-check form-check-inline" v-for="option in searchRadioOptions" :key="option.id">
                <input class="form-check-input" type="radio" name="searchRadioOptions" :id="option.id" :value="option" v-model="searchOption">
                <label class="form-check-label" :for="option.id">{{option.label}}</label>
              </div>
            </div>
          </div>
          <div class="input-group input-group-sm mb-3">
            <input type="text" class="form-control" :placeholder="'Student ' + searchOption.label + ' Contains...'" :aria-label="'Student ' + searchOption.label + ' Contains...'" v-model="searchText" aria-describedby="button-addon2">
            <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="loadStudentList">GO</button>
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
                <th scope="col"></th>
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
              <tr v-for="(item,) in students" :key="item.SystemKey">
                <td>
                  <div style="width:40px;">
                    <img src="/static/img/napoleon-dynamite.jpeg" class="img-fluid rounded-circle border border-3" alt="">
                  </div>
                </td>
                <td>{{item.student_name}}</td>
                <td>
                  <router-link :to="{ name: 'Student', params: { id: item.student_number } }">
                    {{item.student_number}}
                  </router-link>
                </td>
                <td>{{item.uw_net_id}}</td>
                <td>{{item.class_desc}}</td>
                <td>{{item.major_full_name}}</td>
                <td>{{item.enrollment_status_desc}}</td>
                <td>{{item.gender}}</td>
                <td>{{item.adviser_full_name}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <paginate
            v-model="currentPage"
            :records="studentsCount"
            :per-page="pageSize"
            @paginate="loadStudentList">
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
    this.loadStudentList();
    this.searchOption = this.searchRadioOptions[0];
  },
  data() {
    return {
      pageTitle: "Home",
      // data
      students: [],
      // pagination
      studentsCount: 0,
      currentPage: 1,
      pageSize: 50,
      // search filters
      searchOption: null,
      searchText: "",
      searchRadioOptions: [
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
    paginationOptions: function() {
      return {
        offset: this.pageSize * (this.currentPage - 1),
        limit: this.pageSize
      };
    },
    searchOptions: function() {
      if (this.searchOption != null) {
        this.currentPage = 1;
        return {
          filter_type: this.searchOption.id,
          filter_text: this.searchText
        };
      } else {
        return {};
      }
    },
    numPages: function() {
      let page = Math.ceil(this.studentsCount / this.pageSize);
      return (page > 0) ? page : 1;
    }
  },
  methods: {
    loadStudentList: function() {
      let _this = this;
      this.getStudentList(this.paginationOptions, this.searchOptions).then(response => {
        if (response.data) {
          _this.students = response.data["results"];
          _this.studentsCount = response.data["count"]
        }
      });
    }
  },
};
</script>

<style lang="scss">
</style>
