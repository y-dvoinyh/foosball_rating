import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/IndexPage.vue')
      },
      {
        path: 'rating',
        component: () => import('pages/RatingPage.vue')
      },
      {
        path: 'leagues/:id',
        component: () => import('pages/LeaguePage.vue')
      },
      {
        path: 'tournaments/:id',
        component: () => import('pages/TournamentPage.vue')
      },
      {
        path: 'competitions/:id',
        component: () => import('pages/CompetitionPage.vue')
      },
      {
        path: 'players/:id',
        component: () => import('pages/PlayerProfilePage.vue')
      },
      {
        path: 'profile',
        component: () => import('pages/UserProfilePage.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: 'compare',
        component: () => import('pages/ComparePage.vue')
      },
      {
        path: 'events',
        component: () => import('pages/EventsPage.vue')
      },
      {
        path: 'playoff',
        component: () => import('pages/PlayoffBracketPage.vue')
      },
      {
        path: 'admin',
        component: () => import('pages/AdminPage.vue'),
        meta: {
          requiresAuth: true,
          requiresSuperuser: true
        }
      }
    ]
  }
];

export default routes;
