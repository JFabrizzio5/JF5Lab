<template>
  <canvas ref="cnv" class="waves"></canvas>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';

const cnv = ref(null);
let gl, prog, start = performance.now(), raf = 0;

const vs = `
attribute vec2 p;
void main(){ gl_Position = vec4(p, 0., 1.); }`;

const fs = `
precision highp float;
uniform vec2 uR;
uniform float uT;
void main(){
  vec2 uv = (gl_FragCoord.xy / uR) * 2.0 - 1.0;
  uv.x *= uR.x / uR.y;
  float t = uT * 0.35;
  float acc = 0.0;
  for(float i=1.0; i<=5.0; i++){
    float k = i * 1.3;
    acc += sin(uv.x * k * 1.5 + t * (1.0 + i*0.15)) * 0.14 / i;
    acc += cos(uv.y * k * 1.2 + t * (0.6 + i*0.12)) * 0.11 / i;
  }
  float mask = smoothstep(0.35, 0.0, abs(uv.y - acc*2.2));
  vec3 c1 = vec3(0.42, 0.62, 1.0);
  vec3 c2 = vec3(0.62, 0.48, 1.0);
  vec3 col = mix(c1, c2, 0.5 + 0.5*sin(t + uv.x*1.5));
  vec3 bg = vec3(0.043, 0.047, 0.063);
  vec3 final = mix(bg, col, mask * 0.9);
  final += 0.04 * vec3(0.3 + 0.5*sin(t*0.7), 0.25, 0.4);
  gl_FragColor = vec4(final, 1.0);
}`;

function compile(type, src) {
  const s = gl.createShader(type);
  gl.shaderSource(s, src);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
  return s;
}

function resize() {
  const c = cnv.value;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  c.width = Math.floor(innerWidth * dpr);
  c.height = Math.floor(innerHeight * dpr);
  c.style.width = innerWidth + 'px';
  c.style.height = innerHeight + 'px';
  gl.viewport(0, 0, c.width, c.height);
}

function frame() {
  const t = (performance.now() - start) / 1000;
  gl.uniform1f(gl.getUniformLocation(prog, 'uT'), t);
  gl.uniform2f(gl.getUniformLocation(prog, 'uR'), cnv.value.width, cnv.value.height);
  gl.drawArrays(gl.TRIANGLES, 0, 6);
  raf = requestAnimationFrame(frame);
}

onMounted(() => {
  gl = cnv.value.getContext('webgl', { antialias: false, powerPreference: 'high-performance' });
  prog = gl.createProgram();
  gl.attachShader(prog, compile(gl.VERTEX_SHADER, vs));
  gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(prog);
  gl.useProgram(prog);
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, 'p');
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  resize();
  addEventListener('resize', resize);
  frame();
});

onBeforeUnmount(() => {
  cancelAnimationFrame(raf);
  removeEventListener('resize', resize);
});
</script>

<style scoped>
.waves {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}
</style>
