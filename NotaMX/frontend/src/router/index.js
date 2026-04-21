import { createRouter, createWebHistory } from 'vue-router'

const Landing    = () => import('../views/LandingView.vue')
const Demo       = () => import('../views/DemoView.vue')
const Dashboard  = () => import('../views/DashboardView.vue')
const Notes      = () => import('../views/NotesView.vue')
const NoteDetail = () => import('../views/NoteDetailView.vue')
const Customers  = () => import('../views/CustomersView.vue')
const Products   = () => import('../views/ProductsView.vue')
const Billing    = () => import('../views/BillingView.vue')
const Cfdi       = () => import('../views/CfdiView.vue')
const Success    = () => import('../views/BillingSuccessView.vue')
const PublicNote = () => import('../views/PublicNoteView.vue')

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Landing },
    { path: '/demo', component: Demo },
    { path: '/billing/success', component: Success },
    { path: '/billing/cancel', component: Success, props: { canceled: true } },
    { path: '/n/:token', component: PublicNote },
    { path: '/app/dashboard', component: Dashboard, meta: { layout: 'app' } },
    { path: '/app/notes',     component: Notes,     meta: { layout: 'app' } },
    { path: '/app/notes/:id', component: NoteDetail, meta: { layout: 'app' } },
    { path: '/app/customers', component: Customers, meta: { layout: 'app' } },
    { path: '/app/products',  component: Products,  meta: { layout: 'app' } },
    { path: '/app/billing',   component: Billing,   meta: { layout: 'app' } },
    { path: '/app/cfdi',      component: Cfdi,      meta: { layout: 'app' } },
  ]
})
