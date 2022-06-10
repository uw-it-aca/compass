<template>
  <div class="text-light">
    <ul class="nav flex-column my-4">
      <li class="nav-item mb-1 bg-dark-purple-hover rounded">
        <router-link
          :to="'/'"
          active-class="bg-dark-purple rounded"
          class="nav-link text-gray d-block px-2 py-1"
          ><i class="bi bi-calendar-check me-2"></i>Contacts</router-link
        >
      </li>
      <li class="nav-item mb-2 bg-dark-purple-hover rounded">
        <router-link
          :to="'/caseload'"
          active-class="bg-dark-purple rounded"
          class="nav-link text-gray d-block px-2 py-1"
          ><i class="bi bi-people-fill me-2"></i>Caseload</router-link
        >
      </li>
      <li class="nav-item mb-2 bg-dark-purple-hover rounded">
        <router-link
          :to="'/reports'"
          active-class="bg-dark-purple rounded"
          class="nav-link text-gray d-block px-2 py-1"
          ><i class="bi bi-bar-chart-fill me-2"></i>Reports</router-link
        >
      </li>
      <li class="nav-item mb-2 bg-dark-purple-hover rounded">
        <router-link
          :to="'/settings'"
          active-class="bg-dark-purple rounded"
          class="nav-link text-gray d-block px-2 py-1"
          ><i class="bi bi-tools me-2"></i>Settings</router-link
        >
      </li>
      <!-- if admin or support -->
      <li aria-hidden="true" class="nav-item mb-2">
        <a
          href="#"
          class="nav-link disabled text-gray d-block p-0 internal-link"
          ><hr class="m-0 bg-gray" />
          <span class="visually-hidden">Navigation separator</span></a
        >
      </li>

      <li class="nav-item mb-2 bg-dark-purple-hover rounded">
        <router-link
          :to="'/support'"
          active-class="bg-dark-purple rounded"
          class="nav-link text-gray d-block px-2 py-1"
          ><i class="bi bi-question-diamond-fill me-2"></i>Support</router-link
        >
      </li>
    </ul>

    <p
      v-show="userRole === 'manager'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Your role <strong>{{ userRole }}</strong
      >... go forth and do admin related things!
    </p>

    <p
      v-show="$route.path == '/'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>home</strong>... Lorem ipsum dolor, sit amet
      consectetur adipisicing elit. Cum voluptatibus, laborum inventore magni,
      dolore quod incidunt error reiciendis nesciunt ex atque, amet culpa quia
      ullam sit. Deleniti id at odit!
    </p>

    <p
      v-show="$route.path == '/caseload'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>caseloads</strong>... Lorem ipsum dolor, sit amet
      consectetur adipisicing elit. Cum voluptatibus, laborum inventore magni,
      dolore quod incidunt error reiciendis nesciunt ex atque, amet culpa quia
      ullam sit. Deleniti id at odit!
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userRole: document.body.getAttribute("data-user-role"),
    };
  },
};
</script>
