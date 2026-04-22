import axios from 'axios';

const api = axios.create({
  baseURL: '/api/social/v1',
  headers: { 'Content-Type': 'application/json' }
});

api.interceptors.request.use((cfg) => {
  const t = localStorage.getItem('upi_token');
  if (t) cfg.headers.Authorization = `Bearer ${t}`;
  return cfg;
});

export const demoSeed = () => api.post('/demo/seed').then(r => r.data);
export const register = (data) => api.post('/auth/register', data).then(r => r.data);
export const login = (data) => api.post('/auth/login', data).then(r => r.data);
export const me = () => api.get('/auth/me').then(r => r.data);
export const getFeed = (limit = 30) => api.get('/feed', { params: { limit } }).then(r => r.data);
export const createPost = (data) => api.post('/posts', data).then(r => r.data);
export const toggleLike = (id) => api.post(`/posts/${id}/like`).then(r => r.data);
export const getComments = (id) => api.get(`/posts/${id}/comments`).then(r => r.data);
export const addComment = (id, content) => api.post(`/posts/${id}/comments`, { content }).then(r => r.data);
export const getProfile = (username) => api.get(`/users/${username}`).then(r => r.data);
export const searchUsers = (q = '') => api.get('/users', { params: { q } }).then(r => r.data);
