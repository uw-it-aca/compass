import { createWebHistory, createRouter } from 'vue-router';
import { trackRouter } from "vue-gtag-next";

// page components
import Home from '../pages/home.vue';
import Results from '../pages/results.vue';
import Caseload from '../pages/caseload.vue';
import Student from '../pages/student.vue';


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    pathToRegexpOptions: { strict: true },
    props: true
  },
  {
    path: '/results',
    name: 'Results',
    component: Results,
    pathToRegexpOptions: { strict: true },
    props: true
  },
  {
    path: '/caseload',
    name: 'Caseload',
    component: Caseload,
    pathToRegexpOptions: { strict: true },
    props: true
  },
  {
    path: '/student/:id?',
    name: 'Student',
    component: Student,
    pathToRegexpOptions: { strict: true },
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
});

// add router tracking to vue-gtag-next
trackRouter(router);

export default router;
