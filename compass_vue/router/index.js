import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import Home from "../pages/home.vue";
import Caseload from "../pages/caseload.vue";
import Student from "../pages/student.vue";
import Admin from "../pages/admin.vue";

const routes = [
  {
    path: "/",
    component: Home,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/caseload",
    name: "Caseload",
    component: Caseload,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/student/:id?",
    name: "Student",
    component: Student,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    pathToRegexpOptions: { strict: true },
    props: true,
    beforeEnter(to, from, next) {
      if (isAuthorized()) {
        // got to admin page
        next();
      } else {
        // go to 'not authorized'
        next("/not-authorized");
      }
    },
  },
];

function isAuthorized() {
  // get user?
  return false;
}

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// add router tracking to vue-gtag-next
trackRouter(router);

export default router;
