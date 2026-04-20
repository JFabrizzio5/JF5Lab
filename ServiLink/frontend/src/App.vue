<template>
  <router-view />
</template>

<style>
:root {
  --bg: #0a0a0f;
  --bg2: #111118;
  --bg3: #1a1a2e;
  --border: #2a2a3e;
  --text: #e2e8f0;
  --text2: #94a3b8;
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --accent: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --radius: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; }

.btn {
  display: inline-flex; align-items: center; gap: 6px; padding: 10px 20px;
  border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500;
  transition: all 0.2s; text-decoration: none;
}
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-hover); transform: translateY(-1px); }
.btn-secondary { background: var(--bg3); color: var(--text); border: 1px solid var(--border); }
.btn-secondary:hover { border-color: var(--primary); }
.btn-danger { background: var(--danger); color: white; }
.btn-accent { background: var(--accent); color: white; }
.btn-sm { padding: 6px 14px; font-size: 13px; }
.btn-lg { padding: 14px 28px; font-size: 16px; }

.card {
  background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px;
}
.card:hover { border-color: var(--primary); transition: border-color 0.2s; }

.badge {
  display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;
}
.badge-primary { background: rgba(99,102,241,0.2); color: var(--primary); }
.badge-accent { background: rgba(16,185,129,0.2); color: var(--accent); }
.badge-warning { background: rgba(245,158,11,0.2); color: var(--warning); }
.badge-danger { background: rgba(239,68,68,0.2); color: var(--danger); }

.input {
  width: 100%; background: var(--bg3); border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 14px; color: var(--text); font-size: 14px; outline: none; transition: border-color 0.2s;
}
.input:focus { border-color: var(--primary); }
.input::placeholder { color: var(--text2); }

.label { display: block; font-size: 13px; font-weight: 500; color: var(--text2); margin-bottom: 6px; }

.stat-card {
  background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; display: flex; flex-direction: column; gap: 8px;
}
.stat-value { font-size: 32px; font-weight: 700; }
.stat-label { font-size: 13px; color: var(--text2); }

.stars { color: #f59e0b; font-size: 14px; }
.avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
.avatar-lg { width: 64px; height: 64px; }

.layout { display: flex; min-height: 100vh; }
.sidebar {
  width: 240px; background: var(--bg2); border-right: 1px solid var(--border);
  padding: 24px 16px; display: flex; flex-direction: column; gap: 4px; flex-shrink: 0;
}
.sidebar-logo { font-size: 22px; font-weight: 800; padding: 0 8px 24px; color: var(--primary); }
.sidebar a {
  display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 8px;
  color: var(--text2); text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s;
}
.sidebar a:hover, .sidebar a.router-link-active { background: rgba(99,102,241,0.12); color: var(--text); }
.sidebar a.router-link-active { border-left: 3px solid var(--primary); }
.main-content { flex: 1; padding: 32px; overflow-y: auto; }
.page-header { margin-bottom: 28px; }
.page-title { font-size: 24px; font-weight: 700; }
.page-subtitle { color: var(--text2); margin-top: 4px; font-size: 14px; }

.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }

.table { width: 100%; border-collapse: collapse; }
.table th { text-align: left; padding: 12px 16px; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text2); border-bottom: 1px solid var(--border); }
.table td { padding: 14px 16px; border-bottom: 1px solid var(--border); font-size: 14px; }
.table tr:hover td { background: rgba(99,102,241,0.04); }

.status-pending { color: var(--warning); }
.status-accepted { color: var(--primary); }
.status-in_progress { color: #06b6d4; }
.status-completed { color: var(--accent); }
.status-cancelled { color: var(--danger); }

.tag {
  display: inline-block; padding: 2px 8px; background: var(--bg3); border: 1px solid var(--border);
  border-radius: 6px; font-size: 12px; color: var(--text2);
}
</style>
