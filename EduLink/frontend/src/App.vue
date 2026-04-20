<template>
  <div id="app-root">
    <AppSidebar v-if="showSidebar" />
    <main :class="showSidebar ? 'with-sidebar' : 'full-width'">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from './components/AppSidebar.vue'

const route = useRoute()
const publicRoutes = ['/', '/login', '/register']
const showSidebar = computed(() => !publicRoutes.includes(route.path))
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --primary: #f59e0b;
  --primary-dark: #d97706;
  --accent: #10b981;
  --accent-dark: #059669;
  --bg: #0f172a;
  --bg2: #1e293b;
  --bg3: #334155;
  --text: #f1f5f9;
  --text2: #94a3b8;
  --border: #334155;
  --danger: #ef4444;
  --success: #10b981;
  --warning: #f59e0b;
  --sidebar-width: 240px;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
}

#app-root {
  display: flex;
  min-height: 100vh;
}

main.with-sidebar {
  margin-left: var(--sidebar-width);
  flex: 1;
  min-height: 100vh;
  overflow-y: auto;
}

main.full-width {
  flex: 1;
  min-height: 100vh;
}

a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }

button { cursor: pointer; font-family: inherit; }

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--primary);
  color: #0f172a;
}
.btn-primary:hover { background: var(--primary-dark); }

.btn-accent {
  background: var(--accent);
  color: #fff;
}
.btn-accent:hover { background: var(--accent-dark); }

.btn-ghost {
  background: transparent;
  color: var(--text2);
  border: 1px solid var(--border);
}
.btn-ghost:hover { background: var(--bg3); color: var(--text); }

.btn-danger {
  background: var(--danger);
  color: #fff;
}
.btn-danger:hover { opacity: 0.85; }

.btn-sm { padding: 6px 14px; font-size: 12px; }

.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.badge-school {
  background: rgba(245, 158, 11, 0.2);
  color: var(--primary);
  border: 1px solid rgba(245, 158, 11, 0.4);
}

.badge-free {
  background: rgba(16, 185, 129, 0.2);
  color: var(--accent);
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.badge-price {
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.4);
}

.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 13px; color: var(--text2); margin-bottom: 6px; font-weight: 500; }
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
}
.form-group select option { background: var(--bg2); }

.stars { color: var(--primary); }

.page-header {
  padding: 24px 32px;
  border-bottom: 1px solid var(--border);
  background: var(--bg2);
}
.page-header h1 { font-size: 24px; font-weight: 700; }
.page-header p { color: var(--text2); font-size: 14px; margin-top: 4px; }

.page-content { padding: 32px; }

.grid-3 { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.grid-2 { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 20px; }

.stat-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}
.stat-card .stat-number { font-size: 36px; font-weight: 800; color: var(--primary); }
.stat-card .stat-label { color: var(--text2); font-size: 13px; margin-top: 4px; }

.alert {
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
}
.alert-error { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); color: #fca5a5; }
.alert-success { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #6ee7b7; }

.table-wrapper { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 10px 14px; font-size: 12px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid var(--border); }
td { padding: 12px 14px; font-size: 14px; border-bottom: 1px solid rgba(51, 65, 85, 0.5); }
tr:hover td { background: rgba(255,255,255,0.02); }

.empty-state { text-align: center; padding: 60px 20px; }
.empty-state h3 { font-size: 18px; margin-bottom: 8px; }
.empty-state p { color: var(--text2); font-size: 14px; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}
.modal {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  width: 100%;
  max-width: 480px;
  max-height: 80vh;
  overflow-y: auto;
}
.modal h2 { font-size: 20px; font-weight: 700; margin-bottom: 20px; }

.loading { text-align: center; padding: 60px; color: var(--text2); font-size: 16px; }
</style>
