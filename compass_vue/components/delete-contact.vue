<template>
  <a
    role="button"
    class="btn btn-sm fs-9 btn-outline-danger rounded-3 px-2 py-1 ms-1"
    @click="deleteContact()"
  >
    <slot>Delete</slot>
  </a>

  <!-- delete contact confirm modal -->
</template>

<script>
import { deleteStudentContact } from "@/utils/data";

export default {
  inject: ["mq"],
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
  emits: ["contactDeleted"],
  setup() {
    return {
      deleteStudentContact,
    };
  },
  data() {
    return {};
  },
  watch: {
    contact: {
      handler: function () {
        // Don't show 'required' errors until the user has tried to submit
        // then update on every form edit
      },
      deep: true,
    },
  },
  created() {},
  mounted() {},
  methods: {
    deleteContact() {
      let vue = this;
      this.deleteStudentContact(this.contactId)
        .then(() => {
          vue.$emit("contactDeleted");
        })
        .catch((error) => {
          alert(error.data.message);
        });
    },
  },
};
</script>
