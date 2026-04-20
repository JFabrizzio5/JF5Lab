<template>
  <div id="negocioos">
    <template v-if="showLayout">
      <AppSidebar />
      <main class="main-content">
        <router-view />
      </main>
    </template>
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from './components/AppSidebar.vue'

const route = useRoute()
const noLayoutRoutes = ['Landing', 'Login', 'Register']
const showLayout = computed(() => !noLayoutRoutes.includes(route.name))
</script>

<style>
:root {
  --primary: #f97316;
  --primary-dark: #ea6c0a;
  --accent: #6366f1;
  --accent-dark: #4f46e5;
  --bg: #0f1117;
  --bg2: #1a1d27;
  --bg3: #252837;
  --border: #2e3148;
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #f59e0b;
  --sidebar-width: 240px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}

#negocioos {
  min-height: 100vh;
}

.main-content {
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  overflow-x: hidden;
}

@media (max-width: 768px) {
  .main-content { margin-left: 0; }
}

a { color: inherit; text-decoration: none; }

button {
  cursor: pointer;
  border: none;
  font-family: inherit;
}

input, select, textarea {
  font-family: inherit;
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 8px;
  padding: 8px 12px;
  outline: none;
  width: 100%;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--primary);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--primary);
  color: white;
}
.btn-primary:hover { background: var(--primary-dark); }

.btn-accent {
  background: var(--accent);
  color: white;
}
.btn-accent:hover { background: var(--accent-dark); }

.btn-ghost {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border);
}
.btn-ghost:hover { border-color: var(--primary); color: var(--primary); }

.btn-danger {
  background: var(--danger);
  color: white;
}

.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge-danger { background: rgba(239,68,68,0.15); color: var(--danger); }
.badge-success { background: rgba(34,197,94,0.15); color: var(--success); }
.badge-warning { background: rgba(245,158,11,0.15); color: var(--warning); }
.badge-primary { background: rgba(249,115,22,0.15); color: var(--primary); }
.badge-accent { background: rgba(99,102,241,0.15); color: var(--accent); }

.page-header {
  padding: 24px 28px 0;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text);
}

.page-header p {
  color: var(--text-muted);
  font-size: 14px;
  margin-top: 4px;
}

.page-body {
  padding: 0 28px 28px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
}

td {
  padding: 12px 14px;
  font-size: 14px;
  border-bottom: 1px solid var(--border);
}

tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--bg3); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
