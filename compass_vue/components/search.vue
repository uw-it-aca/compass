<template>
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
      v-on:click="showResults"
    >
      GO
    </button>
  </div>
</template>

<script>
import { markRaw } from 'vue';
import dataMixin from '../mixins/data_mixin.js';

export default {
  mixins: [dataMixin],
  components: {},
  created: function () {
    this.searchOption = this.searchRadioOptions[0];
  },
  data() {
    return {
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
    showResults: function() {
      this.$router.push('/results')
    }
  },
};
</script>

<style lang="scss"></style>
