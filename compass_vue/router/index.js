import { createWebHistory, createRouter } from "vue-router";

// page components
import Home from '../pages/home.vue';
import Student from '../pages/student.vue';
import NotFound from '../pages/404.vue';

const routes = [
  { path: '/:pathMatch(.*)*', component: NotFound },
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
