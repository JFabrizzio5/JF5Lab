import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/LandingView.vue'), meta: { landing: true } },
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },

  // Public professional profiles (no auth required)
  { path: '/pro/:id', component: () => import('../views/ProPublicView.vue'), meta: { landing: true } },

  // Chat (client + freelancer)
  { path: '/chats', component: () => import('../views/ChatListView.vue'), meta: { auth: true, roles: ['client', 'freelancer', 'superadmin'] } },
  { path: '/chat/:room_id', component: () => import('../views/ChatView.vue'), meta: { auth: true, roles: ['client', 'freelancer', 'superadmin'] } },

  // Client
  { path: '/marketplace', component: () => import('../views/client/MarketplaceView.vue'), meta: { auth: true, roles: ['client'] } },
  { path: '/home', component: () => import('../views/client/HomeView.vue'), meta: { auth: true, roles: ['client'] } },
  { path: '/professional/:id', component: () => import('../views/client/ProfessionalDetailView.vue'), meta: { auth: true, roles: ['client'] } },
  { path: '/my-bookings', component: () => import('../views/client/MyBookingsView.vue'), meta: { auth: true, roles: ['client'] } },

  // Freelancer
  { path: '/dashboard', component: () => import('../views/freelancer/FreelancerDashboard.vue'), meta: { auth: true, roles: ['freelancer'] } },
  { path: '/my-profile', component: () => import('../views/freelancer/MyProfileView.vue'), meta: { auth: true, roles: ['freelancer'] } },
  { path: '/subscriptions', component: () => import('../views/freelancer/SubscriptionsView.vue'), meta: { auth: true, roles: ['freelancer'] } },

  // Admin
  { path: '/admin', component: () => import('../views/admin/AdminDashboard.vue'), meta: { auth: true, roles: ['superadmin'] } },
  { path: '/admin/users', component: () => import('../views/admin/AdminUsers.vue'), meta: { auth: true, roles: ['superadmin'] } },
  { path: '/admin/categories', component: () => import('../views/admin/AdminCategories.vue'), meta: { auth: true, roles: ['superadmin'] } },
  { path: '/admin/bookings', component: () => import('../views/admin/AdminBookings.vue'), meta: { auth: true, roles: ['superadmin'] } },

  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

function getSession() {
  const token = localStorage.getItem('servilink_token')
  const user = JSON.parse(localStorage.getItem('servilink_user') || 'null')
  return { token, user, isLoggedIn: !!token }
}

const roleHome = { superadmin: '/admin', freelancer: '/dashboard', client: '/marketplace' }

router.beforeEach((to, from, next) => {
  if (to.meta.landing) return next()

  const { isLoggedIn, user } = getSession()

  if (to.meta.guest && isLoggedIn) {
    return next(roleHome[user?.role] || '/marketplace')
  }

  if (to.meta.auth && !isLoggedIn) return next('/login')

  if (to.meta.roles && user && !to.meta.roles.includes(user.role)) {
    return next(roleHome[user.role] || '/login')
  }

  next()
})

export default router
