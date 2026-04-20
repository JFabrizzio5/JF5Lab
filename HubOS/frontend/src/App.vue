<template>
  <div id="hubos" :class="{ 'with-layout': hasLayout }">
    <template v-if="hasLayout">
      <AppSidebar />
      <main class="main-content">
        <router-view />
      </main>
    </template>
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppSidebar from './components/AppSidebar.vue'
import { useAuthStore } from './stores/auth.js'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const hasLayout = computed(() => route.meta.layout !== 'none' && auth.isAuthenticated)

// --- Public-server safety ---
// - Token lives in sessionStorage → auto-wipes when tab closes
//   (so reload is fine, closing browser kills session).
// - Idle 20min → auto logout + WhatsApp desvinculado.
const IDLE_MINUTES = 20
let idleTimer = null

function resetIdle() {
  if (idleTimer) clearTimeout(idleTimer)
  if (!auth.isAuthenticated) return
  idleTimer = setTimeout(async () => {
    await auth.logout()
    router.push('/login')
    alert('Sesión cerrada por inactividad. WhatsApp desvinculado.')
  }, IDLE_MINUTES * 60 * 1000)
}

const activityEvents = ['mousedown', 'keydown', 'scroll', 'touchstart']

onMounted(() => {
  if (window.lucide) window.lucide.createIcons()
  resetIdle()
  activityEvents.forEach(e => window.addEventListener(e, resetIdle, { passive: true }))
})

onUnmounted(() => {
  if (idleTimer) clearTimeout(idleTimer)
  activityEvents.forEach(e => window.removeEventListener(e, resetIdle))
})
</script>

<style>
#hubos { min-height: 100vh; }
#hubos.with-layout .main-content {
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  background: var(--bg);
}
@media (max-width: 860px) {
  #hubos.with-layout .main-content { margin-left: 0; }
}
</style>
