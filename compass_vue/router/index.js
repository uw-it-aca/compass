import { createWebHistory, createRouter } from "vue-router";

// page components
import Home from '../pages/home.vue';
import Student from '../pages/student.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/student/:id?",
    name: "Student",
    component: Student,
    pathToRegexpOptions: { strict: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
