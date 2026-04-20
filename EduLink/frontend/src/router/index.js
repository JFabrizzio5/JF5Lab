import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/LandingView.vue') },
  { path: '/login', component: () => import('../views/LoginView.vue') },
  { path: '/register', component: () => import('../views/RegisterView.vue') },

  // Student routes
  { path: '/courses', component: () => import('../views/student/HomeView.vue'), meta: { requiresAuth: true, role: 'student' } },
  { path: '/courses/:id', component: () => import('../views/student/CourseDetailView.vue'), meta: { requiresAuth: true } },
  { path: '/my-courses', component: () => import('../views/student/MyCoursesView.vue'), meta: { requiresAuth: true, role: 'student' } },
  { path: '/schedule', component: () => import('../views/student/ScheduleView.vue'), meta: { requiresAuth: true, role: 'student' } },

  // Tutor routes
  { path: '/tutor/dashboard', component: () => import('../views/tutor/DashboardView.vue'), meta: { requiresAuth: true, role: 'tutor' } },
  { path: '/tutor/courses', component: () => import('../views/tutor/MyCourses.vue'), meta: { requiresAuth: true, role: 'tutor' } },
  { path: '/tutor/schedule', component: () => import('../views/tutor/ScheduleView.vue'), meta: { requiresAuth: true, role: 'tutor' } },

  // Admin routes
  { path: '/admin', component: () => import('../views/admin/AdminDashboard.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/users', component: () => import('../views/admin/AdminUsers.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/courses', component: () => import('../views/admin/AdminCourses.vue'), meta: { requiresAuth: true, role: 'admin' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null

  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  if (to.meta.role && user?.role !== to.meta.role && user?.role !== 'admin') {
    // Redirect to appropriate home
    if (user?.role === 'admin') return next('/admin')
    if (user?.role === 'tutor') return next('/tutor/dashboard')
    if (user?.role === 'student') return next('/courses')
    return next('/login')
  }

  next()
})

export default router
