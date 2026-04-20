import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3002,
    proxy: {
      '/api': {
        target: 'http://172.21.0.4:8000',
        rewrite: path => path.replace(/^\/api/, '')
      }
    }
  }
})
