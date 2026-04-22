<template>
  <TopNav />

  <main class="mx-auto grid max-w-6xl gap-6 px-6 py-6 md:grid-cols-[200px_1fr_260px]">
    <aside class="sticky top-20 hidden h-fit md:block">
      <nav class="flex flex-col gap-0.5">
        <router-link to="/feed" class="side"><i class="mdi mdi-home-variant"></i> Feed</router-link>
        <router-link to="/explore" class="side"><i class="mdi mdi-compass-outline"></i> Explorar</router-link>
        <router-link v-if="session.user" :to="`/u/${session.user.username}`" class="side">
          <i class="mdi mdi-account-circle-outline"></i> Mi perfil
        </router-link>
        <div class="mt-3 px-3 text-[11px] font-semibold uppercase tracking-wider text-ink-300">Descubre</div>
        <a class="side opacity-60"><i class="mdi mdi-trending-up"></i> Tendencias</a>
        <a class="side opacity-60"><i class="mdi mdi-bookmark-outline"></i> Guardados</a>
      </nav>
    </aside>

    <section class="space-y-4 min-w-0">
      <div v-if="session.authed" class="upi-card p-5">
        <div class="flex gap-3">
          <span class="upi-avatar h-10 w-10 text-lg"><i :class="`mdi mdi-${session.user.avatar_icon}`"></i></span>
          <textarea
            v-model="draft"
            class="w-full resize-none border-none bg-transparent text-[15.5px] leading-relaxed text-white placeholder:text-ink-300 focus:outline-none"
            placeholder="¿Qué está pasando en tu órbita?"
            maxlength="1000"
            rows="2"
          ></textarea>
        </div>
        <div class="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-white/5 pt-3">
          <div class="flex flex-wrap items-center gap-1">
            <button
              v-for="m in moods" :key="m"
              type="button"
              :class="['mood', { 'mood-on': selectedMood === m }]"
              @click="selectedMood = selectedMood === m ? null : m"
              :title="m"
            ><i :class="`mdi mdi-${m}`"></i></button>
          </div>
          <div class="flex items-center gap-2">
            <button class="upi-btn-ghost !py-1.5 !px-3" @click="aiSuggest" :disabled="aiBusy" title="Sugerencia IA">
              <i class="mdi" :class="aiBusy ? 'mdi-loading mdi-spin' : 'mdi-sparkles'"></i>
              <span class="hidden sm:inline">IA</span>
            </button>
            <button class="upi-btn-primary !py-2 !px-4" :disabled="!draft.trim() || posting" @click="submit">
              <i class="mdi mdi-send"></i> Publicar
            </button>
          </div>
        </div>
      </div>

      <div v-else class="upi-card flex items-center gap-4 p-5">
        <span class="grid h-10 w-10 place-items-center rounded-xl bg-upi-500/15 text-upi-200 border border-upi-400/30">
          <i class="mdi mdi-rocket-launch-outline text-xl"></i>
        </span>
        <div class="min-w-0 flex-1">
          <div class="text-[15px] font-semibold text-white">Únete a UpiPlanet</div>
          <div class="text-[13px] text-ink-300">Crea una cuenta para postear, comentar y dar likes.</div>
        </div>
        <router-link to="/auth" class="upi-btn-primary shrink-0">Entrar</router-link>
      </div>

      <div v-if="loading && !posts.length" class="py-10 text-center text-sm text-ink-300">
        <i class="mdi mdi-loading mdi-spin"></i> cargando feed…
      </div>

      <PostCard v-for="p in posts" :key="p.id" :post="p" />

      <div v-if="!loading && !posts.length" class="upi-card py-14 text-center">
        <i class="mdi mdi-telescope text-[32px] text-upi-300"></i>
        <p class="mt-2 text-[14px] text-ink-100">Planeta silencioso.</p>
        <p class="mt-0.5 text-[12.5px] text-ink-300">Sé el primero en dejar huella en la órbita.</p>
      </div>
    </section>

    <aside class="sticky top-20 hidden h-fit space-y-4 md:block">
      <div class="upi-card p-5">
        <div class="mb-3 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wider text-ink-300">
          <i class="mdi mdi-sparkles text-upi-300"></i> Para ti
        </div>
        <p class="text-[13.5px] leading-relaxed text-ink-100">
          El feed se ordena por conversación reciente, no por dopamina. La IA resume cuando se lo pides.
        </p>
      </div>

      <div v-if="suggested.length" class="upi-card p-5">
        <div class="mb-3 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wider text-ink-300">
          <i class="mdi mdi-account-group-outline"></i> Habitantes
        </div>
        <ul class="space-y-3">
          <li v-for="u in suggested" :key="u.id">
            <router-link :to="`/u/${u.username}`" class="flex items-center gap-2.5 hover:opacity-80 transition-opacity">
              <span class="upi-avatar h-8 w-8 text-sm"><i :class="`mdi mdi-${u.avatar_icon}`"></i></span>
              <span class="min-w-0 flex-1">
                <span class="block truncate text-[13.5px] font-semibold text-white">{{ u.display_name }}</span>
                <span class="block truncate text-[12px] text-ink-300">@{{ u.username }}</span>
              </span>
            </router-link>
          </li>
        </ul>
      </div>
    </aside>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import TopNav from '../components/TopNav.vue';
