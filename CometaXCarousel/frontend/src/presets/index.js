// ════════════════════════════════════════════════════════════════════════════
// CometaX Carousel — Designer-grade preset library
// ════════════════════════════════════════════════════════════════════════════
//
// Cada preset:
//   { id, name, description, thumbColor, presetKey, sizeKey, slides[] }
// Cada slide:
//   { templateId, layers: [...] }
//
// Reglas de diseño aplicadas a TODOS los presets:
//   1. Layouts asimétricos: hero text left-aligned + decoración derecha
//   2. Contraste tipográfico: 80-120 hero / 24-30 body / 18-22 eyebrow
//   3. Mínimo 2-3 capas decorativas por slide (waves, blobs, sparkles, etc.)
//   4. Hero slides usan photo-bg con tag-pill
//   5. Stats con big-number 280-360
//   6. Testimoniales con avatar + foto blur
//   7. CTA con glossy-ball / iso-card
//   8. Cada último slide tiene logo CometaX visible (o brand del producto)
//   9. lineHeight 1.05-1.15 en hero text
//  10. Solo MDI icons, sin emojis
// ════════════════════════════════════════════════════════════════════════════

export const CAROUSEL_PRESETS = [
  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 1 · Product Launch
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'product-launch',
    name: 'Lanzamiento de producto',
    description: 'Anuncia un producto nuevo en 6 slides. Hero + razones + precio + CTA.',
    thumbColor: '#6366f1',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      // Slide 1 · HERO con photo-bg
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,minimal', seed: 11, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 28, opacity: 0.18 },
          { type: 'tag-pill', x: 8, y: 11, text: 'Recién lanzado · v1.0' },
          { type: 'sparkle', x: 86, y: 16, size: 48, color: 'accent2' },
          { type: 'text', x: 8, y: 38, w: 84, size: 110, weight: 900, color: 'text', lineHeight: 1.05, text: 'Llegó\nNombreApp.' },
          { type: 'shine-line', y: 60, opacity: 0.7 },
          { type: 'text', x: 8, y: 70, w: 78, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'La forma más rápida de hacer X sin complicarte la vida.' },
          { type: 'text', x: 8, y: 90, size: 20, weight: 800, color: 'accent', text: 'DESLIZA PARA VER MÁS →' }
        ]
      },
      // Slide 2 · Problema
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'gradient-blob', x: 78, y: 28, size: 60, opacity: 0.55 },
          { type: 'comet-trail', x: 80, y: 22, size: 40, opacity: 0.6 },
          { type: 'tag-pill', x: 8, y: 12, text: 'El problema' },
          { type: 'text', x: 8, y: 42, w: 84, size: 80, weight: 900, color: 'text', lineHeight: 1.08, text: 'Hacer X tomaba\nhoras de trabajo\nmanual.' },
          { type: 'shine-line', y: 75, opacity: 0.6 },
          { type: 'text', x: 8, y: 82, w: 78, size: 26, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Y nadie tenía tiempo para eso. Mucho menos paciencia.' }
        ]
      },
      // Slide 3 · Razones (asimétrico con iso-cube)
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 135, opacity: 0.25 },
          { type: 'iso-cube', x: 82, y: 25, size: 180 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Por qué funciona' },
          { type: 'text', x: 8, y: 26, size: 72, weight: 900, color: 'accent', lineHeight: 1.05, text: '3 razones.' },
          { type: 'icon-list', x: 8, y: 56, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-rocket-launch', text: 'Setup en 60 segundos' },
            { icon: 'mdi-shield-check', text: 'Sin cuenta requerida' },
            { icon: 'mdi-currency-usd', text: 'Free tier generoso' }
          ] },
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right', brand: 'cometax' }
        ]
      },
      // Slide 4 · Stat
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'abstract,gradient', seed: 22, overlayAngle: 135, overlayOpacity: 0.85 },
          { type: 'grid-pattern', gap: 50, opacity: 0.1 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Tiempo ahorrado' },
          { type: 'big-number', x: 50, y: 48, align: 'center', size: 320, text: '8h' },
          { type: 'text', x: 50, y: 72, align: 'center', size: 28, weight: 500, color: 'muted', text: 'cada semana, en promedio' },
          { type: 'sparkle', x: 80, y: 32, size: 36, color: 'accent2' },
          { type: 'sparkle', x: 18, y: 70, size: 28, color: 'accent' }
        ]
      },
      // Slide 5 · Precio
      {
        templateId: 'product-launch',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 90, opacity: 0.45 },
          { type: 'glossy-ball', x: 80, y: 25, size: 140 },
          { type: 'tag-pill', x: 50, y: 12, align: 'center', text: 'Precio' },
          { type: 'text', x: 50, y: 32, align: 'center', size: 30, weight: 700, color: 'muted', text: 'Empieza por' },
          { type: 'big-number', x: 50, y: 52, align: 'center', size: 280, text: '$0' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 26, weight: 500, color: 'accent', text: 'Plan Pro desde $199 MXN/mes' }
        ]
      },
      // Slide 6 · CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 33, overlayAngle: 0, overlayOpacity: 0.62 },
          { type: 'glossy-ball', x: 50, y: 35, size: 200 },
          { type: 'sparkle', x: 22, y: 28, size: 36, color: 'accent2' },
          { type: 'sparkle', x: 78, y: 70, size: 30, color: 'accent' },
          { type: 'text', x: 50, y: 60, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Pruébalo hoy.' },
          { type: 'text', x: 50, y: 76, w: 78, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Link en bio. Sin tarjeta para empezar.' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 2 · Discount Promo
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'discount-promo',
    name: 'Promo descuento',
    description: 'Oferta con porcentaje de descuento, urgencia y CTA. 5 slides.',
    thumbColor: '#ec4899',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      // Slide 1 · HERO con big number -40%
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract,sunset', seed: 41, overlayAngle: 135, overlayOpacity: 0.55 },
          { type: 'diagonal-band', y: 18, h: 8, angle: -6, text: 'Oferta limitada' },
          { type: 'sparkle', x: 80, y: 30, size: 50, color: 'accent2' },
          { type: 'sparkle', x: 18, y: 70, size: 36, color: 'accent' },
          { type: 'big-number', x: 50, y: 52, align: 'center', size: 360, text: '-40%' },
          { type: 'shine-line', y: 76, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, w: 80, align: 'center', size: 36, weight: 700, color: 'text', text: 'Solo este fin de semana' },
          { type: 'text', x: 50, y: 92, align: 'center', size: 22, weight: 800, color: 'accent', text: 'DESLIZA PARA VER DETALLES →' }
        ]
      },
      // Slide 2 · Qué incluye
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-cube', x: 82, y: 26, size: 180 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Incluido' },
          { type: 'text', x: 8, y: 26, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Qué te llevas.' },
          { type: 'icon-list', x: 8, y: 52, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-check-circle', text: 'Acceso completo a la plataforma' },
            { icon: 'mdi-check-circle', text: 'Soporte prioritario 24/7' },
            { icon: 'mdi-check-circle', text: 'Actualizaciones gratuitas de por vida' },
            { icon: 'mdi-check-circle', text: 'Sin permanencia ni letra chica' }
          ] }
        ]
      },
      // Slide 3 · Compara antes/después
      {
        templateId: 'before-after',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 50, opacity: 0.5 },
          { type: 'tag-pill', x: 50, y: 10, align: 'center', text: 'Compara' },
          { type: 'text', x: 50, y: 20, align: 'center', size: 56, weight: 900, color: 'text', text: 'Normal vs Promo' },
          { type: 'split', x: 50, y: 60, w: 100, h: 70, leftLabel: 'NORMAL', rightLabel: 'CON DESCUENTO', leftItems: ['$1,500 MXN/mes', 'Pago anual', 'Mismo producto'], rightItems: ['$899 MXN/mes', 'Mismas features', 'Ahorras $7,200/año'] }
        ]
      },
      // Slide 4 · Urgencia
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'abstract,gradient', seed: 42, overlayAngle: 135, overlayOpacity: 0.82 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Termina en' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 340, text: '48h' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 28, weight: 600, color: 'text', text: 'No esperes al último día' }
        ]
      },
      // Slide 5 · CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 90, opacity: 0.55 },
          { type: 'glossy-ball', x: 50, y: 32, size: 200 },
          { type: 'sparkle', x: 18, y: 25, size: 32, color: 'accent2' },
          { type: 'sparkle', x: 82, y: 75, size: 36, color: 'accent' },
          { type: 'text', x: 50, y: 58, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Aprovecha\nya.' },
          { type: 'shine-line', y: 78, opacity: 0.6 },
          { type: 'text', x: 50, y: 84, w: 80, align: 'center', size: 24, weight: 600, color: 'muted', text: 'Código: PROMO40 al checkout' },
          { type: 'logo', x: 50, y: 94, size: 38, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 3 · 5 Tips Rápidos
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'tips-5',
    name: '5 tips rápidos',
    description: 'Cover + 5 tips numerados + CTA follow. Educativo, alta retención.',
    thumbColor: '#22d3ee',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      // Slide 1 · Cover
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,minimal', seed: 51, overlayAngle: 180, overlayOpacity: 0.8 },
          { type: 'dots-pattern', gap: 30, opacity: 0.16 },
          { type: 'comet-trail', x: 80, y: 22, size: 50, opacity: 0.5 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Guarda este post' },
          { type: 'text', x: 8, y: 42, w: 86, size: 92, weight: 900, color: 'text', lineHeight: 1.05, text: '5 tips para\nlanzar tu MVP\nen un fin de semana.' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 91, size: 22, weight: 800, color: 'accent', text: 'DESLIZA →' }
        ]
      },
      // Tips 1-5 con consistent design
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Tip 01 / 05' },
          { type: 'progress-dots', x: 8, y: 16, count: 5, active: 0 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Define\nuna sola feature.' },
          { type: 'shine-line', y: 62, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Si no puedes describirla en una frase, todavía no tienes MVP. Tienes ambición.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-target', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 18, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Tip 02 / 05' },
          { type: 'progress-dots', x: 8, y: 16, count: 5, active: 1 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Usa stack\nque ya conoces.' },
          { type: 'shine-line', y: 62, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'No es momento de aprender Rust. Es momento de validar tu idea.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-toolbox-outline', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Tip 03 / 05' },
          { type: 'progress-dots', x: 8, y: 16, count: 5, active: 2 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Cobra\ndesde el día 1.' },
          { type: 'shine-line', y: 62, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: '"Free hasta validar" suena lindo. Pero un usuario que paga $1 te enseña más que 100 gratis.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-cash', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 18, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Tip 04 / 05' },
          { type: 'progress-dots', x: 8, y: 16, count: 5, active: 3 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Hospéda\nen 1 servicio.' },
          { type: 'shine-line', y: 62, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Vercel, Railway, Render. Lo que sea. Pero no armes Kubernetes para 3 usuarios.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-cloud-upload', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Tip 05 / 05' },
          { type: 'progress-dots', x: 8, y: 16, count: 5, active: 4 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Lanza\nantes de pulir.' },
          { type: 'shine-line', y: 62, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Si te da pena lo que lanzaste, lanzaste a tiempo. Si no, ya esperaste de más.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-rocket-launch', color: 'accent' }
        ]
      },
      // Slide 7 · CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 52, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 50, y: 35, size: 180 },
          { type: 'sparkle', x: 22, y: 22, size: 32, color: 'accent2' },
          { type: 'sparkle', x: 78, y: 78, size: 36, color: 'accent' },
          { type: 'text', x: 50, y: 60, align: 'center', size: 72, weight: 900, color: 'text', lineHeight: 1.05, text: '¿Te sirvió?' },
          { type: 'text', x: 50, y: 75, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Sigue para más tips de producto y MVPs' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 4 · Before / After Case
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'before-after-case',
    name: 'Antes vs Después (caso éxito)',
    description: 'Hook + situación inicial + cambio + resultado en métrica.',
    thumbColor: '#10b981',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      // Slide 1 · Hook
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'portrait,woman,professional', seed: 61, overlayAngle: 0, overlayOpacity: 0.7, overlayGrad: 'linear-gradient(0deg, #064e3b 0%, transparent 60%)' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Caso real · 2026' },
          { type: 'text', x: 8, y: 50, w: 86, size: 78, weight: 900, color: 'text', lineHeight: 1.05, text: 'Cómo María\npasó de cero ventas\na $50k/mes.' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'EN 90 DÍAS · SIN ADS PAGADOS →' }
        ]
      },
      // Slide 2 · El cambio
      {
        templateId: 'before-after',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'tag-pill', x: 50, y: 8, align: 'center', text: 'El cambio' },
          { type: 'text', x: 50, y: 18, align: 'center', size: 56, weight: 900, color: 'text', text: 'Antes vs Después' },
          { type: 'split', x: 50, y: 58, w: 100, h: 70, leftLabel: 'ANTES', rightLabel: 'DESPUÉS', leftItems: ['Posts random', 'Sin sistema', '0 leads/semana'], rightItems: ['Carruseles diarios', 'Calendario editorial', '40+ leads/semana'] }
        ]
      },
      // Slide 3 · Qué hizo
      {
        templateId: 'feature-list',
        layers: [
          { type: 'gradient-blob', x: 18, y: 25, size: 50, opacity: 0.4 },
          { type: 'iso-cube', x: 82, y: 25, size: 160 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Qué hizo' },
          { type: 'text', x: 8, y: 26, size: 64, weight: 900, color: 'accent', lineHeight: 1.05, text: '3 cambios\nclave.' },
          { type: 'icon-list', x: 8, y: 56, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Definió 1 sola buyer persona' },
            { icon: 'mdi-numeric-2-circle', text: 'Usó plantillas (no diseñó cada post)' },
            { icon: 'mdi-numeric-3-circle', text: 'Publicó 5 días/semana sin falta' }
          ] }
        ]
      },
      // Slide 4 · Stat resultado
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'mountain,sunset', seed: 62, overlayAngle: 135, overlayOpacity: 0.82 },
          { type: 'glossy-ball', x: 82, y: 22, size: 120 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Resultado' },
          { type: 'big-number', x: 50, y: 48, align: 'center', size: 280, text: '+1247%' },
          { type: 'shine-line', y: 72, opacity: 0.7 },
          { type: 'text', x: 50, y: 80, w: 78, align: 'center', size: 26, weight: 500, color: 'muted', text: 'crecimiento de revenue en 90 días' }
        ]
      },
      // Slide 5 · CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 90, opacity: 0.55 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-link-variant' },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 48, w: 80, size: 72, weight: 900, color: 'text', lineHeight: 1.05, text: '¿Quieres\nlo mismo?' },
          { type: 'shine-line', y: 76, opacity: 0.6 },
          { type: 'text', x: 8, y: 82, w: 78, size: 24, weight: 500, color: 'muted', text: 'Te dejo la guía completa en el link de la bio. Es gratis.' },
          { type: 'logo', x: 92, y: 92, size: 38, align: 'right', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 5 · Feature Announce
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'feature-announce',
    name: 'Feature nueva',
    description: 'Anuncia un feature nuevo. Badge, qué hace, cómo usarlo, CTA.',
    thumbColor: '#818cf8',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      // Slide 1 · Hero just shipped
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,office', seed: 71, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'grid-pattern', gap: 50, opacity: 0.12 },
          { type: 'tag-pill', x: 8, y: 11, text: 'Just shipped · v2.0' },
          { type: 'sparkle', x: 86, y: 18, size: 50, color: 'accent2' },
          { type: 'text', x: 8, y: 40, w: 86, size: 100, weight: 900, color: 'text', lineHeight: 1.05, text: 'Carrusel\nWizard 2.0' },
          { type: 'shine-line', y: 65, opacity: 0.7 },
          { type: 'text', x: 8, y: 73, w: 80, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Genera 10 slides en menos de un minuto.' },
          { type: 'text', x: 8, y: 90, size: 22, weight: 800, color: 'accent', text: 'CONOCE QUÉ TRAE →' }
        ]
      },
      // Slide 2 · Qué trae
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 135, opacity: 0.22 },
          { type: 'glossy-ball', x: 82, y: 25, size: 130 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Qué trae' },
          { type: 'text', x: 8, y: 26, size: 64, weight: 900, color: 'accent', lineHeight: 1.05, text: '3 cosas\nnuevas.' },
          { type: 'icon-list', x: 8, y: 56, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-magic-staff', text: 'Generador AI desde un prompt' },
            { icon: 'mdi-content-duplicate', text: '12 carruseles pre-armados' },
            { icon: 'mdi-export', text: 'Export ZIP numerado para subir' }
          ] }
        ]
      },
      // Slide 3 · Cómo usarlo
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Cómo usarlo' },
          { type: 'text', x: 8, y: 26, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'En 3 clics.' },
          { type: 'shine-line', y: 50, opacity: 0.6 },
          { type: 'icon-list', x: 8, y: 62, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Abre el editor' },
            { icon: 'mdi-numeric-2-circle', text: 'Elige carrusel pre-armado' },
            { icon: 'mdi-numeric-3-circle', text: 'Cambia textos y exporta' }
          ] }
        ]
      },
      // Slide 4 · CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 72, overlayAngle: 0, overlayOpacity: 0.65 },
          { type: 'glossy-ball', x: 50, y: 32, size: 200 },
          { type: 'sparkle', x: 22, y: 22, size: 32, color: 'accent2' },
          { type: 'sparkle', x: 78, y: 78, size: 36, color: 'accent' },
          { type: 'text', x: 50, y: 58, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Pruébalo.' },
          { type: 'text', x: 50, y: 74, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Es gratis. Sin login. Tus diseños no salen del navegador.' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 6 · Tutorial 3 Steps
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'tutorial-3-steps',
    name: 'Mini tutorial 3 pasos',
    description: 'Cover + 3 pasos numerados + ya quedó. Educativo corto.',
    thumbColor: '#a78bfa',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      // Slide 1 · Cover
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop', seed: 81, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 30, opacity: 0.18 },
          { type: 'comet-trail', x: 80, y: 22, size: 50, opacity: 0.55 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Tutorial · CFDI 4.0' },
          { type: 'text', x: 8, y: 48, w: 86, size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Cómo facturar\nCFDI en 3 pasos.' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'DESLIZA →' }
        ]
      },
      // Pasos 1-3
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Paso 01 / 03' },
          { type: 'progress-dots', x: 8, y: 16, count: 3, active: 0 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Carga tu CSD\ndel SAT.' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 70, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Sube los archivos .cer y .key. Tu contraseña queda solo en tu navegador.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-file-key', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 18, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Paso 02 / 03' },
          { type: 'progress-dots', x: 8, y: 16, count: 3, active: 1 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Captura\nla operación.' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 70, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'RFC del cliente, productos, importes. El catálogo SAT autocompleta.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-pencil', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 8, text: 'Paso 03 / 03' },
          { type: 'progress-dots', x: 8, y: 16, count: 3, active: 2 },
          { type: 'text', x: 8, y: 34, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Timbra\ny envía.' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 70, w: 84, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Un solo click. Recibes XML + PDF. WhatsApp opcional al cliente.' },
          { type: 'icon', x: 82, y: 86, size: 90, align: 'center', icon: 'mdi-check-decagram', color: 'accent' }
        ]
      },
      // CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 82, overlayAngle: 0, overlayOpacity: 0.65 },
          { type: 'glossy-ball', x: 50, y: 32, size: 200 },
          { type: 'sparkle', x: 22, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 50, y: 60, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Ya quedó.' },
          { type: 'text', x: 50, y: 75, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Sigue para más tutoriales de SAT y CFDI' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 7 · Tools Recommendation
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'tools-recommendation',
    name: 'Recomendación de herramientas',
    description: '6 herramientas con descripción corta. Categoría dev/marketing/design.',
    thumbColor: '#34d399',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      // Cover
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,office', seed: 91, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 28, opacity: 0.18 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Guarda este post' },
          { type: 'text', x: 8, y: 42, w: 86, size: 78, weight: 900, color: 'text', lineHeight: 1.05, text: '6 herramientas\ngratis para devs\nque cambian el juego.' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 91, size: 22, weight: 800, color: 'accent', text: 'NINGUNA REQUIERE TARJETA →' }
        ]
      },
      // Tool 1 · Cursor
      {
        templateId: 'product-launch',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'iso-card', x: 80, y: 38, size: 220, icon: 'mdi-language-cpp' },
          { type: 'tag-pill', x: 8, y: 12, text: '01 · Editor con AI' },
          { type: 'text', x: 8, y: 30, size: 90, weight: 900, color: 'text', lineHeight: 1.05, text: 'Cursor.' },
          { type: 'text', x: 8, y: 46, w: 60, size: 28, weight: 700, color: 'accent', text: 'Editor con AI nativo' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 60, size: 24, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Reemplaza VS Code. Tab para autocompletar funciones enteras. Free para uso casual.' }
        ]
      },
      // Tool 2 · Vercel
      {
        templateId: 'product-launch',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'iso-card', x: 80, y: 38, size: 220, icon: 'mdi-triangle' },
          { type: 'tag-pill', x: 8, y: 12, text: '02 · Hosting' },
          { type: 'text', x: 8, y: 30, size: 90, weight: 900, color: 'text', lineHeight: 1.05, text: 'Vercel.' },
          { type: 'text', x: 8, y: 46, w: 60, size: 28, weight: 700, color: 'accent', text: 'Deploy en un git push' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 60, size: 24, weight: 500, color: 'muted', lineHeight: 1.3, text: 'SSL gratis, CDN global, build automático. Free tier brutal para proyectos personales.' }
        ]
      },
      // Tool 3 · Neon
      {
        templateId: 'product-launch',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'iso-card', x: 80, y: 38, size: 220, icon: 'mdi-database' },
          { type: 'tag-pill', x: 8, y: 12, text: '03 · Database' },
          { type: 'text', x: 8, y: 30, size: 90, weight: 900, color: 'text', lineHeight: 1.05, text: 'Neon.' },
          { type: 'text', x: 8, y: 46, w: 60, size: 28, weight: 700, color: 'accent', text: 'Postgres serverless' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 60, size: 24, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Branching de DB como git. Suspende cuando no la usas. Free hasta 0.5 GB.' }
        ]
      },
      // Tool 4 · Resend
      {
        templateId: 'product-launch',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'iso-card', x: 80, y: 38, size: 220, icon: 'mdi-email-fast' },
          { type: 'tag-pill', x: 8, y: 12, text: '04 · Email API' },
          { type: 'text', x: 8, y: 30, size: 90, weight: 900, color: 'text', lineHeight: 1.05, text: 'Resend.' },
          { type: 'text', x: 8, y: 46, w: 60, size: 28, weight: 700, color: 'accent', text: 'Email transaccional' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 60, size: 24, weight: 500, color: 'muted', lineHeight: 1.3, text: 'API limpia, React Email para templates. 3,000 emails/mes gratis.' }
        ]
      },
      // Tool 5 · Sentry
      {
        templateId: 'product-launch',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'iso-card', x: 80, y: 38, size: 220, icon: 'mdi-bug-outline' },
          { type: 'tag-pill', x: 8, y: 12, text: '05 · Monitoring' },
          { type: 'text', x: 8, y: 30, size: 90, weight: 900, color: 'text', lineHeight: 1.05, text: 'Sentry.' },
          { type: 'text', x: 8, y: 46, w: 60, size: 28, weight: 700, color: 'accent', text: 'Errores en tiempo real' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 60, size: 24, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Te enteras del bug antes que el usuario. Free 5k errores/mes.' }
        ]
      },
      // Tool 6 · Plausible
      {
        templateId: 'product-launch',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'iso-card', x: 80, y: 38, size: 220, icon: 'mdi-chart-line' },
          { type: 'tag-pill', x: 8, y: 12, text: '06 · Analytics' },
          { type: 'text', x: 8, y: 30, size: 90, weight: 900, color: 'text', lineHeight: 1.05, text: 'Plausible.' },
          { type: 'text', x: 8, y: 46, w: 60, size: 28, weight: 700, color: 'accent', text: 'Analytics sin cookies' },
          { type: 'shine-line', y: 60, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 60, size: 24, weight: 500, color: 'muted', lineHeight: 1.3, text: 'GDPR-friendly, dashboard simple. Self-host gratis u hosted desde $9/mes.' }
        ]
      },
      // CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 90, opacity: 0.5 },
          { type: 'glossy-ball', x: 50, y: 32, size: 180 },
          { type: 'sparkle', x: 22, y: 25, size: 32, color: 'accent2' },
          { type: 'text', x: 50, y: 58, align: 'center', size: 72, weight: 900, color: 'text', lineHeight: 1.05, text: '¿Cuál te falta?' },
          { type: 'text', x: 50, y: 76, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Comenta abajo. Si conoces otra que no esté, también.' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 8 · Webinar Event
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'webinar-event',
    name: 'Webinar / evento',
    description: 'Save the date + agenda + speakers + CTA registro.',
    thumbColor: '#f59e0b',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      // Save the date
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'office,workspace,team', seed: 101, overlayAngle: 180, overlayOpacity: 0.7 },
          { type: 'sparkle', x: 86, y: 22, size: 50, color: 'accent2' },
          { type: 'tag-pill', x: 50, y: 11, align: 'center', text: 'Webinar gratis · LIVE' },
          { type: 'text', x: 50, y: 38, w: 86, align: 'center', size: 78, weight: 900, color: 'text', lineHeight: 1.05, text: 'Cómo lanzar\nun SaaS MX.' },
          { type: 'shine-line', y: 64, opacity: 0.7 },
          { type: 'text', x: 50, y: 72, w: 80, align: 'center', size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Sin gastar más de $1,000 en infra.' },
          { type: 'big-number', x: 50, y: 88, align: 'center', size: 90, text: '15·05' },
          { type: 'text', x: 50, y: 95, align: 'center', size: 22, weight: 800, color: 'accent', text: '6:00 PM CDMX' }
        ]
      },
      // Agenda
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 135, opacity: 0.22 },
          { type: 'iso-cube', x: 82, y: 25, size: 170 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Agenda' },
          { type: 'text', x: 8, y: 26, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Lo que verás.' },
          { type: 'icon-list', x: 8, y: 56, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-clock-outline', text: '6:00 — Bienvenida' },
            { icon: 'mdi-rocket-launch', text: '6:10 — Demo en vivo' },
            { icon: 'mdi-cash-multiple', text: '6:35 — Stack y costos reales' },
            { icon: 'mdi-comment-question', text: '7:00 — Q&A abierto' }
          ] }
        ]
      },
      // Speaker
      {
        templateId: 'testimonial',
        layers: [
          { type: 'photo-bg', query: 'portrait,woman,professional', seed: 102, overlayAngle: 0, overlayOpacity: 0.6, overlayGrad: 'linear-gradient(0deg, #ec4899 0%, transparent 70%)' },
          { type: 'tag-pill', x: 50, y: 12, align: 'center', text: 'Tu invitada' },
          { type: 'avatar', x: 50, y: 35, size: 160, align: 'center', src: 'https://i.pravatar.cc/300?img=44' },
          { type: 'text', x: 50, y: 60, align: 'center', size: 48, weight: 900, color: 'text', text: 'María R.' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 22, weight: 700, color: 'accent', text: 'FOUNDER · 4 SAAS LANZADOS' },
          { type: 'shine-line', y: 76, opacity: 0.6 },
          { type: 'text', x: 50, y: 84, w: 84, align: 'center', size: 22, weight: 500, color: 'muted', lineHeight: 1.3, text: '"Te voy a enseñar lo que me hubiera ahorrado meses cuando empecé."' }
        ]
      },
      // CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 90, opacity: 0.55 },
          { type: 'glossy-ball', x: 50, y: 32, size: 200 },
          { type: 'sparkle', x: 22, y: 22, size: 30, color: 'accent2' },
          { type: 'sparkle', x: 78, y: 78, size: 36, color: 'accent' },
          { type: 'text', x: 50, y: 58, align: 'center', size: 72, weight: 900, color: 'text', lineHeight: 1.05, text: 'Aparta\ntu lugar.' },
          { type: 'text', x: 50, y: 78, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Cupo limitado. Recibirás recordatorio 1h antes.' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 9 · Job Opening
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'job-opening',
    name: 'Vacante / reclutamiento',
    description: 'Buscamos X. Perks. Requisitos. Cómo aplicar.',
    thumbColor: '#06b6d4',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      // Hero hiring
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'team,office,collaboration', seed: 111, overlayAngle: 180, overlayOpacity: 0.72 },
          { type: 'dots-pattern', gap: 28, opacity: 0.18 },
          { type: 'tag-pill', x: 8, y: 11, text: 'Estamos contratando' },
          { type: 'sparkle', x: 86, y: 18, size: 50, color: 'accent2' },
          { type: 'text', x: 8, y: 38, w: 86, size: 100, weight: 900, color: 'text', lineHeight: 1.05, text: 'Senior\nFull-stack.' },
          { type: 'shine-line', y: 65, opacity: 0.7 },
          { type: 'text', x: 8, y: 73, w: 80, size: 28, weight: 500, color: 'muted', lineHeight: 1.3, text: '100% remoto · LATAM · USD competitivo' },
          { type: 'text', x: 8, y: 91, size: 22, weight: 800, color: 'accent', text: 'DESLIZA PARA DETALLES →' }
        ]
      },
      // Perks
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.2 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-laptop' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Perks' },
          { type: 'text', x: 8, y: 26, size: 60, weight: 900, color: 'text', lineHeight: 1.05, text: 'Por qué\nunirte.' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-currency-usd', text: '$3,500 - $5,000 USD/mes' },
            { icon: 'mdi-home', text: '100% remoto, async' },
            { icon: 'mdi-beach', text: '30 días vacaciones pagadas' },
            { icon: 'mdi-laptop', text: 'Equipo + home office stipend' }
          ] }
        ]
      },
      // Requisitos
      {
        templateId: 'feature-list',
        layers: [
          { type: 'gradient-blob', x: 18, y: 25, size: 50, opacity: 0.4 },
          { type: 'iso-cube', x: 82, y: 28, size: 170 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Buscamos' },
          { type: 'text', x: 8, y: 26, size: 60, weight: 900, color: 'accent', lineHeight: 1.05, text: 'Si tienes...' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-check', text: '5+ años con TypeScript' },
            { icon: 'mdi-check', text: 'Postgres + ORM + RLS' },
            { icon: 'mdi-check', text: 'Has lanzado a producción' },
            { icon: 'mdi-check', text: 'Inglés conversacional' }
          ] }
        ]
      },
      // CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunrise,morning,light', seed: 112, overlayAngle: 0, overlayOpacity: 0.65 },
          { type: 'glossy-ball', x: 80, y: 28, size: 160 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 50, w: 80, size: 72, weight: 900, color: 'text', lineHeight: 1.05, text: 'Aplica\nantes del 30.' },
          { type: 'shine-line', y: 78, opacity: 0.6 },
          { type: 'text', x: 8, y: 84, w: 78, size: 22, weight: 500, color: 'muted', text: 'Manda CV + GitHub al link en bio. Respondemos a todos.' },
          { type: 'logo', x: 92, y: 92, size: 38, align: 'right', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 10 · Testimonial Case
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'testimonial-case',
    name: 'Testimonio cliente',
    description: 'Quote + foto/nombre + métrica resultado. 3 slides.',
    thumbColor: '#c084fc',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      // Testimonio principal
      {
        templateId: 'testimonial',
        layers: [
          { type: 'photo-bg', query: 'portrait,woman,professional', seed: 121, overlayAngle: 0, overlayOpacity: 0.65, overlayGrad: 'linear-gradient(0deg, #1e1b4b 0%, transparent 65%)' },
          { type: 'tag-pill', x: 50, y: 12, align: 'center', text: 'Testimonio · Cliente real' },
          { type: 'text', x: 50, y: 28, align: 'center', size: 140, weight: 900, color: 'accent', lineHeight: 0.8, text: '"' },
          { type: 'avatar', x: 50, y: 52, size: 140, align: 'center', src: 'https://i.pravatar.cc/300?img=47' },
          { type: 'text', x: 50, y: 75, w: 86, align: 'center', size: 32, weight: 500, color: 'text', lineHeight: 1.3, text: '"Pasé de 3 semanas a 1 día para lanzar mi MVP. CometaX me ahorró meses de trabajo."' },
          { type: 'text', x: 50, y: 90, align: 'center', size: 26, weight: 800, color: 'text', text: 'María R.' },
          { type: 'text', x: 50, y: 95, align: 'center', size: 18, weight: 600, color: 'accent', text: 'FOUNDER · DEV TOOLS MX' }
        ]
      },
      // Stat
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 122, overlayAngle: 135, overlayOpacity: 0.85 },
          { type: 'glossy-ball', x: 82, y: 25, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Tiempo ahorrado' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '21x' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, w: 78, align: 'center', size: 28, weight: 500, color: 'muted', text: 'más rápido que armarlo a mano' }
        ]
      },
      // CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 90, opacity: 0.55 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-rocket-launch' },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 52, w: 80, size: 72, weight: 900, color: 'text', lineHeight: 1.05, text: '¿Tu turno?' },
          { type: 'shine-line', y: 78, opacity: 0.6 },
          { type: 'text', x: 8, y: 84, w: 78, size: 24, weight: 500, color: 'muted', text: 'Empieza gratis. Sin tarjeta. Sin compromiso.' },
          { type: 'logo', x: 92, y: 92, size: 38, align: 'right', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 11 · Engagement Question
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'engagement-question',
    name: 'Pregunta / engagement',
    description: 'Pregunta provocadora + opciones + comenta abajo.',
    thumbColor: '#a3e635',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      // Pregunta provocadora
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,minimal', seed: 131, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 30, opacity: 0.18 },
          { type: 'sparkle', x: 86, y: 20, size: 48, color: 'accent2' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Pregunta seria' },
          { type: 'text', x: 8, y: 48, w: 86, size: 72, weight: 900, color: 'text', lineHeight: 1.08, text: '¿Lanzar feo\ny rápido,\no perfecto\ny tarde?' },
          { type: 'shine-line', y: 86, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'DESLIZA PARA VER LAS DOS POSTURAS →' }
        ]
      },
      // Las dos posturas
      {
        templateId: 'before-after',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'tag-pill', x: 50, y: 8, align: 'center', text: 'Las dos posturas' },
          { type: 'text', x: 50, y: 18, align: 'center', size: 56, weight: 900, color: 'text', text: '¿Tú con quién?' },
          { type: 'split', x: 50, y: 60, w: 100, h: 70, leftLabel: 'EQUIPO RÁPIDO', rightLabel: 'EQUIPO PULIDO', leftItems: ['Aprende del usuario', 'Itera con datos', 'Recauda más fácil'], rightItems: ['Mejor primera impresión', 'Marca cuidada', 'Menos refactor después'] }
        ]
      },
      // CTA comenta
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 132, overlayAngle: 0, overlayOpacity: 0.65 },
          { type: 'glossy-ball', x: 50, y: 32, size: 200 },
          { type: 'sparkle', x: 22, y: 22, size: 32, color: 'accent2' },
          { type: 'sparkle', x: 78, y: 78, size: 36, color: 'accent' },
          { type: 'text', x: 50, y: 58, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: '¿Tú qué\nharías?' },
          { type: 'text', x: 50, y: 78, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Comenta abajo. Bonus si das ejemplo real.' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // PRESET 12 · Restaurant Promo
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'restaurant-promo',
    name: 'Restaurante / Food promo',
    description: 'Plato del día, precio, horario, ubicación. 4 slides.',
    thumbColor: '#fb923c',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      // Hero plato
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'food,product', seed: 141, overlayAngle: 180, overlayOpacity: 0.6 },
          { type: 'sparkle', x: 86, y: 22, size: 48, color: 'accent2' },
          { type: 'tag-pill', x: 50, y: 11, align: 'center', text: 'Hoy en el menú' },
          { type: 'text', x: 50, y: 46, w: 84, align: 'center', size: 100, weight: 900, color: 'text', lineHeight: 1.0, text: 'Tacos\nde birria.' },
          { type: 'shine-line', y: 70, opacity: 0.7 },
          { type: 'text', x: 50, y: 78, align: 'center', size: 28, weight: 500, color: 'muted', text: 'Receta de la abuela. 8h cocción.' },
          { type: 'icon', x: 50, y: 92, size: 60, align: 'center', icon: 'mdi-food', color: 'accent' }
        ]
      },
      // Precio
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 142, overlayAngle: 135, overlayOpacity: 0.82 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Orden de 4 piezas' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 340, text: '$89' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Incluye consomé y guacamole' }
        ]
      },
      // Info contacto
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-silverware-fork-knife' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Visítanos' },
          { type: 'text', x: 8, y: 26, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Te esperamos.' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 8, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-clock-outline', text: 'Lun-Sáb · 12 PM - 9 PM' },
            { icon: 'mdi-map-marker', text: 'Av. Insurgentes 123, CDMX' },
            { icon: 'mdi-phone', text: '55 1234 5678 (pedidos)' }
          ] }
        ]
      },
      // CTA
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 143, overlayAngle: 0, overlayOpacity: 0.62 },
          { type: 'glossy-ball', x: 50, y: 32, size: 200 },
          { type: 'sparkle', x: 22, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 50, y: 60, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Pídelos\nya.' },
          { type: 'shine-line', y: 80, opacity: 0.6 },
          { type: 'text', x: 50, y: 86, w: 80, align: 'center', size: 22, weight: 500, color: 'muted', text: 'Rappi · Didi · Uber Eats — o ven directo.' },
          { type: 'logo', x: 50, y: 94, size: 38, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  }
]

