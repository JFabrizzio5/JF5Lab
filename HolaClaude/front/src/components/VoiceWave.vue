<template>
  <div class="wave-wrap" :class="{ active }">
    <canvas ref="cnv" class="wave-canvas"></canvas>
    <div class="wave-info">
      <span class="pill" :class="active ? 'ok' : 'dim'">
        <i :class="active ? 'mdi mdi-microphone' : 'mdi mdi-microphone-off'"></i>
        {{ active ? 'escuchando' : 'micrófono off' }}
      </span>
      <span class="pill mono" v-if="active">vol {{ levelPct }}%</span>
    </div>
    <div class="wave-transcript" v-if="transcript || interim">
      <span class="final">{{ transcript }}</span>
      <span class="interim">{{ interim }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';

const props = defineProps({
  active: { type: Boolean, default: false },
  transcript: { type: String, default: '' },
  interim: { type: String, default: '' }
});

const cnv = ref(null);
const levelPct = ref(0);
let stream = null, ctx = null, analyser = null, data = null, raf = 0;

async function startMic() {
  if (stream) return;
  stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
  ctx = new (window.AudioContext || window.webkitAudioContext)();
  const src = ctx.createMediaStreamSource(stream);
  analyser = ctx.createAnalyser();
  analyser.fftSize = 1024;
  analyser.smoothingTimeConstant = 0.6;
  src.connect(analyser);
  data = new Uint8Array(analyser.fftSize);
  loop();
}

function stopMic() {
  cancelAnimationFrame(raf);
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
  if (ctx) { ctx.close().catch(() => {}); ctx = null; }
  analyser = null;
  levelPct.value = 0;
  draw(true);
}

function draw(flat = false) {
  const c = cnv.value; if (!c) return;
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const w = (c.width = c.clientWidth * dpr);
  const h = (c.height = c.clientHeight * dpr);
  const g = c.getContext('2d');
  g.clearRect(0, 0, w, h);
  g.lineWidth = 2 * dpr;
  g.strokeStyle = props.active ? 'rgba(108,160,255,0.95)' : 'rgba(139,147,167,0.5)';
  g.beginPath();
  if (flat || !analyser) {
    g.moveTo(0, h / 2); g.lineTo(w, h / 2);
  } else {
    analyser.getByteTimeDomainData(data);
    const step = w / data.length;
    let sum = 0;
    for (let i = 0; i < data.length; i++) {
      const v = (data[i] - 128) / 128;
      sum += Math.abs(v);
      const y = h / 2 + v * (h / 2) * 0.9;
      if (i === 0) g.moveTo(0, y); else g.lineTo(i * step, y);
    }
    const rms = sum / data.length;
    levelPct.value = Math.min(100, Math.round(rms * 400));
  }
  g.stroke();
  if (props.active && analyser) {
    const grad = g.createLinearGradient(0, 0, w, 0);
    grad.addColorStop(0, 'rgba(108,160,255,0.1)');
    grad.addColorStop(0.5, 'rgba(157,123,255,0.2)');
    grad.addColorStop(1, 'rgba(108,160,255,0.1)');
    g.fillStyle = grad;
    g.fillRect(0, h / 2 - 1 * dpr, w * (levelPct.value / 100), 2 * dpr);
  }
}

function loop() {
  draw(false);
  raf = requestAnimationFrame(loop);
}

watch(() => props.active, async (on) => {
  if (on) {
    try { await startMic(); } catch (e) { console.warn('mic error', e); }
  } else {
    stopMic();
  }
});

defineExpose({ stopMic });
onBeforeUnmount(stopMic);
</script>

<style scoped>
.wave-wrap { display: flex; flex-direction: column; gap: 6px; padding: 10px 14px; background: var(--surface-2); border-radius: 12px; border: 1px solid var(--border); transition: border-color 0.2s; }
.wave-wrap.active { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(108,160,255,0.15); }
.wave-canvas { width: 100%; height: 48px; display: block; }
.wave-info { display: flex; gap: 8px; align-items: center; }
.pill { font-size: 11px; padding: 3px 8px; border-radius: 999px; background: var(--surface); border: 1px solid var(--border); }
.pill i { margin-right: 4px; }
.pill.ok { color: var(--ok); border-color: rgba(61,220,151,0.4); background: rgba(61,220,151,0.12); }
.pill.dim { color: var(--text-dim); }
.wave-transcript { font-size: 13px; display: flex; gap: 6px; flex-wrap: wrap; }
.wave-transcript .final { color: var(--text); }
.wave-transcript .interim { color: var(--text-dim); font-style: italic; }
</style>
