<template>
  <div class="text-light">
    <ul class="nav flex-column">
      <li class="nav-item mb-1 bg-dark-purple-hover rounded">
        <router-link :to="'/'" class="nav-link text-gray d-block px-2 py-1"
          ><i class="bi bi-house-door-fill me-2"></i>Home</router-link
        >
      </li>
      <li class="nav-item mb-2 bg-dark-purple-hover rounded">
        <router-link :to="'/javerage/caseload'" class="nav-link text-gray d-block px-2 py-1"
          ><i class="bi bi-briefcase-fill me-2"></i>Caseload</router-link
        >
      </li>
      <li aria-hidden="true" class="nav-item mb-2">
        <a href="#" class="nav-link disabled text-gray d-block p-0 internal-link"
          ><hr class="m-0 bg-gray" />
          <span class="visually-hidden"> Navigation separator</span></a
        >
      </li>
    </ul>

    <p v-show="$route.name == 'Caseload'" class="text-dark bg-beige rounded p-3 small">
        Welcome to <strong>caseloads</strong>... Lorem ipsum dolor, sit amet consectetur adipisicing elit. Cum voluptatibus,
        laborum inventore magni, dolore quod incidunt error reiciendis nesciunt ex atque, amet culpa
        quia ullam sit. Deleniti id at odit!
      </p>

  </div>
</template>

<style lang="scss"></style>
