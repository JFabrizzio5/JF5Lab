import React, { useEffect, useState } from 'react'
import { billing } from '../api/api.js'
import { Check, Zap, Star, Building } from 'lucide-react'

const planIcon = { free: Zap, starter: Star, pro: Star, enterprise: Building }
const planColor = { free: '#64748b', starter: '#3b82f6', pro: '#6366f1', enterprise: '#f59e0b' }

const planFeatures = {
  free: ['1 editor', '10 revisiones/mes', 'API básica', 'Soporte email'],
  starter: ['5 editores', '100 revisiones/mes', 'Historial completo', 'Prioridad en soporte'],
  pro: ['20 editores', '500 revisiones/mes', 'Estadísticas avanzadas', 'Integraciones', 'Soporte prioritario'],
  enterprise: ['Editores ilimitados', 'Revisiones ilimitadas', 'SLA garantizado', 'Soporte dedicado', 'Onboarding personalizado'],
}

function fmt(cents) {
  return cents === 0 ? 'Gratis' : `$${(cents / 100).toFixed(0)}/mes`
}

export default function PlansPage() {
  const [plans, setPlans] = useState([])
  const [billing_cycle, setBillingCycle] = useState('monthly')
  const [currentSub, setCurrentSub] = useState(null)
  const [loadingPlan, setLoadingPlan] = useState(null)

  useEffect(() => {
    billing.plans().then(r => setPlans(r.data)).catch(() => {})
    billing.mySubscription().then(r => setCurrentSub(r.data)).catch(() => {})
  }, [])

  const handleSubscribe = async (plan) => {
    if (plan.price_monthly === 0) return
    setLoadingPlan(plan.id)
    try {
      const { data } = await billing.checkout({
        plan_id: plan.id,
        billing: billing_cycle,
        success_url: `${window.location.origin}/?subscribed=true`,
        cancel_url: `${window.location.origin}/plans`,
      })
      window.location.href = data.checkout_url
    } catch (err) {
      const msg = err.response?.data?.detail || 'Error'
      if (msg.includes('not configured')) {
        alert('Stripe no configurado aún. Agrega STRIPE_SECRET_KEY en el .env del backend.')
      } else {
        alert(msg)
      }
    } finally {
      setLoadingPlan(null)
    }
  }

  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: 40 }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, color: '#e2e8f0' }}>Planes y precios</h1>
        <p style={{ color: '#64748b', marginTop: 8, fontSize: 15 }}>Elige el plan que mejor se adapta a tu equipo</p>

        {currentSub && (
          <div style={{ display: 'inline-block', marginTop: 16, padding: '8px 20px', background: '#052e16', border: '1px solid #166534', borderRadius: 20, fontSize: 13, color: '#4ade80' }}>
            Plan actual: <strong>{currentSub.plan?.display_name}</strong>
          </div>
        )}

        {/* Billing toggle */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 12, marginTop: 24 }}>
          <button onClick={() => setBillingCycle('monthly')} style={{
            padding: '7px 20px', borderRadius: 20, border: 'none', cursor: 'pointer',
            background: billing_cycle === 'monthly' ? '#6366f1' : '#334155',
            color: billing_cycle === 'monthly' ? 'white' : '#94a3b8', fontSize: 13, fontWeight: 600,
          }}>Mensual</button>
          <button onClick={() => setBillingCycle('yearly')} style={{
            padding: '7px 20px', borderRadius: 20, border: 'none', cursor: 'pointer',
            background: billing_cycle === 'yearly' ? '#6366f1' : '#334155',
            color: billing_cycle === 'yearly' ? 'white' : '#94a3b8', fontSize: 13, fontWeight: 600,
          }}>Anual <span style={{ fontSize: 11, color: '#22c55e' }}>-20%</span></button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 20, maxWidth: 1000, margin: '0 auto' }}>
        {plans.map(plan => {
          const Icon = planIcon[plan.name] || Star
          const color = planColor[plan.name] || '#6366f1'
          const isCurrentPlan = currentSub?.plan?.name === plan.name
          const price = billing_cycle === 'yearly' ? plan.price_yearly / 12 : plan.price_monthly
          const features = planFeatures[plan.name] || []

          return (
            <div key={plan.id} style={{
              background: '#1e293b', border: `1px solid ${isCurrentPlan ? color : '#334155'}`,
              borderRadius: 16, padding: 24, display: 'flex', flexDirection: 'column', gap: 16,
              position: 'relative', overflow: 'hidden',
            }}>
              {plan.name === 'pro' && (
                <div style={{ position: 'absolute', top: 14, right: 14, background: '#6366f1', color: 'white', fontSize: 10, fontWeight: 700, padding: '3px 8px', borderRadius: 20 }}>POPULAR</div>
              )}

              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <div style={{ width: 40, height: 40, borderRadius: 10, background: `${color}22`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon size={20} color={color} />
                </div>
                <div>
                  <div style={{ fontWeight: 700, color: '#e2e8f0', fontSize: 15 }}>{plan.display_name}</div>
                  <div style={{ fontSize: 12, color: '#64748b' }}>
                    {plan.max_editors === -1 ? 'Ilimitado' : `${plan.max_editors} editor${plan.max_editors > 1 ? 'es' : ''}`}
                  </div>
                </div>
              </div>

              <div>
                <span style={{ fontSize: 30, fontWeight: 700, color: '#e2e8f0' }}>{price === 0 ? 'Gratis' : `$${(price / 100).toFixed(0)}`}</span>
                {price > 0 && <span style={{ fontSize: 13, color: '#64748b' }}>/mes</span>}
                {billing_cycle === 'yearly' && price > 0 && (
                  <div style={{ fontSize: 11, color: '#22c55e', marginTop: 2 }}>Facturado anualmente</div>
                )}
              </div>

              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 8 }}>
                {features.map(f => (
                  <div key={f} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Check size={14} color="#22c55e" />
                    <span style={{ fontSize: 13, color: '#94a3b8' }}>{f}</span>
                  </div>
                ))}
              </div>

              <button
                onClick={() => handleSubscribe(plan)}
                disabled={isCurrentPlan || plan.price_monthly === 0 || loadingPlan === plan.id}
                style={{
                  width: '100%', padding: '11px', border: 'none', borderRadius: 8,
                  background: isCurrentPlan ? '#334155' : plan.price_monthly === 0 ? '#1e293b' : color,
                  border: plan.price_monthly === 0 && !isCurrentPlan ? `1px solid ${color}` : 'none',
                  color: isCurrentPlan ? '#64748b' : plan.price_monthly === 0 ? color : 'white',
                  cursor: isCurrentPlan || plan.price_monthly === 0 ? 'default' : 'pointer',
                  fontSize: 14, fontWeight: 600,
                }}
              >
                {isCurrentPlan ? 'Plan actual' : plan.price_monthly === 0 ? 'Gratis' : loadingPlan === plan.id ? 'Redirigiendo...' : 'Suscribirse'}
              </button>
            </div>
          )
        })}
      </div>

      <div style={{ textAlign: 'center', marginTop: 40, padding: 20, background: '#1e293b', borderRadius: 12, maxWidth: 600, margin: '40px auto 0' }}>
        <p style={{ color: '#64748b', fontSize: 13 }}>
          Para activar pagos reales, configura <code style={{ color: '#818cf8', background: '#0f172a', padding: '2px 6px', borderRadius: 4 }}>STRIPE_SECRET_KEY</code> y <code style={{ color: '#818cf8', background: '#0f172a', padding: '2px 6px', borderRadius: 4 }}>STRIPE_WEBHOOK_SECRET</code> en el archivo <code style={{ color: '#818cf8', background: '#0f172a', padding: '2px 6px', borderRadius: 4 }}>.env</code> del backend.
        </p>
      </div>
    </div>
  )
}
