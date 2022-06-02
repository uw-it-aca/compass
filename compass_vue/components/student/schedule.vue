<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Schedule (sws)</axdd-card-heading>
    </template>
    <template #body>
      <axdd-tabs :tabs-id="'schedule'">
        <template #items>
          <axdd-tab-item
            :tabs-id="'schedule'"
            :panel-id="'current'"
            :active-tab="true"
            >Current</axdd-tab-item
          >
          <axdd-tab-item :tabs-id="'schedule'" :panel-id="'next'"
            >Next</axdd-tab-item
          >
          <axdd-tab-item :tabs-id="'schedule'" :panel-id="'after'"
            >After</axdd-tab-item
          >
          <axdd-tab-item :tabs-id="'schedule'" :panel-id="'further'"
            >Further</axdd-tab-item
          >
        </template>
        <template #panels>
          <axdd-tab-panel :panel-id="'current'" :active-panel="true">
            <p>
              <strong>current</strong> Lorem ipsum dolor sit amet consectetur
              adipisicing elit. Id aperiam dolores harum doloribus libero
              sapiente corrupti sint rerum incidunt. Qui quia hic ipsam culpa
              laudantium delectus sapiente tempore, eveniet modi.
            </p>
          </axdd-tab-panel>
          <axdd-tab-panel :panel-id="'next'">
            <p>
              <strong>next</strong> Lorem ipsum dolor sit amet consectetur
              adipisicing elit. Repellendus iste, expedita, vitae voluptatibus
              nobis amet eligendi consectetur repudiandae aut ut vel? Amet
              nesciunt culpa non molestiae enim consequuntur provident sit.
            </p>
          </axdd-tab-panel>
          <axdd-tab-panel :panel-id="'after'">
            <p>
              <strong>after</strong>, ipsum dolor sit amet consectetur
              adipisicing elit. Doloremque est totam, ipsa corporis molestias,
              temporibus maiores ex enim error perferendis ad veritatis tenetur
              dicta laboriosam nam eaque eum minus distinctio.
            </p>
          </axdd-tab-panel>
          <axdd-tab-panel :panel-id="'further'">
            <p>
              <strong>further</strong>, ipsum dolor sit amet consectetur
              adipisicing elit. Doloremque est totam, ipsa corporis molestias,
              temporibus maiores ex enim error perferendis ad veritatis tenetur
              dicta laboriosam nam eaque eum minus distinctio.
            </p>
          </axdd-tab-panel>
        </template>
      </axdd-tabs>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading, Tabs, TabItem, TabPanel } from "axdd-components";

export default {
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-tabs": Tabs,
    "axdd-tab-item": TabItem,
    "axdd-tab-panel": TabPanel,
  },
  data() {
    return {};
  },
};
</script>
