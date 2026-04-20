import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { reviews, editors } from '../api/api.js'
import { Plus, Filter, Search } from 'lucide-react'

const statusColor = { draft: '#64748b', in_review: '#3b82f6', revision_required: '#f59e0b', approved: '#22c55e', rejected: '#ef4444' }
const statusLabel = { draft: 'Borrador', in_review: 'En revisión', revision_required: 'Requiere revisión', approved: 'Aprobado', rejected: 'Rechazado' }
const priorityColor = { low: '#22c55e', medium: '#3b82f6', high: '#f59e0b', urgent: '#ef4444' }

function Modal({ open, onClose, children }) {
  if (!open) return null
  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 50 }} onClick={onClose}>
      <div style={{ background: '#1e293b', borderRadius: 14, padding: 28, width: 500, border: '1px solid #334155', maxHeight: '90vh', overflow: 'auto' }} onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )
}

export default function ReviewsPage() {
  const navigate = useNavigate()
  const [list, setList] = useState([])
  const [editorList, setEditorList] = useState([])
  const [showCreate, setShowCreate] = useState(false)
  const [filterStatus, setFilterStatus] = useState('')
  const [search, setSearch] = useState('')
  const [form, setForm] = useState({ title: '', description: '', content_url: '', priority: 'medium', assigned_editor_id: '', deadline: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const load = () => {
    reviews.list(filterStatus ? { status: filterStatus } : {}).then(r => setList(r.data)).catch(() => {})
  }

  useEffect(() => { load() }, [filterStatus])
  useEffect(() => { editors.list().then(r => setEditorList(r.data)).catch(() => {}) }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      const payload = { ...form }
      if (!payload.assigned_editor_id) delete payload.assigned_editor_id
      if (!payload.deadline) delete payload.deadline
      if (payload.assigned_editor_id) payload.assigned_editor_id = parseInt(payload.assigned_editor_id)
      await reviews.create(payload)
      setShowCreate(false)
      setForm({ title: '', description: '', content_url: '', priority: 'medium', assigned_editor_id: '', deadline: '' })
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear revisión')
    } finally { setLoading(false) }
  }

  const filtered = list.filter(r => !search || r.title.toLowerCase().includes(search.toLowerCase()))

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: '#e2e8f0' }}>Revisiones</h1>
          <p style={{ color: '#64748b', fontSize: 13, marginTop: 2 }}>{filtered.length} revisiones</p>
        </div>
        <button onClick={() => setShowCreate(true)} style={{
          display: 'flex', alignItems: 'center', gap: 6, padding: '10px 18px',
          background: '#6366f1', border: 'none', borderRadius: 8, color: 'white', fontSize: 14, cursor: 'pointer', fontWeight: 600,
        }}>
          <Plus size={16} /> Nueva revisión
        </button>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <Search size={15} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            placeholder="Buscar revisiones..."
            value={search} onChange={e => setSearch(e.target.value)}
            style={{ width: '100%', padding: '9px 12px 9px 36px', background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', boxSizing: 'border-box' }}
          />
        </div>
        <select value={filterStatus} onChange={e => setFilterStatus(e.target.value)}
          style={{ padding: '9px 14px', background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#94a3b8', fontSize: 13 }}>
          <option value="">Todos los estados</option>
          <option value="draft">Borrador</option>
          <option value="in_review">En revisión</option>
          <option value="revision_required">Requiere revisión</option>
          <option value="approved">Aprobado</option>
          <option value="rejected">Rechazado</option>
        </select>
      </div>

      {/* Table */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#0f172a' }}>
              {['Título', 'Estado', 'Prioridad', 'Asignado a', 'Fecha límite', 'Creado'].map(h => (
                <th key={h} style={{ padding: '10px 16px', textAlign: 'left', fontSize: 11, color: '#64748b', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={6} style={{ padding: 40, textAlign: 'center', color: '#475569', fontSize: 14 }}>Sin revisiones</td></tr>
            ) : filtered.map(r => (
              <tr key={r.id}
                onClick={() => navigate(`/reviews/${r.id}`)}
                style={{ borderTop: '1px solid #334155', cursor: 'pointer' }}
                onMouseEnter={e => e.currentTarget.style.background = '#0f172a'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                <td style={{ padding: '12px 16px', fontSize: 14, color: '#e2e8f0', fontWeight: 500, maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{r.title}</td>
                <td style={{ padding: '12px 16px' }}>
                  <span style={{ display: 'inline-block', padding: '3px 10px', borderRadius: 20, fontSize: 12, fontWeight: 600, background: `${statusColor[r.status]}22`, color: statusColor[r.status] }}>
                    {statusLabel[r.status]}
                  </span>
                </td>
                <td style={{ padding: '12px 16px' }}>
                  <span style={{ display: 'inline-block', padding: '3px 10px', borderRadius: 20, fontSize: 12, fontWeight: 600, background: `${priorityColor[r.priority]}22`, color: priorityColor[r.priority], textTransform: 'capitalize' }}>
                    {r.priority}
                  </span>
                </td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#94a3b8' }}>{r.assigned_editor?.name || '—'}</td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: r.deadline && new Date(r.deadline) < new Date() ? '#ef4444' : '#94a3b8' }}>
                  {r.deadline ? new Date(r.deadline).toLocaleDateString('es') : '—'}
                </td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#64748b' }}>{new Date(r.created_at).toLocaleDateString('es')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create Modal */}
      <Modal open={showCreate} onClose={() => setShowCreate(false)}>
        <h2 style={{ fontSize: 18, fontWeight: 700, color: '#e2e8f0', marginBottom: 20 }}>Nueva revisión</h2>
        <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div>
            <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>Título *</label>
            <input type="text" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} required
              style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', boxSizing: 'border-box' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>Descripción</label>
            <textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} rows={3}
              style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', resize: 'vertical', boxSizing: 'border-box' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>URL del contenido</label>
            <input type="url" value={form.content_url} onChange={e => setForm({ ...form, content_url: e.target.value })}
              style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', boxSizing: 'border-box' }} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div>
              <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>Prioridad</label>
              <select value={form.priority} onChange={e => setForm({ ...form, priority: e.target.value })}
                style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14 }}>
                <option value="low">Baja</option>
                <option value="medium">Media</option>
                <option value="high">Alta</option>
                <option value="urgent">Urgente</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>Asignar editor</label>
              <select value={form.assigned_editor_id} onChange={e => setForm({ ...form, assigned_editor_id: e.target.value })}
                style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14 }}>
                <option value="">Sin asignar</option>
                {editorList.map(ed => <option key={ed.id} value={ed.id}>{ed.name}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>Fecha límite</label>
            <input type="datetime-local" value={form.deadline} onChange={e => setForm({ ...form, deadline: e.target.value })}
              style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', boxSizing: 'border-box' }} />
          </div>
          {error && <div style={{ background: '#450a0a', borderRadius: 8, padding: '8px 12px', fontSize: 13, color: '#fca5a5' }}>{error}</div>}
          <div style={{ display: 'flex', gap: 10, marginTop: 4 }}>
            <button type="button" onClick={() => setShowCreate(false)} style={{ flex: 1, padding: '10px', background: '#334155', border: 'none', borderRadius: 8, color: '#94a3b8', cursor: 'pointer', fontSize: 14 }}>Cancelar</button>
            <button type="submit" disabled={loading} style={{ flex: 1, padding: '10px', background: '#6366f1', border: 'none', borderRadius: 8, color: 'white', cursor: 'pointer', fontSize: 14, fontWeight: 600 }}>
              {loading ? 'Creando...' : 'Crear revisión'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
