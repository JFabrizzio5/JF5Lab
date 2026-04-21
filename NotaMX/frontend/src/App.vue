<script setup>
import { onMounted, ref } from 'vue'
import { useSession } from './stores/session'

const session = useSession()
const theme = ref(localStorage.getItem('theme') || 'light')

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = theme.value
  localStorage.setItem('theme', theme.value)
}

onMounted(() => {
  document.documentElement.dataset.theme = theme.value
  session.restore()
})
</script>

<template>
  <div class="app-shell">
    <router-view />
    <button class="theme-fab" @click="toggleTheme" :title="theme === 'dark' ? 'Modo claro' : 'Modo oscuro'">
      <i :class="theme === 'dark' ? 'mdi mdi-white-balance-sunny' : 'mdi mdi-weather-night'"></i>
    </button>
  </div>
</template>

<style scoped>
.theme-fab {
  position: fixed; bottom: 24px; right: 24px; z-index: 90;
  width: 46px; height: 46px; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text); cursor: pointer; font-size: 20px;
  display: grid; place-items: center;
  box-shadow: var(--shadow-md); transition: transform .2s;
}
.theme-fab:hover { transform: scale(1.08) rotate(-8deg); }
</style>
