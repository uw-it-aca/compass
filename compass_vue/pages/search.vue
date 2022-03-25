// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4">
        <div class="col">
          <search></search>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0 d-flex justify-content-between">
              <h3
                class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
              >
                Results
              </h3>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div v-if="hasResults">
                <p>has 12 results</p>
                <table-display></table-display>
              </div>
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
import Search from '../components/search.vue';
import TableLoading from '../components/table-loading.vue';
import TableDisplay from '../components/table-display.vue';
import Pagination from 'v-pagination-3';
import Layout from '../layout.vue';
import dataMixin from '../mixins/data_mixin.js';

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    search: Search,
    pagination: Pagination,
    'table-loading': TableLoading,
    'table-display': TableDisplay,
  },
  data() {
    return {
      pageTitle: 'Search',

      // loading
      isLoading: false,
      hasResults: false,
    };
  },
  created: function () {
    console.log('created');

    if (this.isLoading == false) {
      this.isLoading = true;
    }
    setTimeout(this.showResults, 3000);
  },
  mounted: function () {
    console.log('mounted');
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
