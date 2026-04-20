import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Landing', component: () => import('../views/LandingView.vue'), meta: { layout: 'none' } },
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue'), meta: { layout: 'none' } },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue'), meta: { layout: 'none' } },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/contacts', name: 'Contacts', component: () => import('../views/ContactsView.vue'), meta: { requiresAuth: true } },
  { path: '/deals', name: 'Deals', component: () => import('../views/DealsView.vue'), meta: { requiresAuth: true } },
  { path: '/content', name: 'Content', component: () => import('../views/ContentView.vue'), meta: { requiresAuth: true } },
  { path: '/templates', name: 'Templates', component: () => import('../views/TemplatesView.vue'), meta: { requiresAuth: true } },
  { path: '/chat', name: 'Chat', component: () => import('../views/ChatView.vue'), meta: { requiresAuth: true } },
  // Public market analysis report — no auth so the link can be shared.
  { path: '/analisis', name: 'MarketAnalysis', component: () => import('../views/MarketAnalysisView.vue'), meta: { layout: 'none' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem('hubos_token')
  if (to.meta.requiresAuth && !token) return next('/login')
  if ((to.path === '/login' || to.path === '/register') && token) return next('/dashboard')
  next()
})

export default router
