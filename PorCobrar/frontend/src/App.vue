<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from './components/AppLayout.vue'
import ThemeToggle from './components/ThemeToggle.vue'
const route = useRoute()
const isApp = computed(() => route.meta?.layout === 'app')
</script>

<template>
  <AppLayout v-if="isApp">
    <router-view />
  </AppLayout>
  <template v-else>
    <router-view />
  </template>
  <ThemeToggle />
</template>
