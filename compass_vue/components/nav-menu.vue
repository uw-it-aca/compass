<template>
  <div class="text-light">
    <ul class="nav flex-column mb-5">
      <li class="nav-item mb-1">
        <router-link
          :to="'/'"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          :class="
            $route.path.includes('/checkins') ? 'bg-dark-purple rounded-3' : ''
          "
          ><i class="bi bi-calendar-check me-2"></i>Check-Ins</router-link
        >
      </li>
      <li class="nav-item mb-1">
        <router-link
          :to="'/caseload'"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          :class="
            $route.path.includes('/caseload') ? 'bg-dark-purple rounded-3' : ''
          "
          ><i class="bi bi-people-fill me-2"></i>Caseload</router-link
        >
      </li>

      <li v-show="userRoles.includes(Role.Manager)" aria-hidden="true" class="nav-item mt-1 mb-2">
        <a
          href="#"
          class="nav-link disabled text-gray d-block p-0 internal-link"
          >
          <span class="fs-8 text-secondary text-uppercase">Enrollment Services</span>
          <hr class="m-0 bg-gray" /></a
        >
      </li>

      <li v-show="false" class="nav-item mb-1">
        <router-link
          :to="'/reports'"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          :class="
            $route.path.includes('/reports') ? 'bg-dark-purple rounded-3' : ''
          "
          ><i class="bi bi-bar-chart-line-fill me-2"></i>Reports</router-link
        >
      </li>
      <li v-show="userRoles.includes(Role.Manager)" class="nav-item mb-1">
        <router-link
          :to="'/affiliations'"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          :class="
            $route.path.includes('/affiliations') ? 'bg-dark-purple rounded-3' : ''
          "
          ><i class="bi bi-cart4 me-2"></i>Batch Affiliations</router-link
        >
      </li>


      <li aria-hidden="true" class="nav-item mt-1 mb-2">
        <a
          href="#"
          class="nav-link disabled text-gray d-block p-0 internal-link"
          >
          <span class="fs-8 text-secondary text-uppercase">Advising Resources</span>
          <hr class="m-0 bg-gray" /></a
        >
      </li>

      <li class="nav-item mb-1">
        <a
          href="https://sdb.admin.uw.edu/sisAdvising/securid/overview.aspx"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          ><i class="bi bi-ear me-2"></i>Academic Records (EARS)</a
        >
      </li>
      <li class="nav-item mb-2">
        <a
          href="https://retention.uw.edu"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          ><i class="bi bi-bar-chart-fill me-2"></i>Retention Analytics (RAD)</a
        >
      </li>
    </ul>
  </div>
</template>

<script>
import { Role } from "@/utils/roles";

export default {
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
