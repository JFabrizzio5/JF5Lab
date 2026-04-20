<template>
  <router-view />
</template>

<style>
:root {
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --accent: #f59e0b;
  --danger: #ef4444;
  --success: #10b981;
  --warning: #f59e0b;
  --bg: #07070d;
  --bg2: #0f0f1a;
  --bg3: #1a1a2e;
  --surface: #1e1e35;
  --border: rgba(255, 255, 255, 0.07);
  --border2: rgba(255, 255, 255, 0.12);
  --text: #e2e8f0;
  --text2: #64748b;
  --text3: #94a3b8;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  line-height: 1.6;
}

.layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 28px;
  overflow-y: auto;
  min-height: 100vh;
}

.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
}

.input {
  width: 100%;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.input:focus {
  border-color: var(--primary);
}

.input::placeholder {
  color: var(--text2);
}

textarea.input {
  resize: vertical;
  min-height: 80px;
}

select.input {
  cursor: pointer;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  text-decoration: none;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-accent {
  background: var(--accent);
  color: #07070d;
}

.btn-accent:hover:not(:disabled) {
  background: #d97706;
  transform: translateY(-1px);
}

.btn-secondary {
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text3);
}

.btn-secondary:hover:not(:disabled) {
  border-color: var(--border2);
  color: var(--text);
}

.btn-danger {
  background: var(--danger);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-success {
  background: var(--success);
  color: white;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
  margin-bottom: 6px;
}

.form-group {
  margin-bottom: 16px;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.badge-primary { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
.badge-success { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.badge-warning { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.badge-danger { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.badge-gray { background: rgba(100, 116, 139, 0.15); color: #94a3b8; }

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}

.page-subtitle {
  color: var(--text2);
  font-size: 14px;
  margin-bottom: 24px;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

@media (max-width: 768px) {
  .grid-2, .grid-3, .grid-4 {
    grid-template-columns: 1fr;
  }
  .main-content {
    padding: 16px;
  }
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.modal {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 16px;
  padding: 28px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-lg {
  max-width: 900px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
}

.modal-close {
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text2);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.2s;
}

.modal-close:hover {
  color: var(--text);
  border-color: var(--border2);
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bg3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--surface); }
</style>
