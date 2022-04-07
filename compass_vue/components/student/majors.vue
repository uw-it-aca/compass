<template>
  <div class="card border-light-gray shadow-sm rounded-3 mb-4">
    <div class="card-header bg-white border-0 p-4 pb-0">
      <h2
        class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
      >Major</h2>
    </div>
    <div class="card-body p-4">
      <ul>
        <li>
          Accepted:
          <span v-for="(major, index) in student.major" :key="index">
            {{ major.major_full_name }}
            <span v-if="index + 1 < student.major.length">,</span>
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    student: {
      type: Object,
      required: true,
    },
  },
  components: {
  },
  data() {
    return {};
  },
}
</script>
