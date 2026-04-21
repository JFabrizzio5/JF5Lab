import { createRouter, createWebHistory } from 'vue-router'

const Landing    = () => import('../views/LandingView.vue')
const Demo       = () => import('../views/DemoView.vue')
const Dashboard  = () => import('../views/DashboardView.vue')
const Invoices   = () => import('../views/InvoicesView.vue')
const Debtors    = () => import('../views/DebtorsView.vue')
const Flows      = () => import('../views/FlowsView.vue')
const Upload     = () => import('../views/UploadView.vue')
const Billing    = () => import('../views/BillingView.vue')
const Pay        = () => import('../views/PayView.vue')

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',            component: Landing },
    { path: '/demo',        component: Demo },
    { path: '/pay/:token',  component: Pay },
    { path: '/app/dashboard', component: Dashboard, meta: { layout: 'app' } },
    { path: '/app/invoices',  component: Invoices,  meta: { layout: 'app' } },
    { path: '/app/debtors',   component: Debtors,   meta: { layout: 'app' } },
    { path: '/app/flows',     component: Flows,     meta: { layout: 'app' } },
    { path: '/app/upload',    component: Upload,    meta: { layout: 'app' } },
    { path: '/app/billing',   component: Billing,   meta: { layout: 'app' } },
  ]
})
