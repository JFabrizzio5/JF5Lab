import React, { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../App.jsx'
import { LayoutDashboard, Users, FileText, CreditCard, LogOut, Menu, X, BookOpen } from 'lucide-react'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/reviews', label: 'Revisiones', icon: FileText },
  { to: '/editors', label: 'Editores', icon: Users, adminOnly: true },
  { to: '/plans', label: 'Planes', icon: CreditCard },
]

export default function Layout() {
  const { editor, logout, isAdmin } = useAuth()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleLogout = () => { logout(); navigate('/login') }

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#0f172a' }}>
      {/* Sidebar */}
      <aside style={{
        width: sidebarOpen ? 240 : 64,
        background: '#1e293b',
        borderRight: '1px solid #334155',
        display: 'flex',
        flexDirection: 'column',
        transition: 'width 0.2s',
        overflow: 'hidden',
        flexShrink: 0,
      }}>
        {/* Logo */}
        <div style={{ padding: '20px 16px', borderBottom: '1px solid #334155', display: 'flex', alignItems: 'center', gap: 10 }}>
          <BookOpen size={24} color="#6366f1" />
          {sidebarOpen && <span style={{ fontWeight: 700, fontSize: 16, color: '#e2e8f0', whiteSpace: 'nowrap' }}>Editorial Manager</span>}
        </div>

        {/* Nav */}
        <nav style={{ flex: 1, padding: '12px 8px', display: 'flex', flexDirection: 'column', gap: 4 }}>
          {navItems.filter(i => !i.adminOnly || isAdmin).map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              style={({ isActive }) => ({
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '10px 12px',
                borderRadius: 8,
                textDecoration: 'none',
                color: isActive ? '#6366f1' : '#94a3b8',
                background: isActive ? '#312e81' : 'transparent',
                fontWeight: isActive ? 600 : 400,
                fontSize: 14,
                whiteSpace: 'nowrap',
                transition: 'all 0.15s',
              })}
            >
              <Icon size={18} />
              {sidebarOpen && label}
            </NavLink>
          ))}
        </nav>

        {/* User info */}
        <div style={{ padding: '12px 8px', borderTop: '1px solid #334155' }}>
          {sidebarOpen && (
            <div style={{ padding: '8px 12px', marginBottom: 8 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: '#e2e8f0', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{editor?.name}</div>
              <div style={{ fontSize: 11, color: '#64748b', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{editor?.role}</div>
            </div>
          )}
          <button
            onClick={handleLogout}
            style={{
              display: 'flex', alignItems: 'center', gap: 10, width: '100%',
              padding: '10px 12px', borderRadius: 8, border: 'none',
              background: 'transparent', color: '#ef4444', cursor: 'pointer',
              fontSize: 14, whiteSpace: 'nowrap',
            }}
          >
            <LogOut size={18} />
            {sidebarOpen && 'Cerrar sesión'}
          </button>
        </div>
      </aside>

      {/* Main */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Topbar */}
        <header style={{
          height: 56, background: '#1e293b', borderBottom: '1px solid #334155',
          display: 'flex', alignItems: 'center', padding: '0 20px', gap: 12,
        }}>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#94a3b8', display: 'flex', alignItems: 'center' }}
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <span style={{ color: '#e2e8f0', fontWeight: 600, fontSize: 15 }}>Editorial Manager</span>
        </header>

        {/* Content */}
        <main style={{ flex: 1, overflow: 'auto', padding: 24 }}>
          <Outlet />
        </main>
      </div>
    </div>
  )
}
