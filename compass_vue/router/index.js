import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";
import { Role } from "../helpers/roles.js";

// page components
import CheckIn from "../pages/check-ins.vue";
import Caseload from "../pages/caseload.vue";
import Student from "../pages/student.vue";
import Reports from "../pages/reports.vue";
import Settings from "../pages/settings.vue";

const routes = [
  {
    path: "/",
    component: CheckIn,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/caseload/:id?",
    component: Caseload,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/student/:id?",
    component: Student,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/reports",
    component: Reports,
    meta: { authorize: [Role.Manager] },
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/settings",
    component: Settings,
    meta: { authorize: [Role.Manager] },
    pathToRegexpOptions: { strict: true },
    props: true,
  },
];

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

// MARK: implement route guards
router.beforeEach((to, from, next) => {
  // get the authorization settings from the meta field for the route
  const { authorize } = to.meta;

  // get the authenticated user role from django context
  let userRoles = document.body.getAttribute("data-user-role").split(',');
 
  // check if authorization is required for this route
  if (authorize) {
    // check to see if current user's role is authorized to view page
    if (authorize.length && !authorize.some((r) => userRoles.includes(r))) {
      // redirect to 'not authorized' page in django
      window.location.replace("/not-authorized");
    }
  }
  next();
});

// add router tracking to vue-gtag-next
trackRouter(router);

export default router;
