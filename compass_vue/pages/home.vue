// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>

      <div class="row my-4">
        <div class="col-5 offset-7">
          <search></search>
        </div>
      </div>

      <h1 class="h4 my-4 text-dark">{{ pageTitle }}</h1>

      <div class="row">
        <div class="col">

          <!-- MARK: card component -->
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0 d-flex justify-content-between">
              <h3 class="h6 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige">
                Today
              </h3>
              <div>{{ getToday() }}</div>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">recent students</div>
          </div>

        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0 d-flex justify-content-between">
              <h3 class="h6 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige">
                Tomorrow
              </h3>
              <div>{{ getTomorrow() }}</div>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">recent students</div>
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
import Search from '../components/search.vue';
import Layout from '../layout.vue';
import dataMixin from '../mixins/data_mixin.js';
import { getToday, getTomorrow } from '../helpers/utils';

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    pagination: Pagination,
    search: Search,
    'table-loading': TableLoading,
  },
  created: function () {
    this.loadStudentList();
    this.searchOption = this.searchRadioOptions[0];
  },
  data() {
    return {
      pageTitle: 'Appointments',

      // loading
      isLoading: true,
      today: 'bal',
      // data
      students: [],
      // pagination
      studentsCount: 20,
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
    getToday,
    getTomorrow,
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
    showResults: function () {
      this.isLoading = false;
    },
  },
  mounted() {
    setTimeout(this.showResults, 4000);
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
