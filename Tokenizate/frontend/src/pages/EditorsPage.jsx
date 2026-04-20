import React, { useEffect, useState } from 'react'
import { editors } from '../api/api.js'
import { useAuth } from '../App.jsx'
import { Plus, Trash2, UserCheck, UserX, Shield, User, Star } from 'lucide-react'

const roleIcon = { admin: Shield, senior_editor: Star, editor: User }
const roleColor = { admin: '#6366f1', senior_editor: '#f59e0b', editor: '#22c55e' }
const roleLabel = { admin: 'Admin', senior_editor: 'Senior Editor', editor: 'Editor' }

function Modal({ open, onClose, children }) {
  if (!open) return null
  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', display: 'flex',
      alignItems: 'center', justifyContent: 'center', zIndex: 50,
    }} onClick={onClose}>
      <div style={{ background: '#1e293b', borderRadius: 14, padding: 28, width: 440, border: '1px solid #334155' }} onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )
}

export default function EditorsPage() {
  const { isAdmin } = useAuth()
  const [list, setList] = useState([])
  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'editor' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const load = () => editors.list().then(r => setList(r.data)).catch(() => {})

  useEffect(() => { load() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      await editors.create(form)
      setShowCreate(false)
      setForm({ name: '', email: '', password: '', role: 'editor' })
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear editor')
    } finally { setLoading(false) }
  }

  const handleDelete = async (id, name) => {
    if (!confirm(`¿Eliminar editor "${name}"?`)) return
    await editors.delete(id).catch(() => {})
    load()
  }

  const toggleActive = async (editor) => {
    await editors.update(editor.id, { is_active: !editor.is_active }).catch(() => {})
    load()
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: '#e2e8f0' }}>Editores</h1>
          <p style={{ color: '#64748b', fontSize: 13, marginTop: 2 }}>{list.length} editores registrados</p>
        </div>
        {isAdmin && (
          <button onClick={() => setShowCreate(true)} style={{
            display: 'flex', alignItems: 'center', gap: 6, padding: '10px 18px',
            background: '#6366f1', border: 'none', borderRadius: 8, color: 'white',
            fontSize: 14, cursor: 'pointer', fontWeight: 600,
          }}>
            <Plus size={16} /> Nuevo editor
          </button>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
        {list.map(ed => {
          const RoleIcon = roleIcon[ed.role] || User
          return (
            <div key={ed.id} style={{
              background: '#1e293b', border: '1px solid #334155', borderRadius: 12,
              padding: 20, opacity: ed.is_active ? 1 : 0.6,
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <div style={{ width: 44, height: 44, borderRadius: '50%', background: `${roleColor[ed.role]}22`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <RoleIcon size={20} color={roleColor[ed.role]} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, color: '#e2e8f0', fontSize: 14 }}>{ed.name}</div>
                    <div style={{ fontSize: 12, color: '#64748b' }}>{ed.email}</div>
                  </div>
                </div>
                <span style={{
                  padding: '3px 10px', borderRadius: 20, fontSize: 11, fontWeight: 600,
                  background: `${roleColor[ed.role]}22`, color: roleColor[ed.role],
                }}>{roleLabel[ed.role]}</span>
              </div>

              <div style={{ marginTop: 16, display: 'flex', gap: 8 }}>
                <span style={{
                  fontSize: 11, padding: '3px 8px', borderRadius: 6,
                  background: ed.is_active ? '#052e16' : '#1c1917',
                  color: ed.is_active ? '#4ade80' : '#78716c',
                }}>{ed.is_active ? 'Activo' : 'Inactivo'}</span>
                {ed.subscription && (
                  <span style={{ fontSize: 11, padding: '3px 8px', borderRadius: 6, background: '#1e1b4b', color: '#818cf8' }}>
                    {ed.subscription.plan?.display_name || 'Plan activo'}
                  </span>
                )}
              </div>

              {isAdmin && (
                <div style={{ marginTop: 14, display: 'flex', gap: 8 }}>
                  <button onClick={() => toggleActive(ed)} style={{
                    flex: 1, padding: '7px', border: '1px solid #334155', borderRadius: 8,
                    background: 'transparent', color: '#94a3b8', cursor: 'pointer', fontSize: 12,
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4,
                  }}>
                    {ed.is_active ? <><UserX size={13} /> Desactivar</> : <><UserCheck size={13} /> Activar</>}
                  </button>
                  <button onClick={() => handleDelete(ed.id, ed.name)} style={{
                    padding: '7px 12px', border: '1px solid #7f1d1d', borderRadius: 8,
                    background: 'transparent', color: '#ef4444', cursor: 'pointer',
                    display: 'flex', alignItems: 'center',
                  }}>
                    <Trash2 size={14} />
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Create Modal */}
      <Modal open={showCreate} onClose={() => setShowCreate(false)}>
        <h2 style={{ fontSize: 18, fontWeight: 700, color: '#e2e8f0', marginBottom: 20 }}>Nuevo editor</h2>
        <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {[
            { label: 'Nombre', key: 'name', type: 'text' },
            { label: 'Email', key: 'email', type: 'email' },
            { label: 'Contraseña', key: 'password', type: 'password' },
          ].map(({ label, key, type }) => (
            <div key={key}>
              <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>{label}</label>
              <input
                type={type} value={form[key]} onChange={e => setForm({ ...form, [key]: e.target.value })} required
                style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', boxSizing: 'border-box' }}
              />
            </div>
          ))}
          <div>
            <label style={{ display: 'block', fontSize: 12, color: '#94a3b8', marginBottom: 5 }}>Rol</label>
            <select value={form.role} onChange={e => setForm({ ...form, role: e.target.value })}
              style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 14 }}>
              <option value="editor">Editor</option>
              <option value="senior_editor">Senior Editor</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          {error && <div style={{ background: '#450a0a', borderRadius: 8, padding: '8px 12px', fontSize: 13, color: '#fca5a5' }}>{error}</div>}
          <div style={{ display: 'flex', gap: 10, marginTop: 4 }}>
            <button type="button" onClick={() => setShowCreate(false)} style={{ flex: 1, padding: '10px', background: '#334155', border: 'none', borderRadius: 8, color: '#94a3b8', cursor: 'pointer', fontSize: 14 }}>Cancelar</button>
            <button type="submit" disabled={loading} style={{ flex: 1, padding: '10px', background: '#6366f1', border: 'none', borderRadius: 8, color: 'white', cursor: 'pointer', fontSize: 14, fontWeight: 600 }}>
              {loading ? 'Creando...' : 'Crear editor'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
