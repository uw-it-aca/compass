// home.vue

<template>
  <layout :page-title="'Home'">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">Home</h1>
    </template>

    <template #content>
      <div class="row my-4">
        <div class="col-lg-2">
          <div class="small lh-lg">Display caseload for:</div>
          <select class="form-select form-select-sm" aria-label="Default select example">
            <option value="0">All advisers</option>
            <option selected value="1">Jon Average</option>
            <option value="2">April Foolery</option>
            <option value="3">Bob Samsonite</option>
          </select>
        </div>

        <div class="col-lg-2 border-start">
          <div class="small lh-lg">Show week:</div>
          <select class="form-select form-select-sm" aria-label="Default select example">
            <option selected>Current Week</option>
            <option value="1">Autumn 2021: Week 4</option>
            <option value="2">Autumn 2021: Week 3</option>
            <option value="3">Autumn 2021: Week 2</option>
            <option value="4">Autumn 2021: Week 1</option>
          </select>
        </div>

        <div class="col offset-lg-3">
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
                  style="margin-top: 6px"
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
        <div class="col-md-3 col-lg-2 small">
          <div class="border-bottom mb-3 pb-3">
            <div class="fw-bold">Sign-ins</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck1" />
              <label class="form-check-label" for="defaultCheck1"> High </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck2" />
              <label class="form-check-label" for="defaultCheck2"> Average </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck2" />
              <label class="form-check-label" for="defaultCheck2"> Low </label>
            </div>

            <div class="fw-bold">Activity</div>
            <div class="form-check">

              <input class="form-check-input" type="checkbox" value="" id="defaultCheck3" />
              <label class="form-check-label" for="defaultCheck3"> High </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck4" />
              <label class="form-check-label" for="defaultCheck4"> Average </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck5" />
              <label class="form-check-label" for="defaultCheck5"> Low </label>
            </div>

            <div class="fw-bold">Assignments</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck6" />
              <label class="form-check-label" for="defaultCheck6"> High </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck7" />
              <label class="form-check-label" for="defaultCheck7"> Average </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck8" />
              <label class="form-check-label" for="defaultCheck8"> Low </label>
            </div>

            <div class="fw-bold">Grades</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck9" />
              <label class="form-check-label" for="defaultCheck9"> High </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck10" />
              <label class="form-check-label" for="defaultCheck10"> Average </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck11" />
              <label class="form-check-label" for="defaultCheck11"> Low </label>
            </div>

            <ul class="mt-3 mb-0 list-inline">
              <li class="list-inline-item"><strong>Low</strong> -5 to -3</li>
              <li class="list-inline-item"><strong>Average</strong> -2.9 to +2.9</li>
              <li class="list-inline-item"><strong>High</strong> +3 to +5</li>
            </ul>
          </div>

          <div class="border-bottom mb-3 pb-3">
            <div class="fw-bold">Populations</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck12" />
              <label class="form-check-label" for="defaultCheck12"> Pre-major </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck17" />
              <label class="form-check-label text-nowrap" for="defaultCheck17">
                Extended Pre-major
              </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck13" />
              <label class="form-check-label" for="defaultCheck13"> STEM </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck14" />
              <label class="form-check-label" for="defaultCheck14"> Freshman </label>
            </div>
            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="defaultCheck15"
                checked
              />
              <label class="form-check-label" for="defaultCheck15"> Athlete </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck16" />
              <label class="form-check-label" for="defaultCheck16"> International </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="defaultCheck17" />
              <label class="form-check-label" for="defaultCheck17"> Graduate </label>
            </div>
          </div>

          <div class="mb-3 pb-3">
            <div class="fw-bold">Sport</div>
            <select class="form-select form-select-sm" aria-label="Default select example">
              <option selected>All sports</option>
              <option value="1">Football</option>
              <option value="2">Soccer</option>
              <option value="3">Track</option>
            </select>
          </div>
        </div>
        <div class="col-md-9 col-lg-10">
          <div class="bg-white border rounded-3 shadow-sm p-3 table-responsive">
            <table class="table table-hover mb-0">
              <thead class="">
                <tr>
                  <th scope="col">Student</th>
                  <th scope="col" class="text-nowrap">Student Number</th>
                  <th scope="col">Priority</th>
                  <th scope="col">Class</th>
                  <th scope="col">Major</th>
                  <th scope="col" class="text-nowrap">Enroll Status</th>
                  <th scope="col">Adviser</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in students" :key="item.SystemKey">
                  <td>
                    <div class="d-flex">
                      <div class="me-2" style="min-width: 55px">
                        <div
                          :class="showPriorityRing(item.retention.priority)"
                          class="rounded-circle border border-3"
                        >
                          <img
                            v-if="item.gender === 'F'"
                            :src="
                              'https://randomuser.me/api/portraits/thumb/women/' +
                              getRandomPerson() +
                              '.jpg'
                            "
                            class="img-fluid rounded-circle border border-white border-2"
                          />
                          <img
                            v-else
                            :src="
                              'https://randomuser.me/api/portraits/thumb/men/' +
                              getRandomPerson() +
                              '.jpg'
                            "
                            class="img-fluid rounded-circle border border-white border-2"
                          />
                        </div>
                      </div>
                      <div>
                        <div class="text-nowrap">
                          <span
                            >{{ item.student_preferred_last_name }},
                            {{ item.student_preferred_first_name }}</span
                          >
                          <span class="badge rounded-pill border border-muted text-dark small">{{
                            item.gender
                          }}</span>
                          <span class="badge rounded-pill border border-muted text-dark small"
                            ><i class="bi bi-trophy-fill text-purple"></i
                          ></span>
                        </div>
                        <div class="small text-secondary">{{ item.uw_net_id }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <router-link :to="{ name: 'Student', params: { id: item.student_number } }">
                      {{ item.student_number }}
                    </router-link>
                  </td>
                  <td>{{ item.retention.priority }}</td>
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
import { markRaw } from 'vue';
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
    getRandomPerson: function (rangeMax) {
      // if no range is specified
      if (!rangeMax) {
        rangeMax = 100;
      }
      // return random number
      return Math.floor(Math.random() * rangeMax);
    },
    showPriorityRing: function (priorityValue) {
      // mocked display
      if (priorityValue == '-3.4') {
        return 'border-danger';
      } else if (priorityValue == '2.2') {
        return 'border-warning';
      } else {
        return '';
      }
    },
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
