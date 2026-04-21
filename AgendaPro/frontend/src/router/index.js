import { createRouter, createWebHistory } from 'vue-router'

const Landing     = () => import('../views/LandingView.vue')
const Demo        = () => import('../views/DemoView.vue')
const Dashboard   = () => import('../views/DashboardView.vue')
const Calendar    = () => import('../views/CalendarView.vue')
const Services    = () => import('../views/ServicesView.vue')
const Staff       = () => import('../views/StaffView.vue')
const Customers   = () => import('../views/CustomersView.vue')
const Billing     = () => import('../views/BillingView.vue')
const Success     = () => import('../views/BookingSuccessView.vue')
const Public      = () => import('../views/PublicBookingView.vue')

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Landing },
    { path: '/demo', component: Demo },
    { path: '/book/success', component: Success },
    { path: '/book/cancel', component: Success, props: { canceled: true } },
    { path: '/app/dashboard', component: Dashboard, meta: { layout: 'app' } },
    { path: '/app/calendar',  component: Calendar,  meta: { layout: 'app' } },
    { path: '/app/services',  component: Services,  meta: { layout: 'app' } },
    { path: '/app/staff',     component: Staff,     meta: { layout: 'app' } },
    { path: '/app/customers', component: Customers, meta: { layout: 'app' } },
    { path: '/app/billing',   component: Billing,   meta: { layout: 'app' } },
    { path: '/:slug', component: Public, props: true },
  ]
})
