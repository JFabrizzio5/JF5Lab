<template>
  <TopNav />
  <main v-if="data" class="mx-auto max-w-2xl space-y-4 px-6 py-8">
    <header class="upi-card p-6">
      <div class="flex items-start gap-5">
        <span class="upi-avatar h-16 w-16 text-[28px]">
          <i :class="`mdi mdi-${data.user.avatar_icon}`"></i>
        </span>
        <div class="min-w-0 flex-1">
          <h2 class="truncate text-[20px] font-semibold tracking-tight text-ink-900">{{ data.user.display_name }}</h2>
          <p class="text-[13px] text-ink-400">@{{ data.user.username }}</p>
          <p v-if="data.user.bio" class="mt-2 text-[14px] leading-relaxed text-ink-700">{{ data.user.bio }}</p>
          <div class="mt-4 flex flex-wrap gap-5 text-[13px] text-ink-500">
            <span><strong class="text-ink-900">{{ data.posts.length }}</strong> posts</span>
            <span><strong class="text-ink-900">{{ data.followers }}</strong> seguidores</span>
            <span><strong class="text-ink-900">{{ data.following }}</strong> seguidos</span>
          </div>
        </div>
      </div>
    </header>

    <section class="space-y-3">
      <article v-for="p in data.posts" :key="p.id" class="upi-card p-5">
        <p class="whitespace-pre-wrap text-[14.5px] leading-relaxed text-ink-900">{{ p.content }}</p>
        <span class="mt-3 block text-[11.5px] text-ink-400">{{ fmt(p.created_at) }}</span>
      </article>
      <p v-if="!data.posts.length" class="py-12 text-center text-[13px] text-ink-400">
        Sin publicaciones.
      </p>
    </section>
  </main>
  <main v-else class="py-20 text-center text-[13px] text-ink-400">
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
