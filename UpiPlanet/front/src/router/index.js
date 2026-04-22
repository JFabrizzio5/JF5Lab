import { createRouter, createWebHistory } from 'vue-router';
import LandingView from '../views/LandingView.vue';
import AuthView from '../views/AuthView.vue';
import FeedView from '../views/FeedView.vue';
import ProfileView from '../views/ProfileView.vue';
import ExploreView from '../views/ExploreView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LandingView, name: 'landing' },
    { path: '/auth', component: AuthView, name: 'auth' },
    { path: '/feed', component: FeedView, name: 'feed' },
    { path: '/explore', component: ExploreView, name: 'explore' },
    { path: '/u/:username', component: ProfileView, name: 'profile' }
  ]
});

export default router;
