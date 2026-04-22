import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 3075,
    proxy: {
      '/api': { target: 'http://api:8000', changeOrigin: true, rewrite: p => p.replace(/^\/api/, '') }
    }
  }
});
