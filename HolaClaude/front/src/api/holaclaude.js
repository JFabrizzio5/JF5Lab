import axios from 'axios';

const api = axios.create({
  baseURL: '/api/holaclaude/v1',
  headers: { 'Content-Type': 'application/json' }
});

export const getStatus = () => api.get('/status').then(r => r.data);
export const enrollFace = (descriptor) => api.post('/enroll', { descriptor }).then(r => r.data);
export const verifyFace = (descriptor, liveness_blinks) =>
  api.post('/verify', { descriptor, liveness_blinks }).then(r => r.data);
export const disableWithPin = (pin) => api.post('/disable', { pin }).then(r => r.data);
export const resetWithPin = (pin, descriptor) => api.post('/reset', { pin, descriptor }).then(r => r.data);
export const fetchGestures = () => api.get('/gestures').then(r => r.data);

export function openAgentWs(token, onMsg) {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  const ws = new WebSocket(`${proto}://${location.host}/api/holaclaude/v1/ws/agent?token=${encodeURIComponent(token)}`);
  ws.onmessage = e => { try { onMsg(JSON.parse(e.data)); } catch { onMsg({ type: 'raw', data: e.data }); } };
  return ws;
}
