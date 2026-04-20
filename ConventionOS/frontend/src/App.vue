<template>
  <router-view />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;600;700;900&display=swap');

:root {
  --primary: #7c3aed;
  --primary-hover: #6d28d9;
  --accent: #f59e0b;
  --danger: #ef4444;
  --success: #10b981;
  --bg: #07070d;
  --bg2: #0f0f1a;
  --bg3: #1a1a2e;
  --surface: #1e1e35;
  --border: rgba(255,255,255,0.07);
  --text: #e2e8f0;
  --text2: #64748b;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}

a { color: inherit; text-decoration: none; }

button { cursor: pointer; font-family: inherit; }

input, textarea, select {
  font-family: inherit;
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 8px;
  padding: 10px 14px;
  width: 100%;
  outline: none;
  transition: border-color 0.2s;
}

input:focus, textarea:focus, select:focus {
  border-color: var(--primary);
}

.btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: var(--primary);
  color: white;
}
.btn-primary:hover { background: var(--primary-hover); }

.btn-accent {
  background: var(--accent);
  color: #000;
}
.btn-accent:hover { opacity: 0.9; }

.btn-danger {
  background: var(--danger);
  color: white;
}
.btn-danger:hover { opacity: 0.85; }

.btn-ghost {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
}
.btn-ghost:hover { border-color: var(--primary); }

.btn-sm { padding: 6px 14px; font-size: 12px; }

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-success { background: rgba(16,185,129,0.15); color: #10b981; }
.badge-warning { background: rgba(245,158,11,0.15); color: #f59e0b; }
.badge-danger { background: rgba(239,68,68,0.15); color: #ef4444; }
.badge-primary { background: rgba(124,58,237,0.15); color: #7c3aed; }
.badge-info { background: rgba(59,130,246,0.15); color: #3b82f6; }

.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 13px; font-weight: 500; color: var(--text2); }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.8);
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
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h2 { margin-bottom: 20px; font-size: 20px; }

table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px 14px; text-align: left; border-bottom: 1px solid var(--border); font-size: 14px; }
th { color: var(--text2); font-weight: 500; font-size: 12px; text-transform: uppercase; }
tr:hover td { background: rgba(255,255,255,0.02); }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}

.stat-card .stat-label { font-size: 12px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }
.stat-card .stat-value { font-size: 28px; font-weight: 700; margin-top: 6px; }

.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.page-header h1 { font-size: 22px; font-weight: 700; }

.scrollbar::-webkit-scrollbar { width: 6px; }
.scrollbar::-webkit-scrollbar-track { background: transparent; }
.scrollbar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
