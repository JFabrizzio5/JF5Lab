<template>
  <article class="upi-card p-5">
    <header class="flex items-center gap-3">
      <router-link :to="`/u/${post.author.username}`" class="upi-avatar h-9 w-9 text-[15px]">
        <i :class="`mdi mdi-${post.author.avatar_icon}`"></i>
      </router-link>
      <div class="min-w-0 flex-1">
        <router-link :to="`/u/${post.author.username}`" class="block truncate text-[14.5px] font-semibold text-ink-900">
          {{ post.author.display_name }}
        </router-link>
        <div class="flex items-center gap-1.5 text-[12px] text-ink-400">
          <span class="truncate">@{{ post.author.username }}</span>
          <span>·</span>
          <span>{{ relTime }}</span>
          <i v-if="post.mood_icon" :class="`mdi mdi-${post.mood_icon} text-ink-500`"></i>
        </div>
      </div>
    </header>

    <p class="mt-3 whitespace-pre-wrap break-words text-[15px] leading-relaxed text-ink-900">{{ post.content }}</p>

    <footer class="mt-4 flex items-center gap-1 border-t border-ink-100 pt-3">
      <button class="action" :class="{ 'text-rose-500': liked }" @click="onLike" :disabled="!session.authed">
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

    <section v-if="open" class="mt-3 space-y-3 border-t border-ink-100 pt-3">
      <div v-if="loading" class="text-[13px] text-ink-400">
        <i class="mdi mdi-loading mdi-spin"></i> cargando
      </div>
      <div v-for="c in comments" :key="c.id" class="flex gap-2.5">
        <span class="upi-avatar h-7 w-7 text-[12px]"><i :class="`mdi mdi-${c.author.avatar_icon}`"></i></span>
        <div class="flex-1 rounded-xl bg-ink-50 px-3 py-2">
          <router-link :to="`/u/${c.author.username}`" class="text-[12.5px] font-semibold text-ink-900">
            {{ c.author.display_name }}
          </router-link>
          <p class="text-[13.5px] text-ink-700">{{ c.content }}</p>
        </div>
      </div>
      <form v-if="session.authed" @submit.prevent="doComment" class="flex gap-2">
        <input v-model="draft" class="upi-input !py-2 !text-[13.5px]" placeholder="Comentar…" maxlength="500" />
        <button class="upi-btn-primary !px-4 !text-[13px]" :disabled="!draft.trim()">Enviar</button>
      </form>
      <p v-else class="text-[13px] text-ink-400">Inicia sesión para comentar.</p>
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
  @apply inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[12.5px] font-medium text-ink-400 transition-colors;
}
.action:hover { @apply bg-ink-50 text-ink-900; }
.action:disabled { @apply opacity-50 cursor-not-allowed; }
</style>
