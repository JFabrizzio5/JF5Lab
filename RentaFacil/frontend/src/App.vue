<template>
  <div id="rf-app">
    <nav v-if="authStore.isAuthenticated" class="sidebar">
      <div class="logo">🏠 RentaFácil</div>
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/properties">Propiedades</router-link>
      <router-link to="/tenants">Inquilinos</router-link>
      <router-link to="/contracts">Contratos</router-link>
      <router-link to="/payments">Pagos</router-link>
      <button class="logout-btn" @click="logout">Cerrar sesión</button>
    </nav>
    <main :class="{ 'with-sidebar': authStore.isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', sans-serif; background: #f5f7fa; color: #1a1a2e; }

#rf-app { display: flex; min-height: 100vh; }

.sidebar {
  width: 220px;
  background: #1a1a2e;
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  gap: 8px;
  position: fixed;
  top: 0; left: 0;
  height: 100vh;
}
.logo { font-size: 1.2rem; font-weight: 700; padding: 8px 0 20px; border-bottom: 1px solid #2d2d4e; margin-bottom: 8px; }
.sidebar a { color: #a0aec0; text-decoration: none; padding: 10px 12px; border-radius: 8px; font-size: 0.9rem; transition: all 0.2s; }
.sidebar a:hover, .sidebar a.router-link-active { background: #2d2d4e; color: #fff; }
.logout-btn { margin-top: auto; background: transparent; border: 1px solid #2d2d4e; color: #a0aec0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 0.9rem; text-align: left; }
.logout-btn:hover { background: #2d2d4e; color: #fff; }

main { flex: 1; padding: 32px; }
main.with-sidebar { margin-left: 220px; }

/* Shared components */
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; font-size: 0.9rem; font-weight: 500; transition: all 0.2s; }
.btn-primary { background: #4f46e5; color: #fff; }
.btn-primary:hover { background: #4338ca; }
.btn-danger { background: #ef4444; color: #fff; }
.btn-danger:hover { background: #dc2626; }
.btn-secondary { background: #e2e8f0; color: #1a1a2e; }
.btn-secondary:hover { background: #cbd5e0; }
.btn-success { background: #10b981; color: #fff; }
.btn-success:hover { background: #059669; }
.card { background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 10px 12px; font-size: 0.8rem; font-weight: 600; color: #64748b; border-bottom: 2px solid #e2e8f0; text-transform: uppercase; letter-spacing: 0.04em; }
td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #f8fafc; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.badge-green { background: #d1fae5; color: #065f46; }
.badge-yellow { background: #fef3c7; color: #92400e; }
.badge-red { background: #fee2e2; color: #991b1b; }
.badge-gray { background: #f1f5f9; color: #475569; }
.badge-blue { background: #dbeafe; color: #1e40af; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
label { font-size: 0.85rem; font-weight: 500; color: #374151; }
input, select, textarea { padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 0.9rem; font-family: inherit; outline: none; transition: border-color 0.2s; }
input:focus, select:focus, textarea:focus { border-color: #4f46e5; box-shadow: 0 0 0 3px rgba(79,70,229,0.1); }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.error-msg { color: #ef4444; font-size: 0.85rem; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; border-radius: 12px; padding: 28px; width: 100%; max-width: 540px; max-height: 90vh; overflow-y: auto; }
.modal-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 24px; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.stat-label { font-size: 0.8rem; color: #64748b; font-weight: 500; margin-bottom: 6px; }
.stat-value { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; }
.stat-value.green { color: #10b981; }
.stat-value.red { color: #ef4444; }
.empty { text-align: center; padding: 40px; color: #94a3b8; font-size: 0.9rem; }
</style>
