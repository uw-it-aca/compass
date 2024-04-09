<template>
  <div class="d-flex">
    <div class="me-2">
      <div v-lazyload class="rounded-circle border border-light border-3">
        <img
          :data-url="person.photo_url"
          @error="$event.target.src = '/static/compass/img/placeholder.png'"
          class="img-profile rounded-circle border bg-light border-white border-2"
        />
      </div>
    </div>
    <div class="flex-fill">
      <div class="">
        <div class="me-2">
          <div>{{ person.display_name }}</div>
          <div class="small text-muted text-capitalize">
            <template v-if="person.pronouns">
              {{ person.pronouns }}
            </template>
          </div>
        </div>
      </div>
      <div class="text-secondary small">
        <router-link :to="{ path: '/student/' + person.student_number }"
          >{{ person.student_number }} </router-link
        >,
        <router-link :to="{ path: '/student/' + person.uwnetid }"
          >{{ person.uwnetid }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import LazyLoad from "@/directives/lazyload";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  directives: {
    lazyload: LazyLoad,
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
