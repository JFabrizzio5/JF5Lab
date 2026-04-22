<template>
  <nav class="sticky top-0 z-20 border-b border-ink-100 bg-white/80 backdrop-blur">
    <div class="mx-auto flex max-w-5xl items-center gap-6 px-6 py-3">
      <router-link to="/" class="flex items-center gap-2 text-[15px] font-semibold tracking-tight text-ink-900">
        <span class="h-2 w-2 rounded-full bg-ink-900"></span>
        UpiPlanet
      </router-link>

      <div class="ml-2 hidden items-center gap-1 sm:flex">
        <router-link to="/feed" class="nav-link">Feed</router-link>
        <router-link to="/explore" class="nav-link">Explorar</router-link>
        <router-link v-if="session.user" :to="`/u/${session.user.username}`" class="nav-link">Perfil</router-link>
      </div>

      <div class="ml-auto flex items-center gap-2">
        <template v-if="session.user">
          <span class="hidden text-[13px] text-ink-500 sm:inline">@{{ session.user.username }}</span>
          <button @click="doLogout" class="upi-btn-ghost !py-1.5 !px-3 !text-[13px]" title="Salir">
            <i class="mdi mdi-logout"></i>
          </button>
        </template>
        <router-link v-else to="/auth" class="upi-btn-primary !py-1.5 !px-4 !text-[13px]">Entrar</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useSession } from '../stores/session';
const session = useSession();
const router = useRouter();
function doLogout() { session.logout(); router.push('/'); }
</script>

<style scoped>
@reference "../styles.css";
.nav-link {
  @apply inline-flex items-center rounded-full px-3 py-1.5 text-[13.5px] font-medium text-ink-500 transition-colors;
}
.nav-link:hover { @apply text-ink-900; }
.router-link-active.nav-link { @apply text-ink-900 bg-ink-100; }
</style>
