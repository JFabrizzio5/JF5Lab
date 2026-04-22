<template>
  <TopNav />
  <main v-if="data" class="mx-auto max-w-2xl space-y-4 px-6 py-6">
    <header class="upi-card relative overflow-hidden p-6 upi-fade-up">
      <div class="absolute inset-x-0 -top-24 h-48 bg-gradient-to-b from-upi-500/25 to-transparent pointer-events-none"></div>
      <div class="relative flex items-start gap-5">
        <span class="upi-avatar h-20 w-20 text-[38px] ring-4 ring-white/10">
          <i :class="`mdi mdi-${data.user.avatar_icon}`"></i>
        </span>
        <div class="min-w-0 flex-1">
          <h2 class="truncate text-[22px] font-semibold tracking-tight text-white">{{ data.user.display_name }}</h2>
          <p class="text-[13px] text-ink-300">@{{ data.user.username }}</p>
          <p class="mt-2 text-[14.5px] leading-relaxed text-ink-100">{{ data.user.bio || 'Sin bio todavía.' }}</p>
          <div class="mt-3 flex flex-wrap gap-4 text-[13px] text-ink-200">
            <span><strong class="text-white">{{ data.posts.length }}</strong> posts</span>
            <span><strong class="text-white">{{ data.followers }}</strong> seguidores</span>
            <span><strong class="text-white">{{ data.following }}</strong> seguidos</span>
          </div>
        </div>
      </div>
    </header>

    <section class="space-y-3">
      <article v-for="p in data.posts" :key="p.id" class="upi-card upi-card-lift p-5">
        <p class="whitespace-pre-wrap text-[15px] leading-relaxed text-ink-50">{{ p.content }}</p>
        <span class="mt-3 flex items-center gap-1.5 text-[12px] text-ink-300">
          <i v-if="p.mood_icon" :class="`mdi mdi-${p.mood_icon} text-upi-300`"></i>
          {{ fmt(p.created_at) }}
        </span>
      </article>
      <p v-if="!data.posts.length" class="py-10 text-center text-[13px] text-ink-300">
        Aún no ha posteado nada.
      </p>
    </section>
  </main>
  <main v-else class="py-20 text-center text-[13px] text-ink-300">
    <i class="mdi mdi-loading mdi-spin"></i> cargando
  </main>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import TopNav from '../components/TopNav.vue';
import { getProfile } from '../api/upi';

const route = useRoute();
const data = ref(null);

async function load() {
  data.value = null;
  try { data.value = await getProfile(route.params.username); }
  catch { data.value = { user: { username: '?', display_name: 'no existe', avatar_icon: 'alert' }, posts: [], followers: 0, following: 0 }; }
}
function fmt(iso) { return new Date(iso).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' }); }
onMounted(load);
watch(() => route.params.username, load);
</script>
