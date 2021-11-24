// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">{{ pageTitle }}</h1>
    </template>

    <template #content>
      <div class="row justify-content-md-center mt-5 mb-3">
        <div class="col col-7">
          <div class="row">
            <div class="col">
              <div class="row">
                <div class="col small border-end">
                  <p class="fw-bold">Sign-ins</p>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck1">
                    <label class="form-check-label" for="defaultCheck1">
                      High
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck2">
                    <label class="form-check-label" for="defaultCheck2">
                      Average
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck2">
                    <label class="form-check-label" for="defaultCheck2">
                      Low
                    </label>
                  </div>
                </div>
                <div class="col small border-end">
                  <p class="fw-bold">Activity</p>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck3">
                    <label class="form-check-label" for="defaultCheck3">
                      High
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck4">
                    <label class="form-check-label" for="defaultCheck4">
                      Average
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck5">
                    <label class="form-check-label" for="defaultCheck5">
                      Low
                    </label>
                  </div>
                </div>
                <div class="col small border-end">
                  <p class="fw-bold">Assignments</p>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck6">
                    <label class="form-check-label" for="defaultCheck6">
                      High
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck7">
                    <label class="form-check-label" for="defaultCheck7">
                      Average
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck8">
                    <label class="form-check-label" for="defaultCheck8">
                      Low
                    </label>
                  </div>
                </div>
                <div class="col small">
                  <p class="fw-bold">Grades</p>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck9">
                    <label class="form-check-label" for="defaultCheck9">
                      High
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck10">
                    <label class="form-check-label" for="defaultCheck10">
                      Average
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck11">
                    <label class="form-check-label" for="defaultCheck11">
                      Low
                    </label>
                  </div>
                </div>
                <div class="col-12 small text-center">
                  <ul class="mt-3 mb-0 list-inline">
                    <li class="list-inline-item me-4"><strong>Low</strong> -5 to -3</li>
                    <li class="list-inline-item me-4"><strong>Average</strong> -2.9 to +2.9</li>
                    <li class="list-inline-item"><strong>High</strong> +3 to +5</li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="col-5 small border-start">
              <p class="fw-bold">Populations</p>
              <div class="grid" style="--bs-columns: 2; row-gap: 0;">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck12">
                  <label class="form-check-label" for="defaultCheck12">
                    Pre-major
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck17">
                  <label class="form-check-label text-nowrap" for="defaultCheck17">
                    Extended Pre-major
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck13">
                  <label class="form-check-label" for="defaultCheck13">
                    STEM
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck14">
                  <label class="form-check-label" for="defaultCheck14">
                    Freshman
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck15">
                  <label class="form-check-label" for="defaultCheck15">
                    Athlete
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck16">
                  <label class="form-check-label" for="defaultCheck16">
                    International
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-5 mb-3">

        <div class="col-sm-2 border-end">
          <div class="small lh-lg">Show week:</div>
          <select class="form-select form-select-sm" aria-label="Default select example">
            <option selected>Current Week</option>
            <option value="1">Autumn 2021: Week 4</option>
            <option value="2">Autumn 2021: Week 3</option>
            <option value="3">Autumn 2021: Week 2</option>
            <option value="4">Autumn 2021: Week 1</option>
          </select>
        </div>
        <div class="col-sm-2">
          <div class="small lh-lg">Display caseload for:</div>
          <select class="form-select form-select-sm" aria-label="Default select example">
            <option value="0">All advisers</option>
            <option selected value="1">Jon Average</option>
            <option value="2">April Foolery</option>
            <option value="3">Bob Samsonite</option>
          </select>
        </div>

        <div class="col-sm-4 offset-md-4">
          <div class="small lh-lg">
            <div class="d-inline me-3 text-nowrap">Find student by:</div>
            <div class="d-inline text-nowrap">
              <div
                class="form-check form-check-inline mb-0"
                v-for="option in searchRadioOptions"
                :key="option.id"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  name="searchRadioOptions"
                  :id="option.id"
                  :value="option"
                  v-model="searchOption"
                  style="margin-top:6px;"
                />
                <label class="form-check-label" :for="option.id">{{ option.label }}</label>
              </div>
            </div>
          </div>
          <div class="input-group input-group-sm mb-0">
            <input
              type="text"
              class="form-control"
              :placeholder="'Student ' + searchOption.label + ' Contains...'"
              :aria-label="'Student ' + searchOption.label + ' Contains...'"
              v-model="searchText"
              aria-describedby="button-addon2"
            />
            <button
              class="btn btn-outline-primary"
              type="button"
              id="button-addon2"
              v-on:click="loadStudentList"
            >
              GO
            </button>
          </div>
        </div>
      </div>


      <div class="row">
        <div class="col">
          <div class="bg-white border rounded-3 shadow-sm p-3 table-responsive">
            <table class="table table-hover mb-0">
              <thead class="">
                <tr>
                  <th scope="col">Student</th>
                  <th scope="col">Student Number</th>
                  <th scope="col">Class</th>
                  <th scope="col">Major</th>
                  <th scope="col">Enroll Status</th>
                  <th scope="col">Adviser</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in students" :key="item.SystemKey">
                  <td>
                    <div class="d-flex">
                      <div :class="getRandomPriority()" class="rounded-circle border border-3 me-2" style="width:55px;">
                        <img
                          v-if="item.gender === 'F'"
                          :src="'https://randomuser.me/api/portraits/thumb/women/' + getRandomPerson() + '.jpg'"
                          class="img-fluid rounded-circle border border-white border-2"

                        />
                        <img
                          v-else
                          :src="'https://randomuser.me/api/portraits/thumb/men/' + getRandomPerson() + '.jpg'"
                          class="img-fluid rounded-circle border border-white border-2"

                        />
                      </div>
                      <div>
                        <div>{{ item.student_preferred_last_name }}, {{ item.student_preferred_first_name }} <span class="badge rounded-pill border border-muted text-dark small me-1">{{ item.gender }}</span></div>
                        <div class="small text-secondary">{{ item.uw_net_id }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <router-link :to="{ name: 'Student', params: { id: item.student_number } }">
                      {{ item.student_number }}
                    </router-link>
                  </td>
                  <td>{{ item.class_desc }}</td>
                  <td>{{ item.major_full_name }}</td>
                  <td>{{ item.enrollment_status_desc }}</td>
                  <td>{{ item.adviser_full_name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="mt-2 mb-4 text-end">
            <pagination
              v-model="currentPage"
              :records="studentsCount"
              :per-page="pageSize"
              :options="pageOptions"
              @paginate="loadStudentList"
            >
            </pagination>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import {markRaw} from 'vue'
import Pagination from 'v-pagination-3';
import MyPagination from '../components/pagination.vue';
import Layout from '../layout.vue';
import dataMixin from '../mixins/data_mixin.js';

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    pagination: Pagination,
  },
  created: function () {
    this.loadStudentList();
    this.searchOption = this.searchRadioOptions[0];
  },
  data() {
    return {
      pageTitle: 'Home',
      // data
      students: [],
      // pagination
      studentsCount: 0,
      currentPage: 1,
      pageSize: 30,
      pageOptions: {
        theme: 'bootstrap4',
        template: markRaw(MyPagination),
      },
      // search filters
      searchOption: null,
      searchText: '',
      searchRadioOptions: [
        {
          id: 'student-number',
          label: 'Number',
        },
        {
          id: 'student-name',
          label: 'Name',
        },
        {
          id: 'student-email',
          label: 'UW NetId',
        },
      ],
    };
  },
  computed: {
    paginationOptions: function () {
      return {
        offset: this.pageSize * (this.currentPage - 1),
        limit: this.pageSize,
      };
    },
    searchOptions: function () {
      if (this.searchOption) {
        return {
          filter_type: this.searchOption.id,
          filter_text: this.searchText,
        };
      } else {
        return {};
      }
    },
    numPages: function () {
      let page = Math.ceil(this.studentsCount / this.pageSize);
      return page > 0 ? page : 1;
    },
  },
  methods: {
    loadStudentList: function () {
      let _this = this;
      this.getStudentList(this.paginationOptions, this.searchOptions).then((response) => {
        if (response.data) {
          _this.students = response.data['results'];
          _this.studentsCount = response.data['count'];
          if (_this.currentPage > _this.numPages) {
            _this.currentPage = 1;
          }
        }
      });
    },
    getRandomPerson: function(rangeMax) {
      // if no range is specified
      if (!rangeMax) {
        rangeMax = 100
      }
      // return random number
      return Math.floor(Math.random() * rangeMax);
    },
    getRandomPriority: function() {
      let int = Math.floor(Math.random() * 10);
      if (int == 0) {
        return 'border-danger'
      }
      else if (int == 1) {
        return 'border-warning'
      }
      else {
        return 'border-light'
      }
    }
  },
};
</script>

<style lang="scss">
.table {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
