<template>
  <div class="cam-wrap">
    <video ref="video" autoplay muted playsinline class="cam-video"></video>
    <canvas ref="overlay" class="cam-overlay"></canvas>
    <div class="cam-hud">
      <span class="pill"><i class="mdi mdi-face-recognition"></i> {{ faceState }}</span>
      <span class="pill" :class="{ dim: pausedGestures }">
        <i class="mdi mdi-hand-back-right"></i>
        {{ pausedGestures ? 'pausado' : (handGesture || 'ninguno') }}
      </span>
      <span class="pill mono">EAR {{ earDisplay }} · {{ fps }}fps</span>
      <span class="pill ok" v-if="blinkCount > 0">parpadeos: {{ blinkCount }}</span>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';

const props = defineProps({
  active: { type: Boolean, default: true },
  pausedGestures: { type: Boolean, default: false }
});
const emit = defineEmits(['descriptor', 'gesture', 'blink']);

const video = ref(null);
const overlay = ref(null);
const faceState = ref('cargando…');
const handGesture = ref('');
const fps = ref(0);
const blinkCount = ref(0);
const earDisplay = ref('--');

const EAR_OPEN = 0.22;
const EAR_CLOSED = 0.17;
const CLOSED_FRAMES_REQUIRED = 2;

let faceapi, Hands;
let handsModel = null;
let lastFace = null;
let eyeOpen = true;
let closedFrames = 0;
let detectRaf = 0, renderRaf = 0, lastRender = 0, framesAcc = 0, fpsTick = 0;
let lastGestureAt = 0;
let waveBuffer = [];

async function setupCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { width: 640, height: 480, facingMode: 'user', frameRate: { ideal: 60 } },
    audio: false
  });
  video.value.srcObject = stream;
  await new Promise(r => video.value.onloadedmetadata = r);
}

async function loadFaceApi() {
  faceapi = await import('face-api.js');
  const MODEL_URL = 'https://justadudewhohacks.github.io/face-api.js/models';
  await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
  await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
  await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
  faceState.value = 'listo';
}

