import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../App.jsx'
import { auth } from '../api/api.js'
import { BookOpen, Loader } from 'lucide-react'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('admin@editorial.com')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const { data } = await auth.login(email, password)
      login(data.access_token, data.editor)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)',
    }}>
      <div style={{
        background: '#1e293b', padding: 40, borderRadius: 16, width: '100%', maxWidth: 420,
        border: '1px solid #334155', boxShadow: '0 25px 50px rgba(0,0,0,0.5)',
      }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: 56, height: 56, borderRadius: 14, background: '#312e81', marginBottom: 16 }}>
            <BookOpen size={28} color="#818cf8" />
          </div>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: '#e2e8f0' }}>Editorial Manager</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>Gestión de editores y revisiones</p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div>
            <label style={{ display: 'block', fontSize: 13, color: '#94a3b8', marginBottom: 6 }}>Email</label>
            <input
              type="email" value={email} onChange={(e) => setEmail(e.target.value)} required
              style={{
                width: '100%', padding: '10px 14px', background: '#0f172a', border: '1px solid #334155',
                borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', boxSizing: 'border-box',
              }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 13, color: '#94a3b8', marginBottom: 6 }}>Contraseña</label>
            <input
              type="password" value={password} onChange={(e) => setPassword(e.target.value)} required
              style={{
                width: '100%', padding: '10px 14px', background: '#0f172a', border: '1px solid #334155',
                borderRadius: 8, color: '#e2e8f0', fontSize: 14, outline: 'none', boxSizing: 'border-box',
              }}
            />
          </div>

          {error && (
            <div style={{ background: '#450a0a', border: '1px solid #991b1b', borderRadius: 8, padding: '10px 14px', fontSize: 13, color: '#fca5a5' }}>
              {error}
            </div>
          )}

          <button
            type="submit" disabled={loading}
            style={{
              width: '100%', padding: '12px', background: loading ? '#4338ca' : '#6366f1',
              border: 'none', borderRadius: 8, color: 'white', fontSize: 14, fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
              transition: 'background 0.15s',
            }}
          >
            {loading ? <><Loader size={16} style={{ animation: 'spin 1s linear infinite' }} /> Iniciando...</> : 'Iniciar sesión'}
          </button>
        </form>

        <p style={{ textAlign: 'center', fontSize: 12, color: '#475569', marginTop: 24 }}>
          Editorial Manager © 2024
        </p>
      </div>
    </div>
  )
}
