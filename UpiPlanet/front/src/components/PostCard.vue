<template>
  <article class="upi-card upi-card-lift p-5">
    <header class="flex items-center gap-3">
      <router-link :to="`/u/${post.author.username}`" class="upi-avatar h-10 w-10 text-lg">
        <i :class="`mdi mdi-${post.author.avatar_icon}`"></i>
      </router-link>
      <div class="min-w-0 flex-1">
        <router-link :to="`/u/${post.author.username}`" class="block truncate text-[15px] font-semibold text-white hover:text-upi-200 transition-colors">
          {{ post.author.display_name }}
        </router-link>
        <div class="flex items-center gap-1.5 text-[12px] text-ink-300">
          <span class="truncate">@{{ post.author.username }}</span>
          <span class="text-ink-400">·</span>
          <span>{{ relTime }}</span>
          <span v-if="post.mood_icon" class="text-upi-300"><i :class="`mdi mdi-${post.mood_icon}`"></i></span>
        </div>
      </div>
      <button class="grid h-8 w-8 place-items-center rounded-full text-ink-300 hover:bg-white/5 hover:text-white transition-colors" title="Más">
        <i class="mdi mdi-dots-horizontal"></i>
      </button>
    </header>

    <p class="mt-3 whitespace-pre-wrap break-words text-[15.5px] leading-relaxed text-ink-50">{{ post.content }}</p>

    <footer class="mt-4 flex items-center gap-1 border-t border-white/5 pt-3">
      <button class="action" :class="{ 'liked': liked }" @click="onLike" :disabled="!session.authed">
        <i :class="liked ? 'mdi mdi-heart' : 'mdi mdi-heart-outline'"></i>
        <span>{{ likes }}</span>
      </button>
      <button class="action" @click="open = !open">
        <i class="mdi mdi-comment-outline"></i>
        <span>{{ post.comments }}</span>
      </button>
      <button class="action" @click="share" title="Compartir">
        <i class="mdi mdi-share-outline"></i>
      </button>
    </footer>

    <section v-if="open" class="mt-3 space-y-3 border-t border-white/5 pt-3">
      <div v-if="loading" class="flex items-center gap-2 text-[13px] text-ink-300">
        <i class="mdi mdi-loading mdi-spin"></i> cargando
      </div>
      <div v-for="c in comments" :key="c.id" class="flex gap-2.5">
        <span class="upi-avatar h-8 w-8 text-sm"><i :class="`mdi mdi-${c.author.avatar_icon}`"></i></span>
        <div class="flex-1 rounded-2xl border border-white/5 bg-white/[0.04] px-3.5 py-2">
          <router-link :to="`/u/${c.author.username}`" class="text-[13px] font-semibold text-white">
            {{ c.author.display_name }}
          </router-link>
          <p class="text-[14px] text-ink-100">{{ c.content }}</p>
        </div>
      </div>
      <form v-if="session.authed" @submit.prevent="doComment" class="flex gap-2">
        <input v-model="draft" class="upi-input !py-2 !text-[14px]" placeholder="Agrega un comentario…" maxlength="500" />
        <button class="upi-btn-primary !px-4" :disabled="!draft.trim()"><i class="mdi mdi-send"></i></button>
      </form>
      <p v-else class="text-[13px] text-ink-300">
        <i class="mdi mdi-information-outline"></i> Inicia sesión para comentar.
      </p>
    </section>
  </article>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { toggleLike, getComments, addComment } from '../api/upi';
import { useSession } from '../stores/session';

const props = defineProps({ post: { type: Object, required: true } });
const session = useSession();
const likes = ref(props.post.likes);
const liked = ref(false);
const open = ref(false);
const loading = ref(false);
const comments = ref([]);
const draft = ref('');

const relTime = computed(() => {
  const d = new Date(props.post.created_at);
  const m = Math.floor((Date.now() - d.getTime()) / 60000);
  if (m < 1) return 'ahora';
  if (m < 60) return `${m}m`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h`;
  return `${Math.floor(h / 24)}d`;
});

async function onLike() {
  try {
    const r = await toggleLike(props.post.id);
    liked.value = r.liked; likes.value = r.total;
  } catch {}
}

async function loadComments() {
  loading.value = true;
  try { comments.value = await getComments(props.post.id); }
  finally { loading.value = false; }
}

async function doComment() {
  const c = draft.value.trim();
  if (!c) return;
  const n = await addComment(props.post.id, c);
  comments.value.push(n);
  draft.value = '';
}

function share() {
  const url = `${location.origin}/u/${props.post.author.username}`;
  if (navigator.share) navigator.share({ title: 'UpiPlanet', text: props.post.content, url });
  else navigator.clipboard.writeText(url);
}

watch(open, (v) => { if (v && !comments.value.length) loadComments(); });
</script>

<style scoped>
@reference "../styles.css";
.action {
  @apply inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[13px] font-medium text-ink-300 transition-colors;
}
.action:hover { @apply bg-white/5 text-white; }
.action.liked { @apply text-rose-400; }
.action.liked:hover { @apply bg-rose-500/10 text-rose-300; }
.action:disabled { @apply opacity-50 cursor-not-allowed; }
</style>
