// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col">
          <div class="bg-gray p-4 rounded-3">
            <div class="small lh-lg">
              <div class="d-inline me-3 text-nowrap fw-bold">Find student by:</div>
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
            <div class="input-group input-group-sm mb-0 w-50">
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
                v-on:click="clickButton"
              >
                GO
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0 d-flex justify-content-between">
              <h3
                class="h6 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
              >
                Results
              </h3>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div v-if="hasResults">12 search results</div>
              <div v-else>no results yet. begin by searching.</div>
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
      pageTitle: 'Search',

      // loading
      isLoading: false,
      hasResults: false,

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
      this.hasResults = true;
    },
    clickButton: function () {
      // show loading again
      if (this.isLoading == false) {
        this.isLoading = true;
      }

      setTimeout(this.showResults, 3000);
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
