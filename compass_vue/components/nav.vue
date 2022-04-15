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
    </ul>

    <p
      v-show="$route.path == '/'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>home</strong>... Lorem ipsum dolor, sit amet consectetur adipisicing
      elit. Cum voluptatibus, laborum inventore magni, dolore quod incidunt error reiciendis
      nesciunt ex atque, amet culpa quia ullam sit. Deleniti id at odit!
    </p>

    <p
      v-show="$route.path == '/caseload'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to <strong>caseloads</strong>... Lorem ipsum dolor, sit amet consectetur adipisicing
      elit. Cum voluptatibus, laborum inventore magni, dolore quod incidunt error reiciendis
      nesciunt ex atque, amet culpa quia ullam sit. Deleniti id at odit!
    </p>
    <br /><br />
  </div>
</template>

<style lang="scss"></style>