// ════════════════════════════════════════════════════════════════════════════
// CometaX SaaS — un carrusel premium por producto
// ════════════════════════════════════════════════════════════════════════════

CAROUSEL_PRESETS.push(
  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · StockLink
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-stocklink',
    name: 'StockLink — pitch',
    description: 'Inventario multi-tenant MX para tiendita, restaurante, paquetería, constructora. 5 slides.',
    thumbColor: '#6366f1',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      // Hero problema
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'product,workspace', seed: 201, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'grid-pattern', gap: 50, opacity: 0.12 },
          { type: 'tag-pill', x: 8, y: 11, text: 'StockLink · SaaS MX' },
          { type: 'sparkle', x: 86, y: 18, size: 48, color: 'accent2' },
          { type: 'text', x: 8, y: 40, w: 86, size: 88, weight: 900, color: 'text', lineHeight: 1.05, text: 'Tu inventario\nse te escapa\nde las manos.' },
          { type: 'shine-line', y: 72, opacity: 0.7 },
          { type: 'text', x: 8, y: 80, w: 80, size: 26, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Excel ya no aguanta. Y los sistemas grandes cuestan $5,000/mes.' },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'HAY ALGO MEJOR →' }
        ]
      },
      // Comparativa
      {
        templateId: 'before-after',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'tag-pill', x: 50, y: 8, align: 'center', text: 'Comparativa real' },
          { type: 'text', x: 50, y: 18, align: 'center', size: 56, weight: 900, color: 'text', text: 'StockLink vs Excel' },
          { type: 'split', x: 50, y: 60, w: 100, h: 70, leftLabel: 'EXCEL', rightLabel: 'STOCKLINK', leftItems: ['Sin alertas', 'No multi-sucursal', 'No QR/barcode', 'Pierdes stock'], rightItems: ['Alertas auto', 'Multi-tenant + RLS', 'QR + NFC + barcode', 'Movimientos atómicos'] }
        ]
      },
      // Para quién
      {
        templateId: 'feature-list',
        layers: [
          { type: 'gradient-blob', x: 18, y: 25, size: 50, opacity: 0.4 },
          { type: 'iso-cube', x: 82, y: 28, size: 180 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Para quién' },
          { type: 'text', x: 8, y: 26, size: 60, weight: 900, color: 'accent', lineHeight: 1.05, text: 'Una app,\n4 industrias.' },
          { type: 'icon-list', x: 8, y: 60, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-store', text: 'Tiendita / Abarrotes' },
            { icon: 'mdi-silverware-fork-knife', text: 'Restaurante (descuento auto)' },
            { icon: 'mdi-truck-delivery', text: 'Paquetería / Bodega' },
            { icon: 'mdi-hammer-wrench', text: 'Construcción / Taller' }
          ] }
        ]
      },
      // Precio
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 202, overlayAngle: 135, overlayOpacity: 0.84 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Plan Starter' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '$499' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 26, weight: 500, color: 'muted', text: 'MXN/mes · Hasta 1,000 SKUs' }
        ]
      },
      // CTA con logo StockLink
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop', seed: 203, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 25, size: 32, color: 'accent2' },
          { type: 'text', x: 8, y: 42, w: 80, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Demo gratis,\ndatos reales.' },
          { type: 'shine-line', y: 70, opacity: 0.6 },
          { type: 'text', x: 8, y: 78, w: 78, size: 22, weight: 500, color: 'muted', text: 'Carga tu industria, vemos cómo se ve con tus SKUs.' },
          { type: 'text', x: 8, y: 86, size: 26, weight: 800, color: 'accent', text: 'stocklink.mx →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'stocklink' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · NotaMX
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-notamx',
    name: 'NotaMX — pitch',
    description: 'POS + notas de venta + WhatsApp + CFDI 4.0 para freelancers y PYME MX. 5 slides.',
    thumbColor: '#10b981',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      // Hero
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,office', seed: 211, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 30, opacity: 0.18 },
          { type: 'tag-pill', x: 8, y: 12, text: 'NotaMX · CFDI 4.0' },
          { type: 'sparkle', x: 86, y: 20, size: 48, color: 'accent2' },
          { type: 'text', x: 8, y: 46, w: 86, size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: '¿Cobras\npor WhatsApp\ny olvidas\nla factura?' },
          { type: 'shine-line', y: 86, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'HAY SOLUCIÓN →' }
        ]
      },
      // Todo en uno
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-receipt-text' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Todo en uno' },
          { type: 'text', x: 8, y: 26, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Cobra y\nfactura aquí.' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-whatsapp', text: 'Link de pago por WhatsApp' },
            { icon: 'mdi-credit-card', text: 'Stripe + Conekta · OXXO/SPEI' },
            { icon: 'mdi-receipt-text', text: 'CFDI 4.0 timbrado auto' },
            { icon: 'mdi-file-pdf-box', text: 'PDF + XML al cliente' }
          ] }
        ]
      },
      // Cómo en 30s
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Cómo' },
          { type: 'text', x: 8, y: 26, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'En 30 segundos.' },
          { type: 'shine-line', y: 50, opacity: 0.6 },
          { type: 'icon-list', x: 8, y: 62, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Capturas el monto y cliente' },
            { icon: 'mdi-numeric-2-circle', text: 'Mandas link por WhatsApp' },
            { icon: 'mdi-numeric-3-circle', text: 'Cliente paga, factura sale sola' }
          ] }
        ]
      },
      // Precio
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 212, overlayAngle: 135, overlayOpacity: 0.85 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Empieza en' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 360, text: '$0' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: '5 facturas/mes gratis. Después $1.50 c/u.' }
        ]
      },
      // CTA con logo NotaMX
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 213, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 42, w: 80, size: 60, weight: 900, color: 'text', lineHeight: 1.05, text: 'Sin contador.\nSin sistema caro.' },
          { type: 'shine-line', y: 72, opacity: 0.6 },
          { type: 'text', x: 8, y: 80, w: 78, size: 22, weight: 500, color: 'muted', text: 'Para freelancers, talleres, consultorios y PYMEs MX.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'notamx.com →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'notamx' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · PorCobrar
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-porcobrar',
    name: 'PorCobrar — pitch',
    description: 'Cobranza automática + scoring deudores + dunning. Para CFOs y contadores MX. 5 slides.',
    thumbColor: '#f59e0b',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      // Hero
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'office,workspace', seed: 221, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 30, opacity: 0.16 },
          { type: 'tag-pill', x: 8, y: 12, text: 'PorCobrar · Cobranza IA' },
          { type: 'sparkle', x: 86, y: 22, size: 48, color: 'accent2' },
          { type: 'text', x: 8, y: 46, w: 86, size: 70, weight: 900, color: 'text', lineHeight: 1.08, text: '¿Tu cartera\nvencida ya pasa\nlos $200,000?' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'HAY FORMA DE COBRARLA →' }
        ]
      },
      // Comparativa
      {
        templateId: 'before-after',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'tag-pill', x: 50, y: 8, align: 'center', text: 'El cambio' },
          { type: 'text', x: 50, y: 18, align: 'center', size: 56, weight: 900, color: 'text', text: 'Antes vs PorCobrar' },
          { type: 'split', x: 50, y: 60, w: 100, h: 70, leftLabel: 'AHORA', rightLabel: 'CON PORCOBRAR', leftItems: ['Persigues por WA', 'Excel de vencimientos', 'Olvidas seguimientos', '0 score deudor'], rightItems: ['Dunning auto 1/3/7/15d', 'Subes CFDI XML', 'Recordatorios programados', 'Score IA por deudor'] }
        ]
      },
      // 4 pasos
      {
        templateId: 'feature-list',
        layers: [
          { type: 'gradient-blob', x: 18, y: 25, size: 50, opacity: 0.4 },
          { type: 'iso-cube', x: 82, y: 28, size: 170 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Cómo funciona' },
          { type: 'text', x: 8, y: 26, size: 60, weight: 900, color: 'accent', lineHeight: 1.05, text: '4 pasos.' },
          { type: 'icon-list', x: 8, y: 56, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Subes tus CFDI XML (parser auto)' },
            { icon: 'mdi-numeric-2-circle', text: 'Eliges flow de cobranza' },
            { icon: 'mdi-numeric-3-circle', text: 'Mandamos WA/email + link Stripe' },
            { icon: 'mdi-numeric-4-circle', text: 'Cobras. Score se actualiza solo' }
          ] }
        ]
      },
      // Stat
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 222, overlayAngle: 135, overlayOpacity: 0.84 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Recuperas en promedio' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '67%' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'de tu cartera vencida en 30 días' }
        ]
      },
      // CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 223, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 42, w: 80, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Para CFOs\ny contadores MX.' },
          { type: 'shine-line', y: 74, opacity: 0.6 },
          { type: 'text', x: 8, y: 80, w: 78, size: 22, weight: 500, color: 'muted', text: 'Demo con tus XMLs. Si no recuperamos, no pagas.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'porcobrar.mx →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'porcobrar' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · PulsoMX
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-pulsomx',
    name: 'PulsoMX — pitch',
    description: 'Software para gym, yoga, coworking, dojos. Sin pagar Mindbody. 5 slides.',
    thumbColor: '#ec4899',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      // Hero
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'workspace,team', seed: 231, overlayAngle: 180, overlayOpacity: 0.75 },
          { type: 'dots-pattern', gap: 28, opacity: 0.18 },
          { type: 'tag-pill', x: 8, y: 11, text: 'PulsoMX · Fitness SaaS' },
          { type: 'sparkle', x: 86, y: 18, size: 48, color: 'accent2' },
          { type: 'text', x: 8, y: 38, w: 86, size: 78, weight: 900, color: 'text', lineHeight: 1.05, text: 'Mindbody\ncuesta\n$3,500/mes.' },
          { type: 'shine-line', y: 70, opacity: 0.7 },
          { type: 'text', x: 8, y: 80, w: 80, size: 28, weight: 700, color: 'accent', text: 'PulsoMX no.' },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'muted', text: 'PARA GYMS · YOGA · COWORKINGS · DOJOS' }
        ]
      },
      // Incluye
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-dumbbell' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Incluye' },
          { type: 'text', x: 8, y: 26, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Todo lo\nque necesitas.' },
          { type: 'icon-list', x: 8, y: 56, w: 60, gap: 6, size: 22, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-account-group', text: 'Membresías recurrentes' },
            { icon: 'mdi-calendar-clock', text: 'Reservas + cupos' },
            { icon: 'mdi-qrcode-scan', text: 'Check-in QR en puerta' },
            { icon: 'mdi-credit-card', text: 'Stripe + Conekta' },
            { icon: 'mdi-chart-line', text: 'Dashboard MRR + churn' }
          ] }
        ]
      },
      // Stat ahorro
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 232, overlayAngle: 135, overlayOpacity: 0.84 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Ahorro anual vs Mindbody' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 280, text: '$36k' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 26, weight: 500, color: 'muted', text: 'MXN/año en software' }
        ]
      },
      // Setup
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'gradient-blob', x: 82, y: 28, size: 50, opacity: 0.45 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Setup' },
          { type: 'text', x: 8, y: 26, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Listo en 1 día.' },
          { type: 'shine-line', y: 50, opacity: 0.6 },
          { type: 'icon-list', x: 8, y: 62, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Cargas tus clases y horarios' },
            { icon: 'mdi-numeric-2-circle', text: 'Cargas planes (mensual, paquete 10)' },
            { icon: 'mdi-numeric-3-circle', text: 'Compartes link a tus alumnos' }
          ] }
        ]
      },
      // CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 233, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 42, w: 80, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Demo gratis\n14 días.' },
          { type: 'shine-line', y: 72, opacity: 0.6 },
          { type: 'text', x: 8, y: 80, w: 78, size: 22, weight: 500, color: 'muted', text: 'Sin tarjeta. Migración asistida si vienes de Mindbody.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'pulsomx.com →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'pulsomx' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · AgendaPro
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-agendapro',
    name: 'AgendaPro — pitch',
    description: 'Reservas con pago anticipado para barberos, dentistas, vets, coaches. 5 slides.',
    thumbColor: '#1e40af',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      // Hero
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop', seed: 241, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 28, opacity: 0.18 },
          { type: 'comet-trail', x: 80, y: 22, size: 50, opacity: 0.5 },
          { type: 'tag-pill', x: 8, y: 12, text: 'AgendaPro · Reservas' },
          { type: 'text', x: 8, y: 46, w: 86, size: 70, weight: 900, color: 'text', lineHeight: 1.08, text: '40% de tus citas\nno llegan.\nY no avisan.' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'SOLUCIÓN: PAGO ANTICIPADO →' }
        ]
      },
      // Cómo
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-calendar-check' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Cómo funciona' },
          { type: 'text', x: 8, y: 26, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Paga, asiste,\nya está.' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-calendar-check', text: 'Cliente reserva en tu link' },
            { icon: 'mdi-credit-card', text: 'Paga el 100% o un anticipo' },
            { icon: 'mdi-whatsapp', text: 'Recordatorio WA 24h y 1h' },
            { icon: 'mdi-star-outline', text: 'Pide review en Google al final' }
          ] }
        ]
      },
      // Para quién
      {
        templateId: 'feature-list',
        layers: [
          { type: 'gradient-blob', x: 18, y: 25, size: 50, opacity: 0.4 },
          { type: 'iso-cube', x: 82, y: 28, size: 170 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Para quién' },
          { type: 'text', x: 8, y: 26, size: 60, weight: 900, color: 'accent', lineHeight: 1.05, text: 'Tu chamba\nes con cita.' },
          { type: 'icon-list', x: 8, y: 58, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-content-cut', text: 'Barbería / estética' },
            { icon: 'mdi-tooth', text: 'Dentista / médico' },
            { icon: 'mdi-paw', text: 'Veterinaria' },
            { icon: 'mdi-meditation', text: 'Coach / terapeuta' }
          ] }
        ]
      },
      // Stat
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 242, overlayAngle: 135, overlayOpacity: 0.85 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Baja no-shows' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '-87%' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 26, weight: 500, color: 'muted', text: 'cuando cobras anticipo' }
        ]
      },
      // CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'office,workspace', seed: 243, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 38, w: 80, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Tu agenda,\ncon dinero\nadelantado.' },
          { type: 'shine-line', y: 76, opacity: 0.6 },
          { type: 'text', x: 8, y: 82, w: 78, size: 22, weight: 500, color: 'muted', text: 'AgendaPro. Reservas que sí pagan.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'agendapro.mx →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'agendapro' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · RentaFacil
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-rentafacil',
    name: 'RentaFacil — pitch',
    description: 'Admin inmobiliario para arrendadores: contratos, pagos, inquilinos. 4 slides.',
    thumbColor: '#84cc16',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      // Hero
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,office', seed: 251, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 28, opacity: 0.18 },
          { type: 'tag-pill', x: 8, y: 12, text: 'RentaFacil · Inmobiliario' },
          { type: 'sparkle', x: 86, y: 22, size: 48, color: 'accent2' },
          { type: 'text', x: 8, y: 46, w: 86, size: 78, weight: 900, color: 'text', lineHeight: 1.05, text: 'Tienes 5 deptos.\nY un Excel\nque ya odias.' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'HAY VIDA DESPUÉS DE EXCEL →' }
        ]
      },
      // Incluye
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-home-city' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Incluye' },
          { type: 'text', x: 8, y: 26, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Renta sin\npelearte.' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-home-city', text: 'Multi-propiedad sin límite' },
            { icon: 'mdi-file-document-edit', text: 'Contratos PDF/DOCX al instante' },
            { icon: 'mdi-cash-multiple', text: 'Recordatorio + recibo CFDI' },
            { icon: 'mdi-account-multiple', text: 'Histórico de inquilinos' }
          ] }
        ]
      },
      // Stat
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 252, overlayAngle: 135, overlayOpacity: 0.85 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Ahorras' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '12h' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'al mes en cobranza y papeleo' }
        ]
      },
      // CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 253, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 42, w: 80, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: '$199 / mes\npor 5 deptos.' },
          { type: 'shine-line', y: 74, opacity: 0.6 },
          { type: 'text', x: 8, y: 80, w: 78, size: 22, weight: 500, color: 'muted', text: 'Sin permanencia. Cancela cuando quieras.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'rentafacil.mx →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'rentafacil' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · RanKiT
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-rankit',
    name: 'RanKiT — pitch',
    description: 'Tracker de visibilidad SEO. Pega tu dominio y ve dónde apareces. 4 slides.',
    thumbColor: '#22d3ee',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      // Hero
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop', seed: 261, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'grid-pattern', gap: 50, opacity: 0.12 },
          { type: 'comet-trail', x: 80, y: 22, size: 50, opacity: 0.6 },
          { type: 'tag-pill', x: 8, y: 12, text: 'RanKiT · SEO Tracker' },
          { type: 'text', x: 8, y: 46, w: 86, size: 70, weight: 900, color: 'text', lineHeight: 1.08, text: '¿En qué keywords\napareces realmente\nen Google?' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'LO SABRÁS EN 30 SEG →' }
        ]
      },
      // Te da
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-magnify' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Te da' },
          { type: 'text', x: 8, y: 26, size: 60, weight: 900, color: 'text', lineHeight: 1.05, text: 'Score SEO\nreal.' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-google', text: 'Posiciones de tus keywords' },
            { icon: 'mdi-trending-up', text: 'Cambios diarios + alertas' },
            { icon: 'mdi-eye', text: 'Quién te roba tráfico' },
            { icon: 'mdi-file-export', text: 'Reportes PDF para el cliente' }
          ] }
        ]
      },
      // Stat
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 262, overlayAngle: 135, overlayOpacity: 0.85 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Vs Semrush' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '1/10' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'del precio. Mismas métricas core.' }
        ]
      },
      // CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop', seed: 263, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 42, w: 80, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Pega\ntu dominio.' },
          { type: 'shine-line', y: 74, opacity: 0.6 },
          { type: 'text', x: 8, y: 80, w: 78, size: 22, weight: 500, color: 'muted', text: '5 keywords gratis. Sin cuenta. Sin tarjeta.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'rankit.mx →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'rankit' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // CometaX · ConsultorIA
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'cometax-consultoria',
    name: 'ConsultorIA — pitch',
    description: 'Consultor IA: pídele estrategia de negocio MX y te responde con plan accionable. 4 slides.',
    thumbColor: '#a855f7',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      // Hero
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,office', seed: 271, overlayAngle: 180, overlayOpacity: 0.78 },
          { type: 'dots-pattern', gap: 28, opacity: 0.18 },
          { type: 'comet-trail', x: 78, y: 22, size: 60, opacity: 0.7 },
          { type: 'tag-pill', x: 8, y: 12, text: 'ConsultorIA · Negocios MX' },
          { type: 'text', x: 8, y: 46, w: 86, size: 70, weight: 900, color: 'text', lineHeight: 1.08, text: 'Un consultor de\nnegocios IA\nentrenado en MX.' },
          { type: 'shine-line', y: 84, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'DISPONIBLE 24/7 →' }
        ]
      },
      // Te resuelve
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'iso-card', x: 80, y: 28, size: 200, icon: 'mdi-robot-happy' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Te resuelve' },
          { type: 'text', x: 8, y: 26, size: 50, weight: 900, color: 'text', lineHeight: 1.05, text: 'Lo que un consultor\ncobra en $50k.' },
          { type: 'icon-list', x: 8, y: 58, w: 60, gap: 7, size: 22, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-bullseye-arrow', text: 'Define nicho y buyer persona' },
            { icon: 'mdi-chart-bar', text: 'Sugiere precios MX por benchmark' },
            { icon: 'mdi-rocket-launch', text: 'Plan 90 días con KPIs' },
            { icon: 'mdi-file-tree', text: 'Estructura legal/fiscal MX' }
          ] }
        ]
      },
      // Stat
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 272, overlayAngle: 135, overlayOpacity: 0.85 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Vs consultor humano' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '99%' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'más barato. Mismo framework.' }
        ]
      },
      // CTA con logo
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,gradient', seed: 273, overlayAngle: 0, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 80, y: 28, size: 170 },
          { type: 'sparkle', x: 18, y: 22, size: 30, color: 'accent2' },
          { type: 'text', x: 8, y: 42, w: 80, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Pregúntale\nahora.' },
          { type: 'shine-line', y: 74, opacity: 0.6 },
          { type: 'text', x: 8, y: 80, w: 78, size: 22, weight: 500, color: 'muted', text: '3 sesiones gratis. Después $99/mes ilimitado.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'consultor.cometax.mx →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'consultoria' }
        ]
      }
    ]
  }
)

