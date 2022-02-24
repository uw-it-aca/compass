// home.vue

<template>
  <layout :page-title="'Home'">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col-lg-4">
          <div class="small lh-lg">Show week:</div>
          <select class="form-select form-select-sm" aria-label="Default select example">
            <option selected>Current Week</option>
            <option value="1">Autumn 2021: Week 4</option>
            <option value="2">Autumn 2021: Week 3</option>
            <option value="3">Autumn 2021: Week 2</option>
            <option value="4">Autumn 2021: Week 1</option>
          </select>
        </div>

        <div class="col offset-lg-2">
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
            >GO</button>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="card shadow-sm mb-3">
            <h3
              class="card-header h6 text-uppercase text-muted fw-bold"
              style="line-height: 30px"
            >Students</h3>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover mb-0">
                  <thead class>
                    <tr>
                      <th scope="col">Name</th>
                      <th scope="col" class="text-nowrap">Student Number</th>
                      <th scope="col">Priority</th>
                      <th scope="col">Class</th>
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
                                  item.id +
                                  '.jpg'
                                "
                                class="img-fluid rounded-circle border border-white border-2"
                              />
                              <img
                                v-else
                                :src="
                                  'https://randomuser.me/api/portraits/thumb/men/' +
                                  item.id +
                                  '.jpg'
                                "
                                class="img-fluid rounded-circle border border-white border-2"
                              />
                            </div>
                          </div>
                          <div>
                            <div class="text-nowrap">
                              <span>
                                {{ item.student_preferred_last_name }},
                                {{ item.student_preferred_first_name }}
                              </span>
                              <span
                                class="badge rounded-pill border border-muted text-dark small"
                              >{{ item.gender }}</span>
                              <span class="badge rounded-pill border border-muted text-dark small">
                                <i class="bi bi-trophy-fill text-purple"></i>
                              </span>
                            </div>
                            <div class="small text-secondary">{{ item.uw_net_id }}</div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <router-link
                          :to="{ name: 'Student', params: { id: item.student_number } }"
                        >{{ item.student_number }}</router-link>
                      </td>
                      <td>{{ item.retention.priority }}</td>
                      <td>{{ item.class_desc }}</td>
                      <td>{{ item.enrollment_status_desc }}</td>
                      <td>{{ item.adviser_full_name }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer text-end">
              <pagination
                v-model="currentPage"
                :records="studentsCount"
                :per-page="pageSize"
                :options="pageOptions"
                @paginate="loadStudentList"
              ></pagination>
            </div>
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
