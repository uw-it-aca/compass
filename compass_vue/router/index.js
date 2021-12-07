import { createWebHistory, createRouter } from 'vue-router';

// page components
import Home from '../pages/home.vue';
import Student from '../pages/student.vue';

const routes = [
  {
    path: '/',
    redirect: '/adviser/javerage'
  },
  {
    path: '/adviser/:netid?',
    name: 'Adviser',
    component: Home,
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

export default router;