// ════════════════════════════════════════════════════════════════════════════
// Showcase visual — pulido marginal sobre la versión existente
// ════════════════════════════════════════════════════════════════════════════

CAROUSEL_PRESETS.push(
  // ══════════════════════════════════════════════════════════════════════════
  // Showcase · Olas + brand
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'showcase-waves',
    name: 'Showcase · Olas + brand',
    description: 'Estilo cinematográfico con ondas inferiores degradadas, dots-pattern y logo CometaX real.',
    thumbColor: '#a855f7',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'dots-pattern', gap: 32, opacity: 0.15 },
          { type: 'gradient-overlay', angle: 180, opacityStart: 0.4 },
          { type: 'sparkle', x: 80, y: 18, size: 50, color: 'accent2' },
          { type: 'sparkle', x: 18, y: 75, size: 30, color: 'accent' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Para creadores' },
          { type: 'text', x: 8, y: 40, w: 86, size: 90, weight: 900, color: 'text', lineHeight: 1.05, text: 'Diseña posts\nque parecen\nde agencia.' },
          { type: 'shine-line', y: 70, opacity: 0.7 },
          { type: 'text', x: 8, y: 78, w: 80, size: 26, weight: 500, color: 'muted', text: 'Sin Photoshop. Sin Canva Pro. Sin login.' },
          { type: 'wave-bottom', h: 28, opacity: 0.7 },
          { type: 'logo', x: 8, y: 92, size: 44, brand: 'cometax', text: 'CometaX' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 135, opacity: 0.3 },
          { type: 'shine-line', y: 25, opacity: 0.6 },
          { type: 'iso-cube', x: 82, y: 28, size: 170 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Incluye' },
          { type: 'text', x: 8, y: 28, size: 60, weight: 900, color: 'text', lineHeight: 1.05, text: 'Estilos\nde verdad.' },
          { type: 'icon-list', x: 8, y: 56, w: 84, gap: 6, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-wave', text: 'Ondas decorativas top/bottom' },
            { icon: 'mdi-format-color-fill', text: 'Mitad-y-mitad de color' },
            { icon: 'mdi-blur', text: 'Imágenes difuminadas de fondo' },
            { icon: 'mdi-dots-grid', text: 'Patrones de puntos / cuadrícula' },
            { icon: 'mdi-rotate-3d-variant', text: 'Bandas diagonales' }
          ] },
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right', brand: 'cometax' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'blur-image', opacity: 0.8, blur: 100 },
          { type: 'gradient-overlay', angle: 0, opacityStart: 0.6 },
          { type: 'sparkle', x: 50, y: 18, size: 40, color: 'accent2' },
          { type: 'glossy-ball', x: 80, y: 25, size: 140 },
          { type: 'text', x: 50, y: 38, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Tu turno.' },
          { type: 'shine-line', y: 56, opacity: 0.6 },
          { type: 'text', x: 50, y: 64, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Abre el editor. Cambia el texto. Exporta. 2 minutos.' },
          { type: 'icon', x: 50, y: 78, size: 90, align: 'center', icon: 'mdi-rocket-launch', color: 'accent' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // Showcase · Persona + blur
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'showcase-blur-people',
    name: 'Showcase · Persona + blur',
    description: 'Testimonio con persona placeholder y fondo difuminado. Para portadas humanas.',
    thumbColor: '#ec4899',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'testimonial',
        layers: [
          { type: 'blur-image', opacity: 0.5, blur: 80, x: 30, y: 30, x2: 70, y2: 70 },
          { type: 'gradient-overlay', angle: 0, opacityStart: 0.5 },
          { type: 'avatar', x: 50, y: 32, size: 180, align: 'center', src: 'https://i.pravatar.cc/300?img=32' },
          { type: 'tag-pill', x: 50, y: 12, align: 'center', text: 'Testimonio real' },
          { type: 'shine-line', y: 56, opacity: 0.6 },
          { type: 'text', x: 50, y: 65, w: 86, align: 'center', size: 32, weight: 500, color: 'text', lineHeight: 1.3, text: '"En 90 días pasé de cero a $50k/mes. Solo cambié los carruseles que publicaba."' },
          { type: 'text', x: 50, y: 84, align: 'center', size: 28, weight: 800, color: 'text', text: 'María R.' },
          { type: 'text', x: 50, y: 90, align: 'center', size: 18, weight: 700, color: 'accent', text: 'FOUNDER · AGENCIA DIGITAL MX' },
          { type: 'wave-bottom', h: 12, opacity: 0.5 }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.25 },
          { type: 'dots-pattern', gap: 28, opacity: 0.15 },
          { type: 'glossy-ball', x: 82, y: 22, size: 130 },
          { type: 'tag-pill', x: 50, y: 14, align: 'center', text: 'Crecimiento real' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 300, text: '+847%' },
          { type: 'shine-line', y: 75, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 26, weight: 500, color: 'muted', text: 'engagement promedio en 30 días' },
          { type: 'wave-bottom', h: 18, opacity: 0.6, variant: 'soft' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'diagonal-band', y: 50, h: 14, angle: -8, text: 'Empieza gratis' },
          { type: 'sparkle', x: 18, y: 22, size: 32, color: 'accent2' },
          { type: 'sparkle', x: 82, y: 78, size: 36, color: 'accent' },
          { type: 'text', x: 50, y: 22, align: 'center', size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Sin agencia.\nSin diseñador.' },
          { type: 'avatar', x: 35, y: 75, size: 80, align: 'center', src: 'https://i.pravatar.cc/300?img=12' },
          { type: 'avatar', x: 50, y: 75, size: 80, align: 'center', src: 'https://i.pravatar.cc/300?img=24' },
          { type: 'avatar', x: 65, y: 75, size: 80, align: 'center', src: 'https://i.pravatar.cc/300?img=36' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 22, weight: 700, color: 'accent', text: '+2,400 CREADORES YA LO USAN' },
          { type: 'logo', x: 50, y: 95, size: 32, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // Showcase · Mitad y mitad
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'showcase-half-split',
    name: 'Showcase · Mitad y mitad',
    description: 'Diseño geométrico con mitad-y-mitad y bandas diagonales. Estilo Stripe/Linear.',
    thumbColor: '#22d3ee',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'half-split', angle: 135, opacity: 0.4 },
          { type: 'grid-pattern', gap: 50, opacity: 0.15 },
          { type: 'sparkle', x: 86, y: 22, size: 48, color: 'accent2' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Edición Pro' },
          { type: 'text', x: 8, y: 40, w: 86, size: 92, weight: 900, color: 'text', lineHeight: 1.05, text: 'Geometría\nlimpia.\nIdeas claras.' },
          { type: 'shine-line', y: 78, opacity: 0.7 },
          { type: 'text', x: 8, y: 86, w: 80, size: 26, weight: 500, color: 'muted', text: 'Plantillas con jerarquía visual de verdad.' },
          { type: 'shine-line', y: 92, opacity: 0.7 }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'diagonal-band', y: 16, h: 10, angle: -6, text: 'Disponible ya', fontSize: 22 },
          { type: 'iso-cube', x: 82, y: 36, size: 170 },
          { type: 'text', x: 8, y: 36, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Para todo tipo\nde marca.' },
          { type: 'icon-list', x: 8, y: 64, w: 60, gap: 6, size: 22, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-store', text: 'Tienda física / e-commerce' },
            { icon: 'mdi-school', text: 'Educadores / coaches' },
            { icon: 'mdi-laptop', text: 'SaaS / software' },
            { icon: 'mdi-food', text: 'Restaurantes / food' }
          ] },
          { type: 'wave-bottom', h: 14, opacity: 0.5, variant: 'soft' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'blur-image', blur: 70, opacity: 0.6 },
          { type: 'sparkle', x: 25, y: 25, size: 40, color: 'accent' },
          { type: 'sparkle', x: 75, y: 75, size: 35, color: 'accent2' },
          { type: 'glossy-ball', x: 80, y: 28, size: 150 },
          { type: 'text', x: 8, y: 36, w: 80, size: 72, weight: 900, color: 'text', lineHeight: 1.05, text: 'Hazlo\ndiferente.' },
          { type: 'shine-line', y: 64, opacity: 0.6 },
          { type: 'text', x: 8, y: 72, w: 78, size: 24, weight: 500, color: 'muted', text: 'Tu marca merece más que una plantilla genérica.' },
          { type: 'icon', x: 8, y: 84, size: 60, icon: 'mdi-creation', color: 'accent2' },
          { type: 'wave-bottom', h: 14, opacity: 0.6 },
          { type: 'logo', x: 92, y: 92, size: 38, align: 'right', brand: 'cometax' }
        ]
      }
    ]
  }
)

