<template>
  <div class="d-flex">
    <div class="me-2">
      <div class="rounded-circle border border-light border-3">
        <img
          :src="person.photo_url"
          @error="$event.target.src = '/static/compass/img/placeholder.jpeg'"
          style="min-width: 60px; width: 60px"
          class="img-fluid rounded-circle border border-white border-2"
        />
      </div>
    </div>
    <div class="flex-fill">
      <div class="text-nowrap">
        <span class="me-2">
          <router-link :to="{ path: '/student/' + person.uwnetid }"
            >{{ person.display_name }} ({{ person.uwnetid }})</router-link
          >
        </span>
        <span
          v-if="person.student.gender === 'M'"
          class="badge rounded-pill border border-muted text-dark"
          >M</span
        >
        <span
          v-if="person.student.gender === 'F'"
          class="badge rounded-pill border border-muted text-dark"
          >F</span
        >

        <span
          v-if="person.student.sports.length > 0"
          class="badge rounded-pill border border-muted text-dark"
        >
          <i class="bi bi-trophy-fill text-purple"></i> Sport:
          <span
            v-for="(sport, index) in person.student.sports"
            :key="sport.code"
          >
            {{ sport.sport_code }}
            <span v-if="index + 1 < person.student.sports.length">, </span>
          </span>
        </span>
      </div>
      <div class="text-secondary">
        {{ person.student.student_number }}, {{ person.student.class_desc }},
        <template v-if="person.student.registered_in_quarter">
          Registered
        </template>
        <template v-else> Unregistered </template>
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
