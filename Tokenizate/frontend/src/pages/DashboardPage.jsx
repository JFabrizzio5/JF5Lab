import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { reviews } from '../api/api.js'
import { useAuth } from '../App.jsx'
import { FileText, CheckCircle, Clock, AlertTriangle, XCircle, TrendingUp, Plus } from 'lucide-react'

const statusColor = {
  draft: '#64748b',
  in_review: '#3b82f6',
  revision_required: '#f59e0b',
  approved: '#22c55e',
  rejected: '#ef4444',
}

const statusLabel = {
  draft: 'Borrador',
  in_review: 'En revisión',
  revision_required: 'Requiere revisión',
  approved: 'Aprobado',
  rejected: 'Rechazado',
}

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div style={{
      background: '#1e293b', border: '1px solid #334155', borderRadius: 12, padding: 20,
      display: 'flex', alignItems: 'center', gap: 16,
    }}>
      <div style={{ width: 48, height: 48, borderRadius: 12, background: `${color}22`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Icon size={22} color={color} />
      </div>
      <div>
        <div style={{ fontSize: 28, fontWeight: 700, color: '#e2e8f0' }}>{value}</div>
        <div style={{ fontSize: 13, color: '#64748b' }}>{label}</div>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const { editor } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [recent, setRecent] = useState([])

  useEffect(() => {
    reviews.stats().then(r => setStats(r.data)).catch(() => {})
    reviews.list().then(r => setRecent(r.data.slice(0, 5))).catch(() => {})
  }, [])

  return (
    <div>
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, color: '#e2e8f0' }}>Hola, {editor?.name} 👋</h1>
        <p style={{ color: '#64748b', fontSize: 14, marginTop: 4 }}>Panel de control — Editorial Manager</p>
      </div>

      {/* Stats */}
      {stats && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16, marginBottom: 32 }}>
          <StatCard icon={FileText} label="Total revisiones" value={stats.total} color="#6366f1" />
          <StatCard icon={Clock} label="En revisión" value={stats.in_review} color="#3b82f6" />
          <StatCard icon={AlertTriangle} label="Requiere revisión" value={stats.revision_required} color="#f59e0b" />
          <StatCard icon={CheckCircle} label="Aprobadas" value={stats.approved} color="#22c55e" />
          <StatCard icon={XCircle} label="Rechazadas" value={stats.rejected} color="#ef4444" />
        </div>
      )}

      {/* Recent reviews */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, overflow: 'hidden' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid #334155', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontWeight: 600, color: '#e2e8f0', fontSize: 15 }}>Revisiones recientes</span>
          <button
            onClick={() => navigate('/reviews/new')}
            style={{
              display: 'flex', alignItems: 'center', gap: 6, padding: '6px 14px',
              background: '#6366f1', border: 'none', borderRadius: 8, color: 'white',
              fontSize: 13, cursor: 'pointer', fontWeight: 600,
            }}
            onClick={() => navigate('/reviews')}
          >
            <Plus size={15} /> Nueva revisión
          </button>
        </div>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#0f172a' }}>
              {['Título', 'Estado', 'Prioridad', 'Editor asignado', 'Fecha'].map(h => (
                <th key={h} style={{ padding: '10px 16px', textAlign: 'left', fontSize: 12, color: '#64748b', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {recent.length === 0 ? (
              <tr><td colSpan={5} style={{ padding: 32, textAlign: 'center', color: '#475569', fontSize: 14 }}>Sin revisiones todavía</td></tr>
            ) : recent.map(r => (
              <tr
                key={r.id}
                onClick={() => navigate(`/reviews/${r.id}`)}
                style={{ borderTop: '1px solid #334155', cursor: 'pointer', transition: 'background 0.1s' }}
                onMouseEnter={e => e.currentTarget.style.background = '#0f172a'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                <td style={{ padding: '12px 16px', fontSize: 14, color: '#e2e8f0', fontWeight: 500 }}>{r.title}</td>
                <td style={{ padding: '12px 16px' }}>
                  <span style={{
                    display: 'inline-block', padding: '3px 10px', borderRadius: 20,
                    fontSize: 12, fontWeight: 600,
                    background: `${statusColor[r.status]}22`, color: statusColor[r.status],
                  }}>{statusLabel[r.status]}</span>
                </td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#94a3b8', textTransform: 'capitalize' }}>{r.priority}</td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#94a3b8' }}>{r.assigned_editor?.name || '—'}</td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#64748b' }}>{new Date(r.created_at).toLocaleDateString('es')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
