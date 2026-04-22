// Plantilla shape:
// { id, name, category, w, h, bg, layers: [{ type, ...props }] }
// type: 'text' | 'shape' | 'icon' | 'logo' | 'gradient-blob' | 'comet-trail'
// Coordenadas en porcentaje (0-100) para responsive a cualquier tamaño.

export const PRESETS = {
  cosmic: {
    name: 'Cosmic',
    bg: 'radial-gradient(ellipse at top, #1e1b4b 0%, #0a0e1a 70%)',
    accent: '#6366f1',
    accent2: '#a855f7',
    text: '#e2e8f0',
    muted: '#94a3b8'
  },
  light: {
    name: 'Light',
    bg: 'linear-gradient(135deg, #f8fafc, #e2e8f0)',
    accent: '#6366f1',
    accent2: '#a855f7',
    text: '#0f172a',
    muted: '#64748b'
  },
  sunset: {
    name: 'Sunset',
    bg: 'linear-gradient(135deg, #ec4899, #f59e0b)',
    accent: '#fff',
    accent2: '#fef3c7',
    text: '#fff',
    muted: 'rgba(255,255,255,0.85)'
  },
  midnight: {
    name: 'Midnight',
    bg: 'linear-gradient(180deg, #020617, #1e293b)',
    accent: '#22d3ee',
    accent2: '#a78bfa',
    text: '#f1f5f9',
    muted: '#94a3b8'
  },
  forest: {
    name: 'Forest',
    bg: 'linear-gradient(135deg, #064e3b, #14532d)',
    accent: '#34d399',
    accent2: '#a3e635',
    text: '#ecfdf5',
    muted: '#a7f3d0'
  }
}

export const SIZES = {
  post: { name: 'Post 4:5', w: 1080, h: 1350 },
  square: { name: 'Square 1:1', w: 1080, h: 1080 },
  story: { name: 'Story 9:16', w: 1080, h: 1920 }
}

