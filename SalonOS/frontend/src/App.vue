<template>
  <div id="salonos-app">
    <template v-if="!isLanding && isAuthenticated">
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
const isLanding = computed(() => !!route.meta.landing || !!route.meta.guest)
const isAuthenticated = computed(() => !!localStorage.getItem('salonos_token'))
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --primary: #7c3aed;
  --primary-dark: #5b21b6;
  --accent: #f59e0b;
  --bg: #0a0a0f;
  --bg2: #111118;
  --surface: #1a1a2e;
  --surface2: #16213e;
  --border: rgba(255,255,255,0.08);
  --text: #e2e8f0;
  --text2: #64748b;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

#salonos-app {
  min-height: 100vh;
}

.main-content {
  margin-left: 240px;
  min-height: 100vh;
  background: var(--bg);
  overflow-x: hidden;
}

.page-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid var(--border);
}

.page-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text);
}

.page-header p {
  color: var(--text2);
  margin-top: 0.25rem;
}

.page-body {
  padding: 2rem;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-primary {
  background: var(--primary);
  color: white;
}
.btn-primary:hover { background: var(--primary-dark); }

.btn-accent {
  background: var(--accent);
  color: #1a1a1a;
}
.btn-accent:hover { opacity: 0.9; }

.btn-ghost {
  background: transparent;
  color: var(--text);
  border: 1px solid var(--border);
}
.btn-ghost:hover { background: var(--surface); }

.btn-danger {
  background: var(--danger);
  color: white;
}
.btn-danger:hover { opacity: 0.85; }

.btn-sm {
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
}

input, select, textarea {
  background: var(--bg2);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 8px;
  padding: 0.6rem 0.9rem;
  font-size: 0.9rem;
  width: 100%;
  outline: none;
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--primary);
}

label {
  display: block;
  font-size: 0.85rem;
  color: var(--text2);
  margin-bottom: 0.35rem;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-inquiry { background: rgba(100,116,139,0.2); color: #94a3b8; }
.badge-quote_sent { background: rgba(59,130,246,0.2); color: #60a5fa; }
.badge-confirmed { background: rgba(16,185,129,0.2); color: #34d399; }
.badge-deposit_paid { background: rgba(124,58,237,0.2); color: #a78bfa; }
.badge-completed { background: rgba(245,158,11,0.2); color: #fbbf24; }
.badge-cancelled { background: rgba(239,68,68,0.2); color: #f87171; }
.badge-web { background: rgba(59,130,246,0.2); color: #60a5fa; }
.badge-whatsapp { background: rgba(16,185,129,0.2); color: #34d399; }
.badge-referral { background: rgba(245,158,11,0.2); color: #fbbf24; }
.badge-direct { background: rgba(124,58,237,0.2); color: #a78bfa; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h2 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

th {
  font-size: 0.8rem;
  color: var(--text2);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td { font-size: 0.9rem; }

tr:hover td { background: rgba(255,255,255,0.02); }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem;
}

.stat-card .stat-label {
  font-size: 0.8rem;
  color: var(--text2);
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.stat-card .stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text);
}

.stat-card .stat-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .main-content { margin-left: 0; }
}
</style>
