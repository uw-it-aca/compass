// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-danger p-4 rounded-3">
            <div class="row">
              <div class="col text-white">
                this is for admins only... you do not have proper authorization
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "Reports",
      isLoading: true,
    };
  },
};
</script>

<style lang="scss"></style>
