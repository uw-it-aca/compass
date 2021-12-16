<template>
  <!-- layout.vue: this is where you override the layout -->
  <topbar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header></template>
    <template #bar v-if="true">
      <div class="bg-beige">
        <div class="container-xl py-2">
            <div class="w-25">
              <select class="form-select form-select-sm" aria-label="Default select example">
                <option value="1" selected>Undergraduate Academic Affairs</option>
                <option value="2">Office of Minority Affairs &amp; Diversity</option>
                <option value="3">International Students Services</option>
                <option value="4">Itegrated Social Sciences</option>
                <option value="5">College of Engineering</option>
                <option value="6">UW Tacoma</option>
                <option value="7">Intercollegiate Athletics</option>
              </select>
            </div>
        </div>
      </div>
    </template>
    <template #main>
      <!-- main section override -->
      <slot name="title">
        <h1>{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer>
      <div class="bg-dark">
        <div class="container-xl py-3 small">
          <div
            class="text-white font-weight-light"
          >Copyright &copy; {{ new Date().getFullYear() }} University of Washington</div>
        </div>
      </div>
    </template>
  </topbar>
</template>

<script>
import { Topbar } from 'axdd-components';

export default {
  name: 'Compass',
  components: {
    'topbar': Topbar,
  },
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: 'Compass',
      appRootUrl: '/',
      userName: 'javerage',
      signOutUrl: document.body.getAttribute('data-logout-url'),

      // automatically set year
      currentYear: new Date().getFullYear(),
    };
  },
};
</script>

<style lang="scss">
</style>
