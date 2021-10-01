<template>
  <div class="VuePagination" :class="props.theme.wrapper">
    <nav :class="props.theme.nav" aria-label="Page navigation example">
      <ul
        v-show="props.showPagination"
        :class="props.theme.list"
        class="pagination pagination-sm justify-content-end m-0"
      >
        <!--<li v-if="props.hasEdgeNav" :class='props.theme.firstPage' @click="props.setFirstPage">
          <button type="button" v-bind="props.firstPageProps">{{ props.texts.first }}</button>
        </li>-->

        <!--<li v-if="props.hasChunksNav" :class="props.theme.prevChunk" @click="props.setPrevChunk">
          <button type="button" v-bind="props.prevChunkProps">{{ props.texts.prevChunk }}</button>
        </li>-->

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

        <!--<li v-if="props.hasChunksNav" :class="props.theme.nextChunk" @click="props.setNextChunk">
          <button type="button" v-bind="props.nextChunkProps">{{ props.texts.nextChunk }}</button>
        </li>

        <li v-if="props.hasEdgeNav" :class="props.theme.lastPage" @click="props.setLastPage">
          <button type="button" v-bind="props.lastPageProps">{{ props.texts.last }}</button>
        </li>-->
      </ul>
      <!--<div v-show="props.hasRecords" :class="props.theme.count">{{ props.count }}</div>-->
    </nav>
  </div>
</template>

<script>
export default {
  name: 'MyPagination',
  props: ['props'],
};
</script>
