import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import Home from "../pages/home.vue";
import Caseload from "../pages/caseload.vue";
import Student from "../pages/student.vue";
import Reports from "../pages/reports.vue";
import Settings from "../pages/settings.vue";

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
    path: "/reports",
    name: "Reports",
    component: Reports,
    pathToRegexpOptions: { strict: true },
    props: true,
    beforeEnter(to, from, next) {
      if (hasPermissions()) {
        // got to reports page
        next();
      } else {
        // redirect to 'not authorized' page in django
        window.location.replace("/not-authorized");
      }
    },
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    pathToRegexpOptions: { strict: true },
    props: true,
    beforeEnter(to, from, next) {
      if (hasPermissions()) {
        // got to reports page
        next();
      } else {
        // redirect to 'not authorized' page in django
        window.location.replace("/not-authorized");
      }
    },
  },
];

function hasPermissions() {
  // get user permssions from /api/endpoint
  return true;
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
