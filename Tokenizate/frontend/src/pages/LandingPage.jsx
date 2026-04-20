import React from 'react'
import { useNavigate } from 'react-router-dom'
import { BookOpen, Users, Star, ArrowRight, CheckCircle2 } from 'lucide-react'
import { useAuth } from '../App.jsx'

export default function LandingPage() {
  const navigate = useNavigate()
  const { token } = useAuth()
  const goApp = () => navigate(token ? '/dashboard' : '/login')

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)', color: '#fff' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '24px 48px', borderBottom: '1px solid #334155' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <BookOpen size={32} color="#818cf8" />
          <h1 style={{ fontSize: 24, margin: 0 }}>Tokenizate</h1>
        </div>
        <button
          onClick={goApp}
          style={{ background: '#6366f1', color: '#fff', border: 0, padding: '10px 24px', borderRadius: 8, cursor: 'pointer', fontWeight: 600 }}
        >
          Iniciar sesión
        </button>
      </header>

      <section style={{ padding: '80px 48px', textAlign: 'center', maxWidth: 900, margin: '0 auto' }}>
        <h2 style={{ fontSize: 56, margin: 0, lineHeight: 1.1, background: 'linear-gradient(90deg,#818cf8,#c084fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Plataforma editorial inteligente
        </h2>
        <p style={{ fontSize: 20, color: '#cbd5e1', marginTop: 24 }}>
          Gestión de reseñas, editores y planes de contenido con IA. Tokeniza tu flujo editorial.
        </p>
        <div style={{ marginTop: 40, display: 'flex', gap: 16, justifyContent: 'center' }}>
          <button
            onClick={goApp}
            style={{ background: '#6366f1', color: '#fff', border: 0, padding: '14px 32px', borderRadius: 8, cursor: 'pointer', fontWeight: 600, fontSize: 16, display: 'flex', alignItems: 'center', gap: 8 }}
          >
            Empezar <ArrowRight size={18} />
          </button>
        </div>
      </section>

      <section style={{ padding: '40px 48px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(260px,1fr))', gap: 24, maxWidth: 1200, margin: '0 auto' }}>
        {[
          { icon: <Users size={28} color="#818cf8" />, title: 'Editores', text: 'Administra equipo editorial y roles.' },
          { icon: <Star size={28} color="#818cf8" />, title: 'Reseñas', text: 'Pipeline completo de reseñas con estados.' },
          { icon: <CheckCircle2 size={28} color="#818cf8" />, title: 'Planes', text: 'Planes de publicación y seguimiento.' },
        ].map((f, i) => (
          <div key={i} style={{ background: '#1e293b', padding: 28, borderRadius: 12, border: '1px solid #334155' }}>
            {f.icon}
            <h3 style={{ marginTop: 16, marginBottom: 8 }}>{f.title}</h3>
            <p style={{ color: '#94a3b8', margin: 0 }}>{f.text}</p>
          </div>
        ))}
      </section>

      <footer style={{ textAlign: 'center', padding: '40px 24px', color: '#64748b', borderTop: '1px solid #334155', marginTop: 80 }}>
        Tokenizate · CometaX Microservices
      </footer>
    </div>
  )
}
