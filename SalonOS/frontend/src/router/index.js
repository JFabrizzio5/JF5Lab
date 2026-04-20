import { createRouter, createWebHistory } from 'vue-router'

import LandingView from '../views/LandingView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import VenuePublicView from '../views/public/VenuePublicView.vue'
import DashboardView from '../views/venue/DashboardView.vue'
import ClientsView from '../views/venue/ClientsView.vue'
import EventsView from '../views/venue/EventsView.vue'
import SpacesView from '../views/venue/SpacesView.vue'
import CalendarView from '../views/venue/CalendarView.vue'
import ChatView from '../views/venue/ChatView.vue'
import ChatListView from '../views/venue/ChatListView.vue'
import SettingsView from '../views/venue/SettingsView.vue'
import BranchesView from '../views/venue/BranchesView.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminVenues from '../views/admin/AdminVenues.vue'

const ROLE_HOME = {
  superadmin: '/admin',
  venue_owner: '/dashboard',
  venue_staff: '/dashboard',
  client: '/',
}

const routes = [
  { path: '/', component: LandingView, meta: { landing: true } },
  { path: '/v/:slug', component: VenuePublicView, meta: { landing: true } },
  { path: '/login', component: LoginView, meta: { guest: true } },
  { path: '/register', component: RegisterView, meta: { guest: true } },

  { path: '/dashboard', component: DashboardView, meta: { auth: true, roles: ['venue_owner', 'venue_staff'] } },
  { path: '/clients', component: ClientsView, meta: { auth: true, roles: ['venue_owner', 'venue_staff'] } },
  { path: '/events', component: EventsView, meta: { auth: true, roles: ['venue_owner', 'venue_staff'] } },
  { path: '/calendar', component: CalendarView, meta: { auth: true, roles: ['venue_owner', 'venue_staff'] } },
  { path: '/spaces', component: SpacesView, meta: { auth: true, roles: ['venue_owner'] } },
  { path: '/branches', component: BranchesView, meta: { auth: true, roles: ['venue_owner'] } },
  { path: '/chats', component: ChatListView, meta: { auth: true, roles: ['venue_owner', 'venue_staff'] } },
  { path: '/chat/:room_id', component: ChatView, meta: { auth: true, roles: ['venue_owner', 'venue_staff'] } },
  { path: '/settings', component: SettingsView, meta: { auth: true, roles: ['venue_owner'] } },

  { path: '/admin', component: AdminDashboard, meta: { auth: true, roles: ['superadmin'] } },
  { path: '/admin/venues', component: AdminVenues, meta: { auth: true, roles: ['superadmin'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('salonos_token')
  const userStr = localStorage.getItem('salonos_user')
  const user = userStr ? JSON.parse(userStr) : null

  if (to.meta.auth) {
    if (!token || !user) {
      return next('/login')
    }
    if (to.meta.roles && !to.meta.roles.includes(user.role)) {
      return next(ROLE_HOME[user.role] || '/')
    }
  }

  if (to.meta.guest && token && user) {
    return next(ROLE_HOME[user.role] || '/')
  }

  next()
})

export default router
