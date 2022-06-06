import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import Home from "../pages/home.vue";
import Caseload from "../pages/caseload.vue";
import Student from "../pages/student.vue";
import Reports from "../pages/reports.vue";
import Settings from "../pages/settings.vue";

// MARK: user roles
export const Role = {
  Super: "Super",
  Admin: "Admin",
  Support: "Support",
  User: "User",
};

const routes = [
  {
    path: "/",
    component: Home,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/caseload",
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
    meta: { authorize: [Role.Support] },
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/settings",
    component: Settings,
    meta: { authorize: [Role.Super, Role.Admin] },
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

  // TODO: get the authenticated users roles from api/endpoint
  let currentUser = { role: Role.User };

  // check if authorization is required for this route
  if (authorize) {
    // check to see if current user's role is authorized to view page
    if (authorize.length && !authorize.includes(currentUser.role)) {
      // redirect to 'not authorized' page in django
      window.location.replace("/not-authorized");
    }
  }
  next();
});

// add router tracking to vue-gtag-next
trackRouter(router);

export default router;
