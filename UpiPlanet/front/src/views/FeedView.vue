<template>
  <TopNav />

  <main class="mx-auto grid max-w-5xl gap-8 px-6 py-8 md:grid-cols-[180px_1fr]">
    <aside class="sticky top-20 hidden h-fit md:block">
      <nav class="flex flex-col gap-0.5">
        <router-link to="/feed" class="side"><i class="mdi mdi-circle-small"></i> Feed</router-link>
        <router-link to="/explore" class="side"><i class="mdi mdi-magnify"></i> Explorar</router-link>
        <router-link v-if="session.user" :to="`/u/${session.user.username}`" class="side">
          <i class="mdi mdi-account-outline"></i> Perfil
        </router-link>
      </nav>
    </aside>

    <section class="space-y-4 min-w-0">
      <div v-if="session.authed" class="upi-card p-5">
        <div class="flex gap-3">
          <span class="upi-avatar h-9 w-9 text-[15px]"><i :class="`mdi mdi-${session.user.avatar_icon}`"></i></span>
          <textarea
            v-model="draft"
            class="w-full resize-none border-none bg-transparent text-[15px] leading-relaxed text-ink-900 placeholder:text-ink-400 focus:outline-none"
            placeholder="¿Qué estás pensando?"
            maxlength="1000"
            rows="2"
          ></textarea>
        </div>
        <div class="mt-2 flex items-center justify-between gap-2 border-t border-ink-100 pt-3">
          <div class="flex items-center gap-0.5">
            <button
              v-for="m in moods" :key="m"
              type="button"
              :class="['mood', { 'mood-on': selectedMood === m }]"
              @click="selectedMood = selectedMood === m ? null : m"
              :title="m"
            ><i :class="`mdi mdi-${m}`"></i></button>
          </div>
          <button class="upi-btn-primary !py-2 !px-4 !text-[13px]" :disabled="!draft.trim() || posting" @click="submit">
            Publicar
          </button>
        </div>
      </div>

      <div v-else class="upi-card flex items-center justify-between gap-4 p-5">
        <div class="min-w-0">
          <div class="text-[15px] font-semibold text-ink-900">Entra para publicar</div>
          <div class="mt-0.5 text-[13px] text-ink-500">Necesitas cuenta para postear y comentar.</div>
        </div>
        <router-link to="/auth" class="upi-btn-primary shrink-0 !text-[13px]">Entrar</router-link>
      </div>

      <div v-if="loading && !posts.length" class="py-10 text-center text-[13px] text-ink-400">
        <i class="mdi mdi-loading mdi-spin"></i> cargando
      </div>

      <PostCard v-for="p in posts" :key="p.id" :post="p" />

      <div v-if="!loading && !posts.length" class="upi-card py-16 text-center">
        <p class="text-[14px] text-ink-500">Aún no hay publicaciones.</p>
        <p class="mt-1 text-[12px] text-ink-400">Sé el primero en publicar.</p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import TopNav from '../components/TopNav.vue';
import PostCard from '../components/PostCard.vue';
import { getFeed, createPost } from '../api/upi';
import { useSession } from '../stores/session';

const session = useSession();
const posts = ref([]);
const draft = ref('');
const posting = ref(false);
const loading = ref(true);
const moods = ['rocket-launch', 'weather-sunset', 'music', 'heart', 'coffee', 'lightbulb-on'];
const selectedMood = ref(null);

async function load() {
  loading.value = true;
  try { posts.value = await getFeed(40); }
  finally { loading.value = false; }
}

async function submit() {
  posting.value = true;
  try {
    const p = await createPost({ content: draft.value.trim(), mood_icon: selectedMood.value });
    posts.value.unshift(p);
    draft.value = ''; selectedMood.value = null;
  } finally { posting.value = false; }
}

onMounted(async () => { await session.rehydrate(); await load(); });
</script>

<style scoped>
@reference "../styles.css";
.side {
  @apply flex items-center gap-2 rounded-lg px-3 py-2 text-[13.5px] font-medium text-ink-500 transition-colors;
}
.side:hover { @apply bg-ink-50 text-ink-900; }
.router-link-active.side { @apply bg-ink-100 text-ink-900; }
.mood {
  @apply grid h-8 w-8 place-items-center rounded-lg text-[15px] text-ink-400 transition-colors;
}
.mood:hover { @apply bg-ink-50 text-ink-700; }
.mood-on { @apply bg-ink-900 text-white; }
</style>