export const TEMPLATES = [
  {
    id: 'cosmic-quote',
    name: 'Cosmic Quote',
    category: 'quote',
    layers: [
      { type: 'comet-trail', x: 70, y: 18, size: 60, opacity: 0.8 },
      { type: 'text', x: 50, y: 50, w: 80, align: 'center', font: 'serif', size: 64, weight: 700, color: 'text', text: 'Las mejores ideas\nempiezan como una chispa' },
      { type: 'text', x: 50, y: 75, w: 70, align: 'center', size: 22, weight: 500, color: 'muted', text: '— @cometax' },
      { type: 'logo', x: 50, y: 92, size: 40, align: 'center' }
    ]
  },
  {
    id: 'feature-list',
    name: 'Feature List',
    category: 'list',
    layers: [
      { type: 'text', x: 8, y: 12, size: 56, weight: 800, color: 'accent', text: '5 Razones' },
      { type: 'text', x: 8, y: 22, size: 32, weight: 500, color: 'text', text: 'Por las que CometaX gana' },
      { type: 'icon-list', x: 8, y: 38, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
        { icon: 'mdi-rocket-launch', text: 'Setup en 60 segundos' },
        { icon: 'mdi-shield-check', text: 'Multi-tenant con RLS' },
        { icon: 'mdi-chart-line', text: 'Métricas en tiempo real' },
        { icon: 'mdi-cash-multiple', text: 'Stripe MX + Conekta' },
        { icon: 'mdi-cube-outline', text: 'Docker out-of-the-box' }
      ] },
      { type: 'logo', x: 92, y: 92, size: 40, align: 'right' }
    ]
  },
  {
    id: 'stat-card',
    name: 'Stat Card',
    category: 'stat',
    layers: [
      { type: 'gradient-blob', x: 80, y: 20, size: 50, opacity: 0.4 },
      { type: 'text', x: 50, y: 32, align: 'center', size: 26, weight: 600, color: 'muted', text: 'TENANTS ACTIVOS' },
      { type: 'text', x: 50, y: 48, align: 'center', size: 180, weight: 900, color: 'accent', text: '12,400' },
      { type: 'text', x: 50, y: 65, align: 'center', size: 28, weight: 500, color: 'text', text: '+34% este mes' },
      { type: 'logo', x: 50, y: 90, size: 40, align: 'center' }
    ]
  },
  {
    id: 'code-snippet',
    name: 'Code Snippet',
    category: 'code',
    layers: [
      { type: 'text', x: 8, y: 10, size: 36, weight: 700, color: 'text', text: 'Crea un microservicio' },
      { type: 'text', x: 8, y: 17, size: 22, weight: 500, color: 'muted', text: 'Un solo comando, listo para producción' },
      { type: 'code-block', x: 8, y: 30, w: 84, h: 38, font: 'mono', size: 28, code: '$ cometax new\n\n? Nombre: MiSaaS\n? Stack: FastAPI\n? IAM: sí\n\n✓ Generado en 12s' },
      { type: 'text', x: 50, y: 80, align: 'center', size: 22, weight: 500, color: 'muted', text: 'cometax.dev' },
      { type: 'logo', x: 92, y: 92, size: 40, align: 'right' }
    ]
  },
  {
    id: 'before-after',
    name: 'Before / After',
    category: 'compare',
    layers: [
      { type: 'text', x: 50, y: 8, align: 'center', size: 38, weight: 800, color: 'text', text: 'Antes vs Después' },
      { type: 'split', x: 50, y: 50, w: 100, h: 70, leftLabel: 'ANTES', rightLabel: 'DESPUÉS', leftItems: ['3 días config', 'Pagos rotos', 'Sin IAM'], rightItems: ['12 segundos', 'Stripe + OXXO', 'JWT RS256'] },
      { type: 'logo', x: 50, y: 92, size: 40, align: 'center' }
    ]
  },
  {
    id: 'testimonial',
    name: 'Testimonial',
    category: 'social',
    layers: [
      { type: 'text', x: 50, y: 12, align: 'center', size: 100, weight: 700, color: 'accent', text: '"' },
      { type: 'text', x: 50, y: 38, w: 84, align: 'center', size: 38, weight: 500, color: 'text', text: 'Pasé de 3 semanas a 1 día para lanzar mi MVP. CometaX me ahorró meses.' },
      { type: 'avatar', x: 50, y: 70, size: 90, align: 'center' },
      { type: 'text', x: 50, y: 80, align: 'center', size: 26, weight: 700, color: 'text', text: 'María R.' },
      { type: 'text', x: 50, y: 85, align: 'center', size: 20, weight: 500, color: 'muted', text: 'Founder · Dev tools MX' }
    ]
  },
  {
    id: 'product-launch',
    name: 'Product Launch',
    category: 'launch',
    layers: [
      { type: 'badge', x: 8, y: 10, text: 'NUEVO', color: 'accent' },
      { type: 'text', x: 8, y: 28, size: 110, weight: 900, color: 'text', text: 'StockLink' },
      { type: 'text', x: 8, y: 42, w: 80, size: 32, weight: 500, color: 'muted', text: 'Inventario multi-tenant para tienditas, restaurantes y más.' },
      { type: 'gradient-blob', x: 75, y: 75, size: 60, opacity: 0.6 },
      { type: 'text', x: 8, y: 80, size: 24, weight: 600, color: 'accent', text: 'stocklink.mx' },
      { type: 'logo', x: 92, y: 92, size: 40, align: 'right' }
    ]
  },
  {
    id: 'tip-tutorial',
    name: 'Tip / Tutorial',
    category: 'tutorial',
    layers: [
      { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'muted', text: 'PASO 02 / 05' },
      { type: 'progress-dots', x: 8, y: 14, count: 5, active: 1 },
      { type: 'text', x: 8, y: 28, size: 56, weight: 800, color: 'text', text: 'Conecta\nStripe MX' },
      { type: 'text', x: 8, y: 50, w: 84, size: 28, weight: 500, color: 'muted', text: 'Activa OXXO + SPEI con un solo webhook. El módulo billing está incluido en ApiIam.' },
      { type: 'icon', x: 50, y: 75, size: 120, align: 'center', icon: 'mdi-credit-card-outline', color: 'accent' },
      { type: 'logo', x: 92, y: 92, size: 40, align: 'right' }
    ]
  },
  {
    id: 'meme-format',
    name: 'Meme Format',
    category: 'meme',
    layers: [
      { type: 'text', x: 50, y: 12, align: 'center', size: 56, weight: 800, color: 'text', text: 'CUANDO TU MVP\nLEVANTA EN 60s' },
      { type: 'icon', x: 50, y: 50, size: 280, align: 'center', icon: 'mdi-emoticon-cool-outline', color: 'accent' },
      { type: 'text', x: 50, y: 88, align: 'center', size: 56, weight: 800, color: 'text', text: '😎 cometax' }
    ]
  },
  {
    id: 'cta-final',
    name: 'CTA Final',
    category: 'cta',
    layers: [
      { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
      { type: 'text', x: 50, y: 32, align: 'center', size: 60, weight: 900, color: 'text', text: '¿Te gustó?' },
      { type: 'text', x: 50, y: 45, w: 80, align: 'center', size: 30, weight: 500, color: 'muted', text: 'Sigue @cometax para más tips de microservicios MX' },
      { type: 'icon', x: 50, y: 65, size: 90, align: 'center', icon: 'mdi-heart', color: 'accent2' },
      { type: 'icon', x: 38, y: 65, size: 70, align: 'center', icon: 'mdi-comment-outline', color: 'accent' },
      { type: 'icon', x: 62, y: 65, size: 70, align: 'center', icon: 'mdi-share-variant', color: 'accent' },
      { type: 'text', x: 50, y: 88, align: 'center', size: 30, weight: 700, color: 'accent', text: '@cometax' }
    ]
  }
]

export function findTemplate(id) {
  return TEMPLATES.find(t => t.id === id)
}
