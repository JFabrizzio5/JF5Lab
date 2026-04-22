<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSession } from './stores/session'

const route = useRoute()
const session = useSession()
const theme = ref(localStorage.getItem('theme') || 'light')

const isApp = computed(() => route.meta?.layout === 'app')

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
  <div class="app-shell" :data-layout="isApp ? 'app' : 'marketing'">
    <router-view />
    <button class="theme-toggle" @click="toggleTheme" :title="theme === 'dark' ? 'Modo claro' : 'Modo oscuro'">
      <i :class="theme === 'dark' ? 'mdi mdi-weather-sunny' : 'mdi mdi-weather-night'"></i>
    </button>
  </div>
</template>

<style scoped>
.theme-toggle {
  position: fixed; bottom: 20px; right: 20px; z-index: 90;
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text); cursor: pointer; font-size: 20px;
  display: grid; place-items: center;
  box-shadow: 0 4px 12px rgba(0,0,0,.15); transition: transform .2s;
}
.theme-toggle:hover { transform: scale(1.05); }
</style>
