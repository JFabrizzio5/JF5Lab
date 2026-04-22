import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/presets', name: 'presets', component: () => import('../views/PresetsView.vue') },
  { path: '/editor', name: 'editor', component: () => import('../views/EditorView.vue') },
  { path: '/pricing', name: 'pricing', component: () => import('../views/PricingView.vue') }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
