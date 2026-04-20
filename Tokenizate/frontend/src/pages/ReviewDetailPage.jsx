import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { reviews, editors } from '../api/api.js'
import { ArrowLeft, Send, Clock, User, Tag, AlertCircle } from 'lucide-react'

const statusColor = { draft: '#64748b', in_review: '#3b82f6', revision_required: '#f59e0b', approved: '#22c55e', rejected: '#ef4444' }
const statusLabel = { draft: 'Borrador', in_review: 'En revisión', revision_required: 'Requiere revisión', approved: 'Aprobado', rejected: 'Rechazado' }
const statusOptions = ['draft', 'in_review', 'revision_required', 'approved', 'rejected']

export default function ReviewDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [review, setReview] = useState(null)
  const [editorList, setEditorList] = useState([])
  const [comment, setComment] = useState('')
  const [newStatus, setNewStatus] = useState('')
  const [statusNote, setStatusNote] = useState('')
  const [loading, setLoading] = useState(false)

  const load = () => reviews.get(id).then(r => setReview(r.data)).catch(() => navigate('/reviews'))

  useEffect(() => {
    load()
    editors.list().then(r => setEditorList(r.data)).catch(() => {})
  }, [id])

  const handleComment = async (e) => {
    e.preventDefault()
    if (!comment.trim()) return
    await reviews.addComment(id, comment)
    setComment('')
    load()
  }

  const handleStatusChange = async () => {
    if (!newStatus) return
    setLoading(true)
    await reviews.changeStatus(id, newStatus, statusNote).catch(() => {})
    setNewStatus(''); setStatusNote('')
    setLoading(false)
    load()
  }

  if (!review) return <div style={{ color: '#64748b', padding: 40, textAlign: 'center' }}>Cargando...</div>

  return (
    <div style={{ maxWidth: 900, margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: 24 }}>
        <button onClick={() => navigate('/reviews')} style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontSize: 13, marginBottom: 16 }}>
          <ArrowLeft size={16} /> Volver a revisiones
        </button>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 16 }}>
          <div style={{ flex: 1 }}>
            <h1 style={{ fontSize: 22, fontWeight: 700, color: '#e2e8f0' }}>{review.title}</h1>
            {review.description && <p style={{ color: '#94a3b8', fontSize: 14, marginTop: 6 }}>{review.description}</p>}
          </div>
          <span style={{ padding: '6px 16px', borderRadius: 20, fontSize: 13, fontWeight: 700, background: `${statusColor[review.status]}22`, color: statusColor[review.status], whiteSpace: 'nowrap' }}>
            {statusLabel[review.status]}
          </span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 20 }}>
        {/* Left */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {/* Comments */}
          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, overflow: 'hidden' }}>
            <div style={{ padding: '14px 18px', borderBottom: '1px solid #334155', fontWeight: 600, color: '#e2e8f0', fontSize: 14 }}>
              Comentarios ({review.comments.length})
            </div>
            <div style={{ padding: 18, display: 'flex', flexDirection: 'column', gap: 14, minHeight: 120 }}>
              {review.comments.length === 0 && (
                <p style={{ color: '#475569', fontSize: 13, textAlign: 'center' }}>Sin comentarios aún</p>
              )}
              {review.comments.map(c => (
                <div key={c.id} style={{ display: 'flex', gap: 10 }}>
                  <div style={{ width: 32, height: 32, borderRadius: '50%', background: '#312e81', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    <User size={15} color="#818cf8" />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', gap: 8, alignItems: 'baseline', marginBottom: 4 }}>
                      <span style={{ fontSize: 13, fontWeight: 600, color: '#e2e8f0' }}>{c.editor?.name || 'Editor'}</span>
                      <span style={{ fontSize: 11, color: '#475569' }}>{new Date(c.created_at).toLocaleString('es')}</span>
                    </div>
                    <div style={{ fontSize: 13, color: '#94a3b8', lineHeight: 1.5 }}>{c.comment}</div>
                  </div>
                </div>
              ))}
            </div>
            <form onSubmit={handleComment} style={{ padding: '0 18px 18px', display: 'flex', gap: 8 }}>
              <input
                value={comment} onChange={e => setComment(e.target.value)}
                placeholder="Agregar comentario..."
                style={{ flex: 1, padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 13, outline: 'none' }}
              />
              <button type="submit" style={{ padding: '9px 14px', background: '#6366f1', border: 'none', borderRadius: 8, color: 'white', cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
                <Send size={15} />
              </button>
            </form>
          </div>

          {/* History */}
          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, overflow: 'hidden' }}>
            <div style={{ padding: '14px 18px', borderBottom: '1px solid #334155', fontWeight: 600, color: '#e2e8f0', fontSize: 14 }}>
              Historial
            </div>
            <div style={{ padding: 18, display: 'flex', flexDirection: 'column', gap: 10 }}>
              {review.history.map(h => (
                <div key={h.id} style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: statusColor[h.new_status], marginTop: 5, flexShrink: 0 }} />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 12, color: '#94a3b8' }}>
                      <span style={{ color: statusColor[h.new_status], fontWeight: 600 }}>{statusLabel[h.new_status]}</span>
                      {h.old_status && <> ← {statusLabel[h.old_status]}</>}
                      {' · '}{h.changed_by_editor?.name}
                    </div>
                    {h.note && <div style={{ fontSize: 12, color: '#64748b', marginTop: 2 }}>{h.note}</div>}
                    <div style={{ fontSize: 11, color: '#475569', marginTop: 2 }}>{new Date(h.changed_at).toLocaleString('es')}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {/* Info card */}
          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, padding: 18 }}>
            <h3 style={{ fontSize: 13, fontWeight: 600, color: '#64748b', marginBottom: 14, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Detalles</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <div>
                <div style={{ fontSize: 11, color: '#475569', marginBottom: 3 }}>Creado por</div>
                <div style={{ fontSize: 13, color: '#e2e8f0' }}>{review.created_by_editor?.name || '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: 11, color: '#475569', marginBottom: 3 }}>Asignado a</div>
                <div style={{ fontSize: 13, color: '#e2e8f0' }}>{review.assigned_editor?.name || 'Sin asignar'}</div>
              </div>
              <div>
                <div style={{ fontSize: 11, color: '#475569', marginBottom: 3 }}>Prioridad</div>
                <div style={{ fontSize: 13, color: '#e2e8f0', textTransform: 'capitalize' }}>{review.priority}</div>
              </div>
              <div>
                <div style={{ fontSize: 11, color: '#475569', marginBottom: 3 }}>Fecha límite</div>
                <div style={{ fontSize: 13, color: review.deadline && new Date(review.deadline) < new Date() ? '#ef4444' : '#e2e8f0' }}>
                  {review.deadline ? new Date(review.deadline).toLocaleString('es') : 'Sin fecha'}
                </div>
              </div>
              {review.content_url && (
                <div>
                  <div style={{ fontSize: 11, color: '#475569', marginBottom: 3 }}>Contenido</div>
                  <a href={review.content_url} target="_blank" rel="noreferrer" style={{ fontSize: 13, color: '#6366f1', wordBreak: 'break-all' }}>Ver enlace</a>
                </div>
              )}
            </div>
          </div>

          {/* Status change */}
          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, padding: 18 }}>
            <h3 style={{ fontSize: 13, fontWeight: 600, color: '#64748b', marginBottom: 14, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Cambiar estado</h3>
            <select value={newStatus} onChange={e => setNewStatus(e.target.value)}
              style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 13, marginBottom: 10 }}>
              <option value="">Seleccionar estado...</option>
              {statusOptions.filter(s => s !== review.status).map(s => (
                <option key={s} value={s}>{statusLabel[s]}</option>
              ))}
            </select>
            <textarea value={statusNote} onChange={e => setStatusNote(e.target.value)}
              placeholder="Nota (opcional)..." rows={2}
              style={{ width: '100%', padding: '9px 12px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#e2e8f0', fontSize: 13, outline: 'none', resize: 'none', marginBottom: 10, boxSizing: 'border-box' }} />
            <button onClick={handleStatusChange} disabled={!newStatus || loading}
              style={{ width: '100%', padding: '9px', background: newStatus ? '#6366f1' : '#334155', border: 'none', borderRadius: 8, color: newStatus ? 'white' : '#64748b', cursor: newStatus ? 'pointer' : 'not-allowed', fontSize: 13, fontWeight: 600 }}>
              {loading ? 'Actualizando...' : 'Actualizar estado'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