async function loadHands() {
  const mod = await import('@mediapipe/hands');
  Hands = mod.Hands;
  handsModel = new Hands({ locateFile: f => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${f}` });
  handsModel.setOptions({ maxNumHands: 1, modelComplexity: 1, minDetectionConfidence: 0.6, minTrackingConfidence: 0.5 });
  handsModel.onResults(onHandResults);
}

function classifyHand(landmarks) {
  const tips = [4, 8, 12, 16, 20];
  const pips = [2, 6, 10, 14, 18];
  const extended = tips.map((t, i) => {
    const tip = landmarks[t], pip = landmarks[pips[i]];
    if (i === 0) return Math.abs(tip.x - landmarks[0].x) > Math.abs(pip.x - landmarks[0].x) * 1.2;
    return tip.y < pip.y;
  });
  const [thumb, idx, mid, ring, pinky] = extended;
  if (idx && mid && ring && pinky) return 'open_palm';
  if (!idx && !mid && !ring && !pinky) return 'fist';
  if (thumb && !idx && !mid && !ring && !pinky) return 'thumbs_up';
  if (idx && mid && !ring && !pinky) return 'peace';
  if (idx && !mid && !ring && !pinky) return 'pointing_up';
  return '';
}

function detectWave(landmarks) {
  waveBuffer.push({ x: landmarks[0].x, t: performance.now() });
  waveBuffer = waveBuffer.filter(p => performance.now() - p.t < 900);
  if (waveBuffer.length < 10) return false;
  const xs = waveBuffer.map(p => p.x);
  const min = Math.min(...xs), max = Math.max(...xs);
  return (max - min) > 0.1;
}

function onHandResults(res) {
  if (!res.multiHandLandmarks || !res.multiHandLandmarks.length) {
    handGesture.value = '';
    waveBuffer = [];
    return;
  }
  if (props.pausedGestures) return;
  const lm = res.multiHandLandmarks[0];
  let g = classifyHand(lm);
  if (g === 'open_palm' && detectWave(lm)) g = 'wave';
  if (g && g !== handGesture.value && performance.now() - lastGestureAt > 700) {
    handGesture.value = g;
    lastGestureAt = performance.now();
    emit('gesture', g);
  }
}

function eyeAspect(points) {
  const d = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
  return (d(points[1], points[5]) + d(points[2], points[4])) / (2 * d(points[0], points[3]));
}

async function detectLoop() {
  if (!props.active) { detectRaf = requestAnimationFrame(detectLoop); return; }
  try {
    const d = await faceapi
      .detectSingleFace(video.value, new faceapi.TinyFaceDetectorOptions({ inputSize: 320, scoreThreshold: 0.55 }))
      .withFaceLandmarks()
      .withFaceDescriptor();
    if (d) {
      lastFace = d;
      faceState.value = 'rostro detectado';
      const lm = d.landmarks;
      const lEye = lm.getLeftEye(), rEye = lm.getRightEye();
      const ear = (eyeAspect(lEye) + eyeAspect(rEye)) / 2;
      earDisplay.value = ear.toFixed(2);
      if (eyeOpen) {
        if (ear < EAR_CLOSED) {
          closedFrames++;
          if (closedFrames >= CLOSED_FRAMES_REQUIRED) {
            eyeOpen = false;
          }
        } else {
          closedFrames = 0;
        }
      } else {
        if (ear > EAR_OPEN) {
          eyeOpen = true;
          closedFrames = 0;
          blinkCount.value++;
          emit('blink', blinkCount.value);
        }
      }
    } else {
      faceState.value = 'sin rostro';
      earDisplay.value = '--';
    }
  } catch (e) { /* ignore */ }
  if (handsModel) {
    try { await handsModel.send({ image: video.value }); } catch {}
  }
  detectRaf = requestAnimationFrame(detectLoop);
}

function renderLoop(now) {
  if (lastRender) {
    framesAcc++;
    if (now - fpsTick > 1000) { fps.value = framesAcc; framesAcc = 0; fpsTick = now; }
  } else { fpsTick = now; }
  lastRender = now;
  const c = overlay.value;
  if (c && video.value) {
    const w = video.value.videoWidth, h = video.value.videoHeight;
    if (c.width !== w) { c.width = w; c.height = h; }
    const ctx = c.getContext('2d');
    ctx.clearRect(0, 0, w, h);
    if (lastFace) {
      const b = lastFace.detection.box;
      ctx.strokeStyle = 'rgba(108,160,255,0.85)';
      ctx.lineWidth = 2;
      ctx.strokeRect(b.x, b.y, b.width, b.height);
    }
  }
  renderRaf = requestAnimationFrame(renderLoop);
}

defineExpose({
  captureDescriptor() {
    return lastFace ? Array.from(lastFace.descriptor) : null;
  },
  getBlinks() { return blinkCount.value; },
  resetBlinks() { blinkCount.value = 0; closedFrames = 0; eyeOpen = true; },
  forceBlink() { blinkCount.value++; emit('blink', blinkCount.value); }
});

onMounted(async () => {
  try {
    await setupCamera();
    await Promise.all([loadFaceApi(), loadHands()]);
    renderRaf = requestAnimationFrame(renderLoop);
    detectLoop();
  } catch (e) {
    faceState.value = 'error: ' + e.message;
  }
});

onBeforeUnmount(() => {
  cancelAnimationFrame(detectRaf);
  cancelAnimationFrame(renderRaf);
  if (video.value && video.value.srcObject) {
    video.value.srcObject.getTracks().forEach(t => t.stop());
  }
});
</script>

<style scoped>
.cam-wrap { position: relative; width: 320px; height: 240px; border-radius: 16px; overflow: hidden; border: 1px solid var(--border); background: #000; }
.cam-video { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
.cam-overlay { position: absolute; inset: 0; width: 100%; height: 100%; transform: scaleX(-1); pointer-events: none; }
.cam-hud { position: absolute; left: 8px; bottom: 8px; display: flex; flex-direction: column; gap: 4px; }
.pill { font-size: 11px; background: rgba(0,0,0,0.55); color: #fff; padding: 3px 8px; border-radius: 999px; backdrop-filter: blur(6px); }
.pill i { margin-right: 4px; }
.pill.ok { background: rgba(61,220,151,0.3); border: 1px solid rgba(61,220,151,0.6); }
.pill.dim { opacity: 0.5; }
</style>
