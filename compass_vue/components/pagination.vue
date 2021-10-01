<template>
  <div class="VuePagination" :class="props.theme.wrapper" >

    <div v-show="props.hasRecords" class="small lh-lg text-end" :class="props.theme.count">{{ props.count }}</div>

    <nav :class="props.theme.nav" aria-label="Page navigation example">
      <ul
        v-show="props.showPagination"
        :class="props.theme.list"
        class="pagination pagination-sm justify-content-end m-0"
      >
        <li :class="props.theme.prev" @click="props.setPrevPage">
          <button type="button" v-bind="props.prevProps">
            <span aria-hidden="true">&laquo;</span>
          </button>
        </li>

        <li
          v-for="page in props.pages"
          :key="page"
          :class="props.pageClasses(page)"
          v-on="props.pageEvents(page)"
        >
          <button type="button" v-bind="props.aProps" :class="props.theme.link">{{ page }}</button>
        </li>

        <li :class="props.theme.next" @click="props.setNextPage">
          <button type="button" v-bind="props.nextProps">
            <span aria-hidden="true">&raquo;</span>
          </button>
        </li>
      </ul>
      <!---->
    </nav>
  </div>
</template>

<script>
export default {
  name: 'MyPagination',
  props: ['props'],
};
</script>
