<template>
  <nav class="sticky top-0 z-20 border-b border-white/5 bg-ink-900/70 backdrop-blur-xl">
    <div class="mx-auto flex max-w-6xl items-center gap-5 px-6 py-3">
      <router-link to="/" class="flex items-center gap-2.5 font-semibold tracking-tight text-white">
        <span class="grid h-8 w-8 place-items-center rounded-xl bg-gradient-to-br from-upi-400 to-upi-700 text-white shadow-[0_6px_20px_-6px_rgba(109,53,255,0.7)]">
          <i class="mdi mdi-orbit text-[18px]"></i>
        </span>
        <span class="text-[15px]">UpiPlanet</span>
      </router-link>

      <div class="ml-2 hidden items-center gap-1 sm:flex">
        <router-link to="/feed" class="nav-link"><i class="mdi mdi-home-variant"></i><span>Feed</span></router-link>
        <router-link to="/explore" class="nav-link"><i class="mdi mdi-compass-outline"></i><span>Explorar</span></router-link>
        <router-link v-if="session.user" :to="`/u/${session.user.username}`" class="nav-link">
          <i class="mdi mdi-account-circle-outline"></i><span>Yo</span>
        </router-link>
      </div>

      <div class="ml-auto flex items-center gap-2.5">
        <template v-if="session.user">
          <div class="hidden items-center gap-2 rounded-full border border-white/10 bg-white/5 py-1 pr-3 pl-1 sm:flex">
            <span class="upi-avatar h-7 w-7 text-sm">
              <i :class="`mdi mdi-${session.user.avatar_icon}`"></i>
            </span>
            <span class="text-[13px] font-medium text-ink-100">{{ session.user.display_name }}</span>
          </div>
          <button @click="doLogout" class="upi-btn-ghost !py-1.5 !px-3" title="Salir">
            <i class="mdi mdi-logout"></i>
          </button>
        </template>
        <router-link v-else to="/auth" class="upi-btn-primary !py-1.5 !px-4 !text-[13px]">
          <i class="mdi mdi-arrow-right-thin"></i> Entrar
        </router-link>
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
  @apply inline-flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[13.5px] font-medium text-ink-200 transition-colors;
}
.nav-link:hover { @apply text-white bg-white/5; }
.router-link-active.nav-link { @apply text-upi-200 bg-upi-500/15 border border-upi-400/30; }
</style>
