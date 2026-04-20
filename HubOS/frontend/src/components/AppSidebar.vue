<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-mark">
        <i data-lucide="layers" class="lucide-icon" style="width:20px;height:20px"></i>
      </div>
      <div class="brand-text">
        <div class="brand-name">HubOS</div>
        <div class="brand-ws">{{ auth.user?.workspace_name || '—' }}</div>
      </div>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section">General</div>
      <SidebarLink to="/dashboard" icon="layout-dashboard" label="Dashboard" />

      <div class="nav-section">CRM</div>
      <SidebarLink to="/contacts" icon="users" label="Contactos" />
      <SidebarLink to="/deals" icon="kanban" label="Deals" />

      <div class="nav-section">CMS</div>
      <SidebarLink to="/content" icon="file-text" label="Contenido" />
      <SidebarLink to="/templates" icon="layout-template" label="Plantillas" />

      <div class="nav-section">Mensajería</div>
      <SidebarLink to="/chat" icon="message-circle" label="Chat WhatsApp" />
    </nav>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-avatar">{{ initial }}</div>
        <div class="user-details">
          <div class="user-name">{{ auth.user?.name }}</div>
          <div class="user-role">{{ auth.user?.role }}</div>
        </div>
      </div>
      <button @click="logout" class="logout-btn" title="Cerrar sesión">
        <i data-lucide="log-out" class="lucide-icon" style="width:18px;height:18px"></i>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed, onMounted, h } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const initial = computed(() => (auth.user?.name || 'U')[0].toUpperCase())

async function logout() {
  await auth.logout()
  router.push('/login')
}

const SidebarLink = {
  props: ['to', 'icon', 'label'],
  setup(props) {
    return () => h(RouterLink, { to: props.to, class: 'nav-item', activeClass: 'active' }, {
      default: () => [
        h('i', { 'data-lucide': props.icon, class: 'lucide-icon', style: 'width:17px;height:17px' }),
        h('span', props.label),
      ],
    })
  },
}

function refreshIcons() { if (window.lucide) window.lucide.createIcons() }
onMounted(refreshIcons)
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  background: var(--bg2);
  border-right: 1px solid var(--border);
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow-y: auto;
}
.sidebar-brand {
  padding: 1.1rem 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  border-bottom: 1px solid var(--border);
}
.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: 9px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.brand-name { font-weight: 800; font-size: 0.95rem; letter-spacing: -0.3px; }
.brand-ws { font-size: 0.7rem; color: var(--text2); }

.sidebar-nav {
  flex: 1;
  padding: 0.75rem 0.6rem;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}
.nav-section {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text3);
  padding: 0.75rem 0.7rem 0.35rem;
  font-weight: 700;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.55rem 0.8rem;
  border-radius: 8px;
  color: var(--text2);
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.15s;
  cursor: pointer;
}
.nav-item:hover { background: rgba(99,102,241,0.1); color: var(--text); }
.nav-item.active { background: rgba(99,102,241,0.18); color: #a5b4fc; font-weight: 600; }

.sidebar-footer {
  padding: 0.9rem;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.user-info { display: flex; align-items: center; gap: 0.55rem; flex: 1; min-width: 0; }
.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  color: white;
  flex-shrink: 0;
}
.user-details { min-width: 0; }
.user-name { font-size: 0.82rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 0.7rem; color: var(--text3); text-transform: capitalize; }
.logout-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text2);
  width: 34px;
  height: 34px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}
.logout-btn:hover { border-color: var(--danger); color: var(--danger); }
</style>
