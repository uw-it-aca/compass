import { createWebHistory, createRouter } from "vue-router";
// vue-gtag-next track routing
import { trackRouter } from "vue-gtag-next";

import { Role } from "@/utils/roles";

// page components
import CheckIn from "@/pages/check-ins.vue";
import Caseload from "@/pages/caseload.vue";
import Student from "@/pages/student.vue";
import Reports from "@/pages/reports.vue";
import Affiliations from "@/pages/affiliations.vue";

const routes = [
  {
    path: "/",
    redirect: "/checkins",
  },
  {
    path: "/checkins/:id?",
    name: "checkins",
    component: CheckIn,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/caseload/:id?",
    name: "caseload",
    component: Caseload,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/student/:id?",
    name: "student",
    component: Student,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/reports",
    name: "reports",
    component: Reports,
    meta: { authorize: [Role.Manager] },
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/affiliations",
    name: "affiliations",
    component: Affiliations,
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
  let userRoles = document.body.getAttribute("data-user-role").split(",");

  // check if authorization is required for this route
  if (authorize) {
    // check to see if current user's role is authorized to view page
    if (authorize.length && !authorize.some((r) => userRoles.includes(r))) {
      // redirect to 'unauthorized' page in django/nginx
      window.location.replace("/unauthorized-user");
    }
  }
  next();
});

// add router tracking to vue-gtag-next
trackRouter(router);

export default router;
