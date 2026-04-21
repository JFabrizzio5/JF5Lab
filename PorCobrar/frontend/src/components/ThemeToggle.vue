<script setup>
import { useSession } from '../stores/session'
const s = useSession()
</script>

<template>
  <button class="theme-toggle" :title="'Tema: ' + s.theme" @click="s.toggleTheme()">
    <i class="mdi" :class="s.theme === 'dark' ? 'mdi-weather-sunny' : 'mdi-weather-night'"></i>
  </button>
</template>
