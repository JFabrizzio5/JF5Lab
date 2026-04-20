import { createRouter, createWebHistory } from 'vue-router'

const LandingView = () => import('../views/LandingView.vue')
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const VendorPublicView = () => import('../views/public/VendorPublicView.vue')
const DashboardView = () => import('../views/vendor/DashboardView.vue')
const ItemsView = () => import('../views/vendor/ItemsView.vue')
const AvailabilityView = () => import('../views/vendor/AvailabilityView.vue')
const BookingsView = () => import('../views/vendor/BookingsView.vue')
const SettingsView = () => import('../views/vendor/SettingsView.vue')
const PaymentsView = () => import('../views/vendor/PaymentsView.vue')
const AdminDashboard = () => import('../views/admin/AdminDashboard.vue')
const AdminVendors = () => import('../views/admin/AdminVendors.vue')

const routes = [
  { path: '/', component: LandingView, meta: { landing: true } },
  { path: '/r/:slug', component: VendorPublicView, meta: { landing: true } },
  { path: '/login', component: LoginView, meta: { guest: true } },
  { path: '/register', component: RegisterView, meta: { guest: true } },
  { path: '/vendor/dashboard', component: DashboardView, meta: { auth: true, roles: ['vendor'] } },
  { path: '/vendor/items', component: ItemsView, meta: { auth: true, roles: ['vendor'] } },
  { path: '/vendor/availability', component: AvailabilityView, meta: { auth: true, roles: ['vendor'] } },
  { path: '/vendor/bookings', component: BookingsView, meta: { auth: true, roles: ['vendor'] } },
  { path: '/vendor/settings', component: SettingsView, meta: { auth: true, roles: ['vendor'] } },
  { path: '/vendor/payments', component: PaymentsView, meta: { auth: true, roles: ['vendor'] } },
  { path: '/admin', component: AdminDashboard, meta: { auth: true, roles: ['superadmin'] } },
  { path: '/admin/vendors', component: AdminVendors, meta: { auth: true, roles: ['superadmin'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

const roleHome = {
  superadmin: '/admin',
  vendor: '/vendor/dashboard',
  customer: '/',
}

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('rentame_token')
  const userRaw = localStorage.getItem('rentame_user')
  const user = userRaw ? JSON.parse(userRaw) : null
  const role = user?.role || null

  if (to.meta.auth) {
    if (!token || !user) {
      return next('/login')
    }
    if (to.meta.roles && !to.meta.roles.includes(role)) {
      return next(roleHome[role] || '/')
    }
  }

  if (to.meta.guest && token && user) {
    return next(roleHome[role] || '/')
  }

  next()
})

export default router
