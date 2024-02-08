<template>
  <slot></slot>
  <tr class="border-0">
    <td colspan="100%" class="border-0">
      <nav aria-label="Page navigation example">
        <ul class="pagination pagination-sm justify-content-center m-0">
          <li class="page-item">
            <a
              class="page-link"
              :class="currentPage == 1 ? 'disabled' : ''"
              href="#"
              role="button"
              @click="$emit('changePage', currentPage - 1)"
              >Previous</a
            >
          </li>
          <template v-for="page in pages" :key="page">
            <li class="page-item">
              <a
                class="page-link"
                :class="page == currentPage ? 'active' : ''"
                href="#"
                role="button"
                @click="$emit('changePage', page)"
                >{{ page }}</a
              >
            </li>
          </template>
          <li class="page-item">
            <a
              class="page-link"
              :class="currentPage == pageCount ? 'disabled' : ''"
              href="#"
              role="button"
              @click="$emit('changePage', currentPage + 1)"
              >Next</a
            >
          </li>
        </ul>
      </nav>
    </td>
  </tr>
</template>
<script>
import { computed } from "vue";

export default {
  //note this emit back to parent
  emits: ["changePage"],
  props: {
    //changed to just get the length of the list
    itemCount: {
      type: Number,
      required: true,
    },
    itemsPerPage: {
      type: Number,
      default: 10,
    },
    currentPage: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const pageCount = computed(() =>
      Math.ceil(props.itemCount / props.itemsPerPage)
    );

    const pages = computed(() => {
      return Array.from({ length: pageCount.value }, (_, i) => i + 1);
    });

    return {
      pageCount,
      pages,
    };
  },
  data() {
    return {};
  },
};
</script>
