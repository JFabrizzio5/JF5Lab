import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { public: true } },
  { path: '/register', component: () => import('../views/RegisterView.vue'), meta: { public: true } },
  { path: '/', component: () => import('../views/LandingView.vue'), meta: { public: true } },
  { path: '/dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/properties', component: () => import('../views/PropertiesView.vue') },
  { path: '/tenants', component: () => import('../views/TenantsView.vue') },
  { path: '/contracts', component: () => import('../views/ContractsView.vue') },
  { path: '/payments', component: () => import('../views/PaymentsView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (!to.meta.public && !token) return '/login'
  if (to.meta.public && token && to.path !== '/') return '/dashboard'
})

export default router
