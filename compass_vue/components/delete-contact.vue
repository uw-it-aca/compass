<template>
  <a
    role="button"
    class="btn text-nowrap"
    @click="deleteContact()"
    :class="[
      buttonType === 'button'
        ? 'btn-sm btn-danger text-danger rounded-3 px-3 py-2'
        : 'fs-9 btn-outline-gray text-danger rounded-3 px-2 py-1',
    ]"
  >
    <slot>Delete</slot>
  </a>

  <!-- delete contact confirm modal -->
</template>

<script>
import dataMixin from "@/mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  inject: ["mq"],
  emits: ["contactDeleted"],
  props: {
    buttonType: {
      type: String,
      required: true,
    },
    person: {
      type: Object,
      required: true,
    },
    contactId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {};
  },
  created() {},
  mounted() {},
  watch: {
    contact: {
      handler: function () {
        // Don't show 'required' errors until the user has tried to submit
        // then update on every form edit
      },
      deep: true,
    },
  },
  methods: {
    deleteContact() {
      alert("delete this!");
    },
  },
};
</script>