// ════════════════════════════════════════════════════════════════════════════
// Designer-grade — fotos reales Unsplash + 3D iso shapes
// ════════════════════════════════════════════════════════════════════════════

CAROUSEL_PRESETS.push(
  // ══════════════════════════════════════════════════════════════════════════
  // Photo · Negocio premium
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'photo-business',
    name: 'Foto · Negocio premium',
    description: 'Fotos reales Unsplash, tipografía bold, layout asimétrico tipo editorial.',
    thumbColor: '#0f172a',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'office,laptop,workspace', seed: 311, overlayAngle: 0, overlayOpacity: 0.55 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Edición #042 · Mensual' },
          { type: 'sparkle', x: 86, y: 18, size: 48, color: 'accent2' },
          { type: 'text', x: 8, y: 40, w: 86, size: 100, weight: 900, color: 'text', lineHeight: 1.05, text: 'El estado\ndel SaaS\nen México.' },
          { type: 'shine-line', y: 76, opacity: 0.7 },
          { type: 'text', x: 8, y: 84, w: 80, size: 26, weight: 500, color: 'muted', lineHeight: 1.3, text: 'Datos, fundadores y números reales del último trimestre.' },
          { type: 'text', x: 8, y: 93, size: 20, weight: 800, color: 'accent', text: 'COMETAX · INSIGHTS' }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'minimal,abstract,gradient', seed: 312, overlayAngle: 135, overlayOpacity: 0.7 },
          { type: 'glossy-ball', x: 82, y: 25, size: 130 },
          { type: 'tag-pill', x: 50, y: 12, align: 'center', text: 'Dato del trimestre' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 340, text: '847' },
          { type: 'shine-line', y: 76, opacity: 0.7 },
          { type: 'text', x: 50, y: 82, align: 'center', size: 28, weight: 500, color: 'muted', text: 'SaaS mexicanos lanzados en Q1 2026' },
          { type: 'text', x: 50, y: 92, align: 'center', size: 18, weight: 800, color: 'accent', text: 'FUENTE · COMETAX RESEARCH' }
        ]
      },
      {
        templateId: 'testimonial',
        layers: [
          { type: 'photo-bg', query: 'portrait,professional,woman', seed: 313, overlayAngle: 0, overlayOpacity: 0.6, overlayGrad: 'linear-gradient(0deg, #020617 0%, transparent 60%)' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Founder · Fintech CDMX' },
          { type: 'shine-line', y: 70, opacity: 0.6 },
          { type: 'text', x: 8, y: 78, w: 84, size: 36, weight: 500, color: 'text', lineHeight: 1.3, text: '"En 6 meses pasé de idea a $80,000 MXN/mes. Sin levantar capital."' },
          { type: 'text', x: 8, y: 92, size: 26, weight: 800, color: 'text', text: 'Andrea M.' },
          { type: 'text', x: 8, y: 96, size: 16, weight: 700, color: 'accent', text: 'CEO · MUNDO FINTECH' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.3 },
          { type: 'iso-cube', x: 78, y: 30, size: 220 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Lo que aprendimos' },
          { type: 'text', x: 8, y: 28, size: 60, weight: 900, color: 'text', lineHeight: 1.05, text: '3 patrones\nrepetidos.' },
          { type: 'icon-list', x: 8, y: 60, w: 60, gap: 8, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Empezaron solos, no en equipo' },
            { icon: 'mdi-numeric-2-circle', text: 'Cobraron antes de pulir' },
            { icon: 'mdi-numeric-3-circle', text: 'Distribuyeron 10x más que crearon' }
          ] }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'mountain,sunset,horizon', seed: 314, overlayAngle: 0, overlayOpacity: 0.55 },
          { type: 'glossy-ball', x: 80, y: 25, size: 160 },
          { type: 'sparkle', x: 18, y: 22, size: 32, color: 'accent2' },
          { type: 'text', x: 8, y: 50, w: 80, size: 76, weight: 900, color: 'text', lineHeight: 1.05, text: 'Tu turno\nde aparecer\nen la lista.' },
          { type: 'shine-line', y: 80, opacity: 0.6 },
          { type: 'text', x: 8, y: 86, size: 22, weight: 500, color: 'muted', text: 'Lee el reporte completo' },
          { type: 'text', x: 8, y: 92, size: 28, weight: 800, color: 'accent', text: 'cometax.mx/insights →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // Photo · Producto premium
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'photo-product',
    name: 'Foto · Producto premium',
    description: 'Foto producto con iso-card 3D, half-split, tag glassmorphism. Estilo Apple.',
    thumbColor: '#a855f7',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'minimal,product', seed: 321, overlayAngle: 180, overlayOpacity: 0.7 },
          { type: 'iso-card', x: 50, y: 42, size: 320, icon: 'mdi-rocket-launch', rotateY: -16, rotateX: 6 },
          { type: 'sparkle', x: 18, y: 22, size: 36, color: 'accent2' },
          { type: 'sparkle', x: 82, y: 70, size: 30, color: 'accent' },
          { type: 'tag-pill', x: 50, y: 76, align: 'center', text: 'Disponible en MX' },
          { type: 'text', x: 50, y: 86, align: 'center', size: 72, weight: 900, color: 'text', lineHeight: 1.0, text: 'Gen 2.' },
          { type: 'shine-line', y: 93, opacity: 0.6 },
          { type: 'text', x: 50, y: 96, align: 'center', size: 18, weight: 600, color: 'muted', text: 'Más rápido. Más simple. Más tuyo.' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'photo-bg', query: 'gradient,colorful,abstract', seed: 322, overlayOpacity: 0.85, overlayAngle: 90 },
          { type: 'iso-cube', x: 80, y: 25, size: 180 },
          { type: 'glossy-ball', x: 20, y: 78, size: 100 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Lo que cambia' },
          { type: 'text', x: 8, y: 30, w: 70, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Velocidad,\ndiseño,\ndetalle.' },
          { type: 'icon-list', x: 8, y: 64, w: 80, gap: 8, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-flash', text: '4× más rápido en exportar' },
            { icon: 'mdi-palette', text: '12 paletas premium nuevas' },
            { icon: 'mdi-cube-outline', text: 'Formas 3D editables' }
          ] }
        ]
      },
      {
        templateId: 'testimonial',
        layers: [
          { type: 'photo-bg', query: 'portrait,man,creative', seed: 323, overlayAngle: 0, overlayOpacity: 0.7, overlayGrad: 'linear-gradient(0deg, #0a0e1a 0%, transparent 50%)' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Tester · Beta gen 2' },
          { type: 'shine-line', y: 65, opacity: 0.6 },
          { type: 'text', x: 8, y: 75, w: 84, size: 36, weight: 500, color: 'text', lineHeight: 1.3, text: '"Lo probé 30 minutos y borré mi suscripción de Canva."' },
          { type: 'text', x: 8, y: 90, size: 26, weight: 800, color: 'text', text: 'Diego R.' },
          { type: 'text', x: 8, y: 95, size: 16, weight: 700, color: 'accent', text: 'DISEÑADOR · STUDIO MTY' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 324, overlayOpacity: 0.62 },
          { type: 'glossy-ball', x: 50, y: 32, size: 200 },
          { type: 'sparkle', x: 22, y: 22, size: 32, color: 'accent2' },
          { type: 'text', x: 50, y: 60, align: 'center', size: 80, weight: 900, color: 'text', lineHeight: 1.05, text: 'Pruébalo.' },
          { type: 'shine-line', y: 76, opacity: 0.6 },
          { type: 'text', x: 50, y: 82, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Sin tarjeta. Sin login. 100% en tu navegador.' },
          { type: 'logo', x: 50, y: 92, size: 42, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },

  // ══════════════════════════════════════════════════════════════════════════
  // Photo · Equipo / Vacante
  // ══════════════════════════════════════════════════════════════════════════
  {
    id: 'photo-team',
    name: 'Foto · Equipo / Vacante',
    description: 'Reclutamiento con fotos reales, glossy ball, layout asimétrico premium.',
    thumbColor: '#06b6d4',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'team,office,collaboration', seed: 331, overlayOpacity: 0.65 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Buscamos talento' },
          { type: 'sparkle', x: 86, y: 18, size: 50, color: 'accent2' },
          { type: 'text', x: 8, y: 40, w: 86, size: 110, weight: 900, color: 'text', lineHeight: 1.05, text: 'Únete\nal equipo.' },
          { type: 'shine-line', y: 72, opacity: 0.7 },
          { type: 'text', x: 8, y: 80, w: 80, size: 26, weight: 500, color: 'muted', text: 'Posiciones abiertas en ingeniería, diseño y producto.' },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'COMETAX · CAREERS' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,minimal', seed: 332, overlayOpacity: 0.85, overlayAngle: 135 },
          { type: 'iso-card', x: 78, y: 32, size: 200, icon: 'mdi-laptop' },
          { type: 'tag-pill', x: 8, y: 14, text: 'Por qué unirte' },
          { type: 'text', x: 8, y: 28, w: 60, size: 56, weight: 900, color: 'text', lineHeight: 1.05, text: 'Trabajo\ncomo debe ser.' },
          { type: 'icon-list', x: 8, y: 60, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-home', text: '100% remoto, async' },
            { icon: 'mdi-currency-usd', text: 'Sueldo USD competitivo' },
            { icon: 'mdi-beach', text: '30 días vacaciones' },
            { icon: 'mdi-medical-bag', text: 'Seguro gastos médicos' }
          ] }
        ]
      },
      {
        templateId: 'testimonial',
        layers: [
          { type: 'photo-bg', query: 'portrait,professional,smiling', seed: 333, overlayOpacity: 0.55 },
          { type: 'tag-pill', x: 50, y: 10, align: 'center', text: 'Team · CTO' },
          { type: 'avatar', x: 50, y: 28, size: 160, align: 'center', src: 'https://i.pravatar.cc/300?img=15' },
          { type: 'shine-line', y: 50, opacity: 0.6 },
          { type: 'text', x: 50, y: 60, w: 84, align: 'center', size: 32, weight: 500, color: 'text', lineHeight: 1.3, text: '"Es el lugar donde finalmente puedo trabajar como ingeniero senior, sin reuniones inútiles."' },
          { type: 'text', x: 50, y: 84, align: 'center', size: 26, weight: 800, color: 'text', text: 'Roberto K.' },
          { type: 'text', x: 50, y: 90, align: 'center', size: 18, weight: 700, color: 'accent', text: 'CTO · 4 AÑOS EN COMETAX' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunrise,morning,light', seed: 334, overlayOpacity: 0.5 },
          { type: 'glossy-ball', x: 80, y: 28, size: 180 },
          { type: 'sparkle', x: 18, y: 22, size: 32, color: 'accent2' },
          { type: 'text', x: 8, y: 48, w: 80, size: 64, weight: 900, color: 'text', lineHeight: 1.05, text: 'Aplica\nantes del 30.' },
          { type: 'shine-line', y: 76, opacity: 0.6 },
          { type: 'text', x: 8, y: 82, size: 22, weight: 500, color: 'muted', text: 'Mandamos respuesta a todos. Promesa.' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'accent', text: 'cometax.mx/jobs →' },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'cometax' }
        ]
      }
    ]
  }
)

