import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3065,
    proxy: {
      '/api': { target: 'http://api:8000', changeOrigin: true, rewrite: p => p.replace(/^\/api/, '') },
      '/ws': { target: 'ws://api:8000', ws: true, rewrite: p => p.replace(/^\/ws/, '') }
    }
  }
});
