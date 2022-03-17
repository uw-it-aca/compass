// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-gray p-4 rounded-3">
            <div class="row">
              <div class="col-5 d-flex justify-content-between">
                <div class="flex-fill me-3">
                  <div class="fw-bold lh-lg">Show week:</div>
                  <select class="form-select form-select-sm" aria-label="Default select example">
                    <option selected>Current Week</option>
                    <option value="1">Autumn 2021: Week 4</option>
                    <option value="2">Autumn 2021: Week 3</option>
                    <option value="3">Autumn 2021: Week 2</option>
                    <option value="4">Autumn 2021: Week 1</option>
                  </select>
                </div>
                <div class="flex-fill">
                  <div class="fw-bold lh-lg">Display caseload for:</div>
                  <select class="form-select form-select-sm" aria-label="Default select example">
                    <option value="0">All advisers</option>
                    <option selected value="1">Jon Average</option>
                    <option value="2">April Foolery</option>
                    <option value="3">Bob Samsonite</option>
                  </select>
                </div>
              </div>
              <div class="col-7 border-start d-flex justify-content-between">
                <div class="flex-fill me-3">
                  <div class="fw-bold lh-lg">Class Standing:</div>
                  <select class="form-select form-select-sm" aria-label=".form-select-sm example">
                    <option selected>All</option>
                    <option value="1">Freshman</option>
                    <option value="2">Sophomore</option>
                    <option value="3">Junior</option>
                    <option value="4">Senior</option>
                  </select>
                </div>

                <div class="me-3">
                  <div class="fw-bold lh-lg">Population:</div>
                  <select class="form-select form-select-sm" aria-label=".form-select-sm example">
                    <option selected>All</option>
                    <option value="1">Atheletes</option>
                    <option value="2">Pre-Engineering</option>
                    <option value="3">STEM</option>
                  </select>
                </div>
                <div class="me-3">
                  <div class="fw-bold lh-lg">Sport (if Athelete):</div>
                  <select class="form-select form-select-sm" aria-label=".form-select-sm example">
                    <option selected>All</option>
                    <option value="1">Football</option>
                    <option value="2">Baseball</option>
                    <option value="3">Volleyball</option>
                  </select>
                </div>

                <div class="flex-fill">
                  <div class="fw-bold lh-lg">Status:</div>
                  <div class="form-check form-check-inline">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="flexRadioDefault"
                      id="flexRadioDefault1"
                    />
                    <label class="form-check-label" for="flexRadioDefault1">Active</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="flexRadioDefault"
                      id="flexRadioDefault2"
                      checked
                    />
                    <label class="form-check-label" for="flexRadioDefault2">Inactive</label>
                  </div>
                </div>
              </div>
            </div>
            <!-- Retention Filters-->
            <div class="row mt-4">
              <div class="col-5">
                <div class="d-flex">
                  <div class="fw-bold me-3">Priority:</div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck1" />
                    <label class="form-check-label" for="defaultCheck1"> Top </label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck2" />
                    <label class="form-check-label" for="defaultCheck2"> Middle </label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck2" />
                    <label class="form-check-label" for="defaultCheck2"> Bottom </label>
                  </div>
                </div>
              </div>
              <div class="col-7 border-start">
                <div class="">
                  <a
                    class="small"
                    data-bs-toggle="collapse"
                    href="#collapseExample"
                    role="button"
                    aria-expanded="false"
                    aria-controls="collapseExample"
                  >
                    Show Retention filters
                  </a>
                </div>
                <div class="collapse" id="collapseExample">
                  <div class="d-flex pt-3">
                    <div class="flex-fill">
                      <div class="fw-bold">Sign-ins</div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck1"
                        />
                        <label class="form-check-label" for="defaultCheck1"> High </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck2"
                        />
                        <label class="form-check-label" for="defaultCheck2"> Average </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck2"
                        />
                        <label class="form-check-label" for="defaultCheck2"> Low </label>
                      </div>
                    </div>
                    <div class="flex-fill">
                      <div class="fw-bold">Activity</div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck3"
                        />
                        <label class="form-check-label" for="defaultCheck3"> High </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck4"
                        />
                        <label class="form-check-label" for="defaultCheck4"> Average </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck5"
                        />
                        <label class="form-check-label" for="defaultCheck5"> Low </label>
                      </div>
                    </div>
                    <div class="flex-fill">
                      <div class="fw-bold">Assignments</div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck6"
                        />
                        <label class="form-check-label" for="defaultCheck6"> High </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck7"
                        />
                        <label class="form-check-label" for="defaultCheck7"> Average </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck8"
                        />
                        <label class="form-check-label" for="defaultCheck8"> Low </label>
                      </div>
                    </div>
                    <div class="flex-fill">
                      <div class="fw-bold">Grades</div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck9"
                        />
                        <label class="form-check-label" for="defaultCheck9"> High </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck10"
                        />
                        <label class="form-check-label" for="defaultCheck10"> Average </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="defaultCheck11"
                        />
                        <label class="form-check-label" for="defaultCheck11"> Low </label>
                      </div>
                    </div>
                  </div>
                  <ul class="mt-3 mb-0 list-inline">
                    <li class="list-inline-item"><strong>Low</strong> -5 to -3</li>
                    <li class="list-inline-item"><strong>Average</strong> -2.9 to +2.9</li>
                    <li class="list-inline-item"><strong>High</strong> +3 to +5</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row my-4">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0">
              <h3
                class="h6 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
              >
                My Cases
              </h3>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div class="table-responsive">
                <table class="table mb-0">
                  <thead class="small">
                    <tr>
                      <th scope="col" class="ps-0">Name</th>
                      <th scope="col" class="text-nowrap">Student Number</th>
                      <th scope="col">Priority</th>
                      <th scope="col">Class</th>
                      <th scope="col" class="text-nowrap">Enroll Status</th>
                      <th scope="col">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in students" :key="item.SystemKey" class="bg-light-hover">
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
                          <div class="flex-fill">
                            <div class="text-nowrap">
                              <span>
                                {{ item.student_preferred_last_name }},
                                {{ item.student_preferred_first_name }}
                              </span>
                              <span
                                class="badge rounded-pill border border-muted text-dark small"
                                >{{ item.gender }}</span
                              >
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
                          >{{ item.student_number }}</router-link
                        >
                      </td>
                      <td>top/middle/bottom {{ item.retention.priority }}</td>
                      <td>{{ item.class_desc }}</td>
                      <td>{{ item.enrollment_status_desc }}</td>
                      <td>Active/Inactive</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div v-show="!isLoading" class="card-footer bg-white p-4">
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
import TableLoading from '../components/table-loading.vue';
import Pagination from 'v-pagination-3';
import MyPagination from '../components/pagination.vue';
import Layout from '../layout.vue';
import Search from '../components/search.vue';
import dataMixin from '../mixins/data_mixin.js';

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    pagination: Pagination,
    search: Search,
    'table-loading': TableLoading,
  },
  created: function () {
    setTimeout(this.loadStudentList, 3000);
    //this.loadStudentList();

    this.searchOption = this.searchRadioOptions[0];
  },
  data() {
    return {
      pageTitle: 'Caseload',

      isLoading: true,

      // data
      students: [],
      // pagination
      studentsCount: 0,
      currentPage: 1,
      pageSize: 10,
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

        this.isLoading = false;
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
    showResults: function () {
      this.isLoading = false;
    },
  },
  mounted() {
    //setTimeout(this.showResults, 4000);
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
