import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/LandingView.vue') },
  { path: '/login', component: () => import('../views/LoginView.vue') },
  { path: '/register', component: () => import('../views/RegisterView.vue') },

  // Public convention pages
  { path: '/c/:slug', component: () => import('../views/public/ConventionPublicView.vue'), meta: { landing: true } },
  { path: '/c/:slug/checkout', component: () => import('../views/public/TicketCheckoutView.vue'), meta: { landing: true } },

  // Organizer pages
  {
    path: '/organizer',
    component: () => import('../views/organizer/DashboardView.vue'),
    meta: { requiresAuth: true, role: 'organizer' },
    children: []
  },
  { path: '/organizer/dashboard', component: () => import('../views/organizer/DashboardView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/settings', component: () => import('../views/organizer/ConventionSettingsView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/stages', component: () => import('../views/organizer/StagesView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/speakers', component: () => import('../views/organizer/SpeakersView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/stands', component: () => import('../views/organizer/StandsView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/sponsors', component: () => import('../views/organizer/SponsorsView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/tickets', component: () => import('../views/organizer/TicketsView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/tournaments', component: () => import('../views/organizer/TournamentsView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/attendees', component: () => import('../views/organizer/AttendeesView.vue'), meta: { requiresAuth: true, role: 'organizer' } },
  { path: '/organizer/payments', component: () => import('../views/organizer/PaymentsView.vue'), meta: { requiresAuth: true, role: 'organizer' } },

  // Admin pages
  { path: '/admin', component: () => import('../views/admin/AdminDashboard.vue'), meta: { requiresAuth: true, role: 'superadmin' } },
  { path: '/admin/conventions', component: () => import('../views/admin/AdminConventions.vue'), meta: { requiresAuth: true, role: 'superadmin' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.requiresAuth) {
    if (!token) return next('/login')
    if (to.meta.role === 'superadmin' && user?.role !== 'superadmin') return next('/')
    if (to.meta.role === 'organizer' && !['organizer', 'superadmin'].includes(user?.role)) return next('/')
  }
  next()
})

export default router
