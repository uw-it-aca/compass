// home.vue

<template>
  <layout :page-title="'Home'">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col-5 offset-7">
          <search></search>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-3">
              <h3 class="h6 m-0 text-uppercase fw-bold text-uppercase text-dark-beige">
                Search Results
              </h3>
            </div>
            <div v-if="isLoading" class="card-body p-4 pt-0 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4 pt-0 table-responsive-md">search results</div>
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
import Search from '../components/search.vue';
import Layout from '../layout.vue';
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
    //this.loadStudentList();
    this.searchOption = this.searchRadioOptions[0];
  },
  data() {
    return {
      // loading
      isLoading: true,

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
  },
  methods: {
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
    setTimeout(this.showResults, 3000);
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