import PostCard from '../components/PostCard.vue';
import { getFeed, createPost, searchUsers } from '../api/upi';
import { useSession } from '../stores/session';

const session = useSession();
const posts = ref([]);
const suggested = ref([]);
const draft = ref('');
const posting = ref(false);
const loading = ref(true);
const aiBusy = ref(false);
const moods = ['rocket-launch', 'weather-sunset', 'music', 'heart', 'coffee', 'lightbulb-on', 'palette'];
const selectedMood = ref(null);

const AI_SUGGESTIONS = [
  'Hoy miré el cielo por 5 minutos. Recomendado para todos.',
  'Pequeño logro del día: descansar sin culpa.',
  'Escucha una canción vieja con oídos nuevos. Vale la pena.',
  'Mi café de hoy sabe a planeta lejano.',
  'La mejor idea de la semana vino mientras caminaba.',
];

async function load() {
  loading.value = true;
  try {
    posts.value = await getFeed(40);
    suggested.value = (await searchUsers()).slice(0, 8);
  } finally { loading.value = false; }
}

async function submit() {
  posting.value = true;
  try {
    const p = await createPost({ content: draft.value.trim(), mood_icon: selectedMood.value });
    posts.value.unshift(p);
    draft.value = ''; selectedMood.value = null;
  } finally { posting.value = false; }
}

async function aiSuggest() {
  aiBusy.value = true;
  try {
    await new Promise(r => setTimeout(r, 450));
    draft.value = AI_SUGGESTIONS[Math.floor(Math.random() * AI_SUGGESTIONS.length)];
  } finally { aiBusy.value = false; }
}

onMounted(async () => { await session.rehydrate(); await load(); });
</script>

<style scoped>
@reference "../styles.css";
.side {
  @apply flex items-center gap-2 rounded-xl px-3 py-2 text-[14px] font-medium text-ink-200 transition-colors;
}
.side:hover { @apply bg-white/5 text-white; }
.router-link-active.side { @apply bg-upi-500/15 text-upi-100 border border-upi-400/30; }
.mood {
  @apply grid h-8 w-8 place-items-center rounded-lg text-[16px] text-ink-300 transition-colors;
}
.mood:hover { @apply bg-white/5 text-upi-200; }
.mood-on {
  @apply text-white;
  background: linear-gradient(135deg, var(--color-upi-500), var(--color-upi-700));
  box-shadow: 0 4px 14px -4px rgba(109,53,255,0.7);
}
</style>
