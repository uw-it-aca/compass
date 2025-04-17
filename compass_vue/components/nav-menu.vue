<template>
  <div class="text-light">
    <ul class="nav flex-column mb-4">
      <li class="nav-item mb-1 position-relative">
        <BLink
          :to="'/checkins'"
          class="d-flex justify-content-between nav-link rounded-3 text-light bg-white-hover bg-opacity-10-hover"
          exact-active-class="bg-white bg-opacity-10"
        >
          <span
            ><i class="bi bi-calendar-check me-3 text-white text-opacity-50"></i
            >Check-Ins</span
          >
        </BLink>
      </li>
      <li class="nav-item mb-1">
        <BLink
          :to="'/caseload'"
          class="d-flex justify-content-between nav-link rounded-3 text-light bg-white-hover bg-opacity-10-hover"
          exact-active-class="bg-white bg-opacity-10"
        >
          <span
            ><i class="bi bi-people-fill me-3 text-white text-opacity-50"></i
            >Caseload</span
          ></BLink
        >
      </li>

      <li v-show="userRoles.includes(Role.Manager)" class="nav-item mb-1">
        <BLink
          :to="'/affiliations'"
          class="d-flex justify-content-between nav-link rounded-3 text-light bg-white-hover bg-opacity-10-hover"
          exact-active-class="bg-white bg-opacity-10"
          ><span
            ><i class="bi bi-cart4 me-3 text-white text-opacity-50"></i>Batch
            Affiliations</span
          ></BLink
        >
      </li>
      <li v-if="false" aria-hidden="true" class="nav-item mt-1 mb-2">
        <BLink
          :to="'/reports'"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          :class="
            $route.path.includes('/reports') ? 'bg-dark-purple rounded-3' : ''
          "
          ><i class="bi bi-bar-chart-line-fill me-2"></i>Reports</BLink
        >
      </li>
    </ul>
  </div>
</template>

<script>
import { Role } from "@/utils/roles";
import { BLink } from "bootstrap-vue-next";

export default {
  components: { BLink },
  props: {
    userRoles: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      Role: Role,
    };
  },
};
</script>
