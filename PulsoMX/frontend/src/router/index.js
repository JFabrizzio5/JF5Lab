import { createRouter, createWebHistory } from 'vue-router'

const Landing    = () => import('../views/LandingView.vue')
const Demo       = () => import('../views/DemoView.vue')
const Dashboard  = () => import('../views/DashboardView.vue')
const Members    = () => import('../views/MembersView.vue')
const Classes    = () => import('../views/ClassesView.vue')
const Checkin    = () => import('../views/CheckinView.vue')
const Billing    = () => import('../views/BillingView.vue')
const Success    = () => import('../views/BillingSuccessView.vue')

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Landing },
    { path: '/demo', component: Demo },
    { path: '/billing/success', component: Success },
    { path: '/billing/cancel', component: Success, props: { canceled: true } },
    { path: '/app/dashboard', component: Dashboard, meta: { layout: 'app' } },
    { path: '/app/members',   component: Members,   meta: { layout: 'app' } },
    { path: '/app/classes',   component: Classes,   meta: { layout: 'app' } },
    { path: '/app/checkin',   component: Checkin,   meta: { layout: 'app' } },
    { path: '/app/billing',   component: Billing,   meta: { layout: 'app' } },
  ]
})