// ════════════════════════════════════════════════════════════════
// Mockups y pasos — laptop/celular/navegador + tutoriales numerados
// ════════════════════════════════════════════════════════════════

CAROUSEL_PRESETS.push(
  {
    id: 'mockup-saas-launch',
    name: 'Mockup · Lanzamiento SaaS',
    description: 'Producto en navegador con URL real + pasos numerados para empezar. 5 slides.',
    thumbColor: '#6366f1',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'workspace,office', seed: 1, overlayOpacity: 0.75 },
          { type: 'tag-pill', x: 8, y: 10, text: 'Lanzamiento · 2026' },
          { type: 'text', x: 8, y: 30, w: 60, size: 100, weight: 900, color: 'text', text: 'Tu SaaS\nen el navegador.' },
          { type: 'text', x: 8, y: 60, w: 55, size: 26, weight: 500, color: 'muted', text: 'Sin instalar nada. Funciona en cualquier laptop.' },
          { type: 'browser-mockup', x: 75, y: 50, align: 'center', size: 460, url: 'cometax.mx/dashboard' },
          { type: 'logo', x: 8, y: 92, size: 36, brand: 'cometax' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.25 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Cómo funciona' },
          { type: 'text', x: 8, y: 24, size: 56, weight: 900, color: 'text', text: 'En 3 pasos\nempiezas a cobrar.' },
          { type: 'step-row', x: 8, y: 65, w: 84, gap: 14, titleSize: 24, descSize: 16, steps: [
            { title: 'Crea tu cuenta', desc: 'Solo email. Sin tarjeta.', icon: 'mdi-email-outline' },
            { title: 'Configura tus precios', desc: 'Stripe MX o Conekta. OXXO + SPEI.', icon: 'mdi-credit-card' },
            { title: 'Comparte tu link', desc: 'Cobranza automática 24/7.', icon: 'mdi-link-variant' }
          ] },
          { type: 'logo', x: 92, y: 92, size: 32, align: 'right', brand: 'cometax' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 2, overlayOpacity: 0.6 },
          { type: 'tag-pill', x: 50, y: 12, align: 'center', text: 'También en tu bolsillo' },
          { type: 'phone-mockup', x: 50, y: 50, align: 'center', size: 280 },
          { type: 'text', x: 50, y: 88, align: 'center', size: 32, weight: 800, color: 'text', text: 'iOS · Android · PWA' },
          { type: 'logo', x: 50, y: 95, align: 'center', size: 32, brand: 'cometax' }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-overlay', angle: 135, opacityStart: 0.4 },
          { type: 'glossy-ball', x: 78, y: 22, size: 130 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Resultados reales' },
          { type: 'big-number', x: 8, y: 45, size: 280, text: '24h' },
          { type: 'text', x: 8, y: 70, w: 70, size: 32, weight: 700, color: 'text', text: 'es lo que tarda\nun cliente promedio\nen pagarte el primer cobro.' },
          { type: 'logo', x: 92, y: 92, align: 'right', size: 32, brand: 'cometax' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunset,mountain', seed: 3, overlayOpacity: 0.55 },
          { type: 'glossy-ball', x: 50, y: 28, align: 'center', size: 170 },
          { type: 'text', x: 50, y: 58, align: 'center', size: 70, weight: 900, color: 'text', text: 'Empieza\ngratis hoy.' },
          { type: 'text', x: 50, y: 80, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Sin cuenta. Sin tarjeta. Solo prueba.' },
          { type: 'text', x: 50, y: 90, align: 'center', size: 28, weight: 800, color: 'accent', text: 'cometax.mx →' },
          { type: 'logo', x: 50, y: 96, align: 'center', size: 32, brand: 'cometax' }
        ]
      }
    ]
  },
  {
    id: 'mockup-app-feature',
    name: 'Mockup · Feature en celular',
    description: 'Pantalla nueva en mockup celular con descripción + step-row.',
    thumbColor: '#a855f7',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'photo-bg', query: 'gradient,abstract', seed: 4, overlayOpacity: 0.7 },
          { type: 'tag-pill', x: 8, y: 10, text: 'Update · v2.4' },
          { type: 'text', x: 8, y: 32, w: 55, size: 88, weight: 900, color: 'text', text: 'Notificaciones\nque sí avisan.' },
          { type: 'text', x: 8, y: 60, w: 50, size: 24, weight: 500, color: 'muted', text: 'Push, email y WhatsApp en un solo lugar.' },
          { type: 'phone-mockup', x: 78, y: 48, align: 'center', size: 260 },
          { type: 'logo', x: 8, y: 92, size: 32, brand: 'cometax' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'dots-pattern', gap: 28, opacity: 0.15 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Cómo activarlo' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 900, color: 'text', text: 'Tres clicks.\nNada más.' },
          { type: 'step-row', x: 8, y: 60, w: 84, gap: 14, titleSize: 22, descSize: 15, steps: [
            { title: 'Abre el panel', desc: 'Menú · Notificaciones', icon: 'mdi-cog' },
            { title: 'Conecta canales', desc: 'WhatsApp Business o email', icon: 'mdi-message' },
            { title: 'Define cuándo disparar', desc: 'Eventos personalizados', icon: 'mdi-bell-ring' }
          ] },
          { type: 'logo', x: 92, y: 92, align: 'right', size: 30, brand: 'cometax' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'half-split', angle: 135, opacity: 0.3 },
          { type: 'glossy-ball', x: 75, y: 30, size: 140 },
          { type: 'text', x: 8, y: 35, w: 70, size: 60, weight: 900, color: 'text', text: 'Disponible\nahora mismo.' },
          { type: 'text', x: 8, y: 65, w: 70, size: 24, weight: 500, color: 'muted', text: 'Si ya tienes cuenta, actualiza la app.' },
          { type: 'text', x: 8, y: 80, size: 30, weight: 800, color: 'accent', text: 'cometax.mx/changelog' },
          { type: 'logo', x: 8, y: 92, size: 32, brand: 'cometax' }
        ]
      }
    ]
  },
  {
    id: 'tutorial-steps-laptop',
    name: 'Tutorial · 5 pasos con laptop',
    description: 'Tutorial completo con mockup laptop por slide. Educativo profesional.',
    thumbColor: '#22d3ee',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'laptop,workspace', seed: 5, overlayOpacity: 0.7 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Guía paso a paso' },
          { type: 'text', x: 8, y: 35, w: 84, size: 78, weight: 900, color: 'text', text: 'Cómo lanzar\nun SaaS en\n5 pasos reales.' },
          { type: 'text', x: 8, y: 78, size: 22, weight: 600, color: 'accent', text: 'GUARDA Y DESLIZA →' },
          { type: 'logo', x: 92, y: 92, align: 'right', size: 32, brand: 'cometax' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'tag-pill', x: 8, y: 10, text: 'PASO 01 / 05' },
          { type: 'progress-dots', x: 8, y: 18, count: 5, active: 0 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 900, color: 'text', text: 'Define el problema.' },
          { type: 'text', x: 8, y: 46, w: 84, size: 22, weight: 500, color: 'muted', text: 'En una sola frase. Si necesitas párrafos, todavía no lo entiendes.' },
          { type: 'browser-mockup', x: 50, y: 78, align: 'center', size: 440, url: 'notion.so/tu-doc' },
          { type: 'logo', x: 92, y: 95, align: 'right', size: 26, brand: 'cometax' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'tag-pill', x: 8, y: 10, text: 'PASO 02 / 05' },
          { type: 'progress-dots', x: 8, y: 18, count: 5, active: 1 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 900, color: 'text', text: 'Diseña la landing.' },
          { type: 'text', x: 8, y: 46, w: 84, size: 22, weight: 500, color: 'muted', text: 'Hero + 3 features + CTA. Vercel deploy gratis.' },
          { type: 'laptop-mockup', x: 50, y: 78, align: 'center', size: 480 },
          { type: 'logo', x: 92, y: 95, align: 'right', size: 26, brand: 'cometax' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'tag-pill', x: 8, y: 10, text: 'PASO 03 / 05' },
          { type: 'progress-dots', x: 8, y: 18, count: 5, active: 2 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 900, color: 'text', text: 'Conecta Stripe MX.' },
          { type: 'text', x: 8, y: 46, w: 84, size: 22, weight: 500, color: 'muted', text: 'OXXO + SPEI + tarjeta. Webhook a /api/billing.' },
          { type: 'browser-mockup', x: 50, y: 78, align: 'center', size: 440, url: 'dashboard.stripe.com' },
          { type: 'logo', x: 92, y: 95, align: 'right', size: 26, brand: 'cometax' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'tag-pill', x: 8, y: 10, text: 'PASO 04 / 05' },
          { type: 'progress-dots', x: 8, y: 18, count: 5, active: 3 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 900, color: 'text', text: 'Trae 10 usuarios beta.' },
          { type: 'text', x: 8, y: 46, w: 84, size: 22, weight: 500, color: 'muted', text: 'Pídeles feedback brutal. Ajusta. Repite.' },
          { type: 'phone-mockup', x: 50, y: 78, align: 'center', size: 240 },
          { type: 'logo', x: 92, y: 95, align: 'right', size: 26, brand: 'cometax' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'tag-pill', x: 8, y: 10, text: 'PASO 05 / 05' },
          { type: 'progress-dots', x: 8, y: 18, count: 5, active: 4 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 900, color: 'text', text: 'Lanza público.' },
          { type: 'text', x: 8, y: 46, w: 84, size: 22, weight: 500, color: 'muted', text: 'Product Hunt, X, LinkedIn. Cobra desde día 1.' },
          { type: 'glossy-ball', x: 50, y: 70, align: 'center', size: 200 },
          { type: 'icon', x: 50, y: 70, align: 'center', size: 100, icon: 'mdi-rocket-launch', color: 'text' },
          { type: 'logo', x: 92, y: 95, align: 'right', size: 26, brand: 'cometax' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunrise,workspace', seed: 6, overlayOpacity: 0.55 },
          { type: 'glossy-ball', x: 50, y: 30, align: 'center', size: 170 },
          { type: 'text', x: 50, y: 58, align: 'center', size: 60, weight: 900, color: 'text', text: '¿Te sirvió?' },
          { type: 'text', x: 50, y: 78, w: 80, align: 'center', size: 22, weight: 500, color: 'muted', text: 'Sigue para más guías de producto y SaaS MX.' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 26, weight: 800, color: 'accent', text: '@cometax' },
          { type: 'logo', x: 50, y: 95, align: 'center', size: 30, brand: 'cometax' }
        ]
      }
    ]
  },
  {
    id: 'tutorial-steps-quick',
    name: 'Tutorial · 3 pasos rápidos',
    description: 'Mini guía con step-row destacado en un solo slide. Para tips cortos.',
    thumbColor: '#10b981',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'photo-bg', query: 'food,product', seed: 7, overlayOpacity: 0.75 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Tip rápido' },
          { type: 'text', x: 8, y: 38, w: 84, size: 80, weight: 900, color: 'text', text: 'Tu carta digital\nlista en 3 pasos.' },
          { type: 'text', x: 8, y: 78, size: 22, weight: 600, color: 'accent', text: 'Para restaurantes y cafeterías' },
          { type: 'logo', x: 92, y: 92, align: 'right', size: 32, brand: 'cometax' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.22 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Los 3 pasos' },
          { type: 'text', x: 8, y: 22, size: 56, weight: 900, color: 'text', text: 'En 15 minutos\nya está al aire.' },
          { type: 'step-row', x: 8, y: 60, w: 84, gap: 16, titleSize: 24, descSize: 16, steps: [
            { title: 'Sube tu menú PDF o foto', desc: 'Lo extraemos y formateamos por ti', icon: 'mdi-upload' },
            { title: 'Personaliza con tu logo', desc: 'Colores, tipografía, fotos de platillos', icon: 'mdi-palette' },
            { title: 'Comparte el QR en mesa', desc: 'Imprime y pega. Ya pueden ordenar', icon: 'mdi-qrcode' }
          ] },
          { type: 'logo', x: 92, y: 95, align: 'right', size: 28, brand: 'cometax' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'gradient-overlay', angle: 0, opacityStart: 0.4 },
          { type: 'phone-mockup', x: 50, y: 45, align: 'center', size: 280 },
          { type: 'tag-pill', x: 50, y: 12, align: 'center', text: 'Así lo ven tus clientes' },
          { type: 'text', x: 50, y: 82, align: 'center', size: 28, weight: 700, color: 'text', text: 'Limpio. Rápido. Tuyo.' },
          { type: 'logo', x: 50, y: 92, align: 'center', size: 32, brand: 'cometax' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'food', seed: 8, overlayOpacity: 0.6 },
          { type: 'glossy-ball', x: 75, y: 28, size: 140 },
          { type: 'text', x: 8, y: 38, w: 70, size: 64, weight: 900, color: 'text', text: 'Empieza\ngratis hoy.' },
          { type: 'text', x: 8, y: 72, w: 70, size: 22, weight: 500, color: 'muted', text: 'Hasta 50 platillos sin pagar nada.' },
          { type: 'text', x: 8, y: 84, size: 28, weight: 800, color: 'accent', text: 'cometax.mx/cartas →' },
          { type: 'logo', x: 8, y: 94, size: 32, brand: 'cometax' }
        ]
      }
    ]
  }
)

export function findPreset(id) {
  return CAROUSEL_PRESETS.find(p => p.id === id)
}
