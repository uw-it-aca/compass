<template>
  <div class="d-flex">
    <div class="me-2">
      <div class="rounded-circle border border-light border-3">
        <img
          :src="person.photo_url"
          @error="$event.target.src = '/static/compass/img/placeholder.png'"
          class="img-profile rounded-circle border bg-light border-white border-2"
        />
      </div>
    </div>
    <div class="flex-fill">
      <div class="text-nowrap">
        <span class="me-2">
          <router-link :to="{ path: '/student/' + person.uwnetid }"
            >{{ person.display_name }}
          </router-link>
          <span class="ms-2 text-muted"
            >(<template v-if="person.pronouns">
              {{ person.pronouns }}
            </template>
            <template v-else>not specified</template>)</span
          >
        </span>
      </div>
      <div class="text-secondary">
        {{ person.student.student_number }}, {{ person.uwnetid }}
      </div>
    </div>
  </div>
</template>

<script>
import { Card, CardHeading } from "axdd-components";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.img-profile {
  height: 45px;
  width: 45px;
  object-fit: cover;
  object-position: top;
}
</style>
