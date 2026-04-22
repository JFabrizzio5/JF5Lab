import { createRouter, createWebHistory } from 'vue-router'

const Landing   = () => import('../views/LandingView.vue')
const Demo      = () => import('../views/DemoView.vue')
const Dashboard = () => import('../views/DashboardView.vue')
const Items     = () => import('../views/ItemsView.vue')
const Scanner   = () => import('../views/ScannerView.vue')
const Labels    = () => import('../views/LabelsView.vue')
const Attendance= () => import('../views/AttendanceView.vue')
const Movements = () => import('../views/MovementsView.vue')
const Reports   = () => import('../views/ReportsView.vue')

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Landing, meta: { layout: 'marketing' } },
    { path: '/demo', component: Demo, meta: { layout: 'marketing' } },
    { path: '/app/dashboard',  component: Dashboard,  meta: { layout: 'app' } },
    { path: '/app/items',      component: Items,      meta: { layout: 'app' } },
    { path: '/app/scanner',    component: Scanner,    meta: { layout: 'app' } },
    { path: '/app/labels',     component: Labels,     meta: { layout: 'app' } },
    { path: '/app/attendance', component: Attendance, meta: { layout: 'app' } },
    { path: '/app/movements',  component: Movements,  meta: { layout: 'app' } },
    { path: '/app/reports',    component: Reports,    meta: { layout: 'app' } },
  ]
})
