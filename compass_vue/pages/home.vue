// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col">
          <!-- MARK: card component -->
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0 d-flex justify-content-between">
              <h3
                class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
              >
                Today, {{ getToday() }}
              </h3>
              <div>

                <div class="input-group">
                  <input
                    type="text"
                    class="form-control form-control-sm"
                    placeholder="Search all students..."
                    aria-label="Recipient's username"
                    aria-describedby="button-addon2"
                  />
                  <button
                    class="btn btn-sm btn-outline-dark-purple btn-outline-secondary"
                    type="button"
                    id="button-addon2"
                  >Search</button>
                </div>

              </div>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <table-display></table-display>
            </div>
          </div>
        </div>
      </div>

    </template>
  </layout>
</template>

<script>
import { markRaw } from 'vue';
import Search from '../components/search.vue';
import TableLoading from '../components/table-loading.vue';
import TableDisplay from '../components/table-display.vue';
import Pagination from 'v-pagination-3';
import MyPagination from '../components/pagination.vue';
import Layout from '../layout.vue';
import dataMixin from '../mixins/data_mixin.js';
import { getToday, getYesterday } from '../helpers/utils';

export default {
  mixins: [dataMixin],
  components: {
    'layout': Layout,
    'search': Search,
    'pagination': Pagination,
    'table-loading': TableLoading,
    'table-display': TableDisplay
  },
  created: function () {
    this.loadStudentList();
  },
  data() {
    return {
      pageTitle: 'Contacts',

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
    };
  },
  computed: {
    paginationOptions: function () {
      return {
        offset: this.pageSize * (this.currentPage - 1),
        limit: this.pageSize,
      };
    },
    numPages: function () {
      let page = Math.ceil(this.studentsCount / this.pageSize);
      return page > 0 ? page : 1;
    },
  },
  methods: {
    getToday,
    getYesterday,
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
