import { route } from 'quasar/wrappers';
import {
  createMemoryHistory,
  createRouter,
  createWebHistory
} from 'vue-router';

import { useAuth } from 'src/composables/use-auth';
import routes from './routes';

export default route(() => {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : createWebHistory;

  const router = createRouter({
    history: createHistory(process.env.VUE_ROUTER_BASE),
    routes
  });

  router.beforeEach(async (to) => {
    const { state, isAuthenticated, restoreSession } = useAuth();

    if (!to.meta.requiresAuth && !to.meta.requiresSuperuser) {
      return true;
    }

    await restoreSession();

    if (to.meta.requiresAuth && !isAuthenticated.value) {
      return {
        path: '/',
        query: {
          login: '1',
          redirect: to.fullPath
        }
      };
    }

    if (to.meta.requiresSuperuser && !state.currentUser?.is_superuser) {
      return { path: '/' };
    }

    return true;
  });

  return router;
});
