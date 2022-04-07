<template>
  <div class="card border-light-gray shadow-sm rounded-3 mb-4">
    <div class="card-header border-0 bg-white p-4 pb-0">
      <h2
        class="h5 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
      >Schedule</h2>
    </div>
    <div class="card-body p-4">
      <axdd-tabs :tabs-id="'schedule'">
        <template #items>
          <axdd-tab-item :tabs-id="'schedule'" :panel-id="'current'" :active-tab="true">Current</axdd-tab-item>
          <axdd-tab-item :tabs-id="'schedule'" :panel-id="'next'">Next</axdd-tab-item>
          <axdd-tab-item :tabs-id="'schedule'" :panel-id="'after'">After</axdd-tab-item>
          <axdd-tab-item :tabs-id="'schedule'" :panel-id="'further'">Further</axdd-tab-item>
        </template>
        <template #panels>
          <axdd-tab-panel :panel-id="'current'" :active-panel="true">
            <p>
              <strong>current</strong> Lorem ipsum dolor sit amet consectetur adipisicing elit. Id aperiam
              dolores harum doloribus libero sapiente corrupti sint rerum incidunt. Qui
              quia hic ipsam culpa laudantium delectus sapiente tempore, eveniet modi.
            </p>
          </axdd-tab-panel>
          <axdd-tab-panel :panel-id="'next'">
            <p>
              <strong>next</strong> Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus
              iste, expedita, vitae voluptatibus nobis amet eligendi consectetur
              repudiandae aut ut vel? Amet nesciunt culpa non molestiae enim consequuntur
              provident sit.
            </p>
          </axdd-tab-panel>
          <axdd-tab-panel :panel-id="'after'">
            <p>
              <strong>after</strong>, ipsum dolor sit amet consectetur adipisicing elit. Doloremque est
              totam, ipsa corporis molestias, temporibus maiores ex enim error perferendis
              ad veritatis tenetur dicta laboriosam nam eaque eum minus distinctio.
            </p>
          </axdd-tab-panel>
          <axdd-tab-panel :panel-id="'further'">
            <p>
              <strong>further</strong>, ipsum dolor sit amet consectetur adipisicing elit. Doloremque est
              totam, ipsa corporis molestias, temporibus maiores ex enim error perferendis
              ad veritatis tenetur dicta laboriosam nam eaque eum minus distinctio.
            </p>
          </axdd-tab-panel>
        </template>
      </axdd-tabs>
    </div>
  </div>
</template>


<script>

import Tabs from '../../_components/tabs/tabs.vue';
import TabItem from '../../_components/tabs/item.vue';
import TabPanel from '../../_components/tabs/panel.vue';

export default {
  components: {
    'axdd-tabs': Tabs,
    'axdd-tab-item': TabItem,
    'axdd-tab-panel': TabPanel,
  },
  data() {
    return { };
  },
}

</script>
