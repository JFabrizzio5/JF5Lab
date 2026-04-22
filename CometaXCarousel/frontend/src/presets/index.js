// Carruseles pre-armados. Cada preset tiene:
// - id, name, description, thumbColor (para preview)
// - presetKey (paleta) + sizeKey (tamaño)
// - slides[]: cada slide { templateId, layers: [...] }
// El editor reemplaza state al cargar.

export const CAROUSEL_PRESETS = [
  {
    id: 'product-launch',
    name: 'Lanzamiento de producto',
    description: 'Anuncia un producto nuevo en 6 slides. Hero + razones + precio + CTA.',
    thumbColor: '#6366f1',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 8, y: 10, text: 'NUEVO', color: 'accent' },
          { type: 'text', x: 8, y: 35, size: 110, weight: 900, color: 'text', text: 'Llegó\nNombreApp' },
          { type: 'text', x: 8, y: 55, w: 80, size: 30, weight: 500, color: 'muted', text: 'La forma más rápida de hacer X sin complicarte.' },
          { type: 'gradient-blob', x: 75, y: 75, size: 60, opacity: 0.6 },
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right' }
        ]
      },
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'comet-trail', x: 70, y: 18, size: 50, opacity: 0.7 },
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'muted', text: 'EL PROBLEMA' },
          { type: 'text', x: 8, y: 38, w: 84, size: 56, weight: 800, color: 'text', text: 'Hacer X tomaba\nhoras de trabajo manual.' },
          { type: 'text', x: 8, y: 62, w: 80, size: 26, weight: 500, color: 'muted', text: 'Y nadie tenía tiempo para eso.' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'POR QUÉ FUNCIONA' },
          { type: 'text', x: 8, y: 22, size: 56, weight: 800, color: 'accent', text: '3 razones' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 8, size: 28, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-rocket-launch', text: 'Setup en 60 segundos' },
            { icon: 'mdi-shield-check', text: 'Sin cuenta requerida' },
            { icon: 'mdi-currency-usd', text: 'Free tier generoso' }
          ] },
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right' }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 20, size: 50, opacity: 0.4 },
          { type: 'text', x: 50, y: 32, align: 'center', size: 26, weight: 600, color: 'muted', text: 'TIEMPO AHORRADO' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '8h' },
          { type: 'text', x: 50, y: 67, align: 'center', size: 28, weight: 500, color: 'text', text: 'cada semana, en promedio' },
          { type: 'logo', x: 50, y: 90, size: 40, align: 'center' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 50, y: 12, text: 'PRECIO', color: 'accent', align: 'center' },
          { type: 'text', x: 50, y: 30, align: 'center', size: 36, weight: 700, color: 'muted', text: 'Empieza' },
          { type: 'text', x: 50, y: 48, align: 'center', size: 200, weight: 900, color: 'text', text: 'Gratis' },
          { type: 'text', x: 50, y: 70, align: 'center', size: 28, weight: 500, color: 'accent', text: 'Plan Pro desde $199 MXN/mes' },
          { type: 'logo', x: 50, y: 90, size: 40, align: 'center' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 64, weight: 900, color: 'text', text: 'Pruébalo hoy' },
          { type: 'text', x: 50, y: 45, w: 80, align: 'center', size: 28, weight: 500, color: 'muted', text: 'Link en bio. Sin tarjeta para empezar.' },
          { type: 'icon', x: 50, y: 65, size: 90, align: 'center', icon: 'mdi-arrow-up-circle', color: 'accent2' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 30, weight: 700, color: 'accent', text: '@tumarca' }
        ]
      }
    ]
  },
  {
    id: 'discount-promo',
    name: 'Promo descuento',
    description: 'Oferta con porcentaje de descuento, urgencia y CTA. 5 slides.',
    thumbColor: '#ec4899',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 50, y: 12, text: 'OFERTA LIMITADA', color: 'accent', align: 'center' },
          { type: 'text', x: 50, y: 38, align: 'center', size: 240, weight: 900, color: 'text', text: '-40%' },
          { type: 'text', x: 50, y: 60, w: 80, align: 'center', size: 38, weight: 700, color: 'text', text: 'Solo este fin de semana' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 24, weight: 600, color: 'muted', text: 'Desliza para ver detalles' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'INCLUIDO' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Qué te llevas' },
          { type: 'icon-list', x: 8, y: 40, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-check-circle', text: 'Acceso completo a la plataforma' },
            { icon: 'mdi-check-circle', text: 'Soporte prioritario' },
            { icon: 'mdi-check-circle', text: 'Actualizaciones gratis' },
            { icon: 'mdi-check-circle', text: 'Sin permanencia' }
          ] }
        ]
      },
      {
        templateId: 'before-after',
        layers: [
          { type: 'text', x: 50, y: 8, align: 'center', size: 38, weight: 800, color: 'text', text: 'Compara' },
          { type: 'split', x: 50, y: 50, w: 100, h: 70, leftLabel: 'NORMAL', rightLabel: 'CON DESCUENTO', leftItems: ['$1,500 MXN/mes', 'Pago anual', 'Mismo producto'], rightItems: ['$899 MXN/mes', 'Mismas features', 'Ahorras $7,200/año'] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 30, size: 60, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'TERMINA EN' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '48h' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 600, color: 'text', text: 'No esperes al último día' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 60, weight: 900, color: 'text', text: 'Aprovecha\nya' },
          { type: 'text', x: 50, y: 52, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Código: PROMO40 al checkout' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-cart-arrow-down', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'Link en bio →' }
        ]
      }
    ]
  },
  {
    id: 'tips-5',
    name: '5 tips rápidos',
    description: 'Cover + 5 tips numerados + CTA follow. Educativo, alta retención.',
    thumbColor: '#22d3ee',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'comet-trail', x: 75, y: 20, size: 60, opacity: 0.7 },
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'GUARDA ESTE POST' },
          { type: 'text', x: 8, y: 42, w: 84, size: 80, weight: 900, color: 'text', text: '5 tips para\nlanzar tu MVP\nen un fin de semana' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Desliza →' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'TIP 01 / 05' },
          { type: 'progress-dots', x: 8, y: 14, count: 5, active: 0 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Define\nuna sola feature' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: 'Si no puedes describirla en una frase, todavía no tienes MVP. Tienes ambición.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-target', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'TIP 02 / 05' },
          { type: 'progress-dots', x: 8, y: 14, count: 5, active: 1 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Usa stack\nque ya conoces' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: 'No es momento de aprender Rust. Es momento de validar.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-toolbox-outline', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'TIP 03 / 05' },
          { type: 'progress-dots', x: 8, y: 14, count: 5, active: 2 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Cobra\ndesde el día 1' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: '"Free hasta validar" suena lindo. Pero un usuario que paga $1 te enseña más que 100 gratis.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-cash', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'TIP 04 / 05' },
          { type: 'progress-dots', x: 8, y: 14, count: 5, active: 3 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Hospéda\nen 1 servicio' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: 'Vercel, Railway, Render. Lo que sea. Pero no armes Kubernetes para 3 usuarios.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-cloud-upload', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'TIP 05 / 05' },
          { type: 'progress-dots', x: 8, y: 14, count: 5, active: 4 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Lanza\nantes de pulir' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: 'Si te da pena lo que lanzaste, lanzaste a tiempo.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-rocket-launch', color: 'accent' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: '¿Te sirvió?' },
          { type: 'text', x: 50, y: 45, w: 80, align: 'center', size: 28, weight: 500, color: 'muted', text: 'Sigue para más tips de producto y MVPs' },
          { type: 'icon', x: 38, y: 65, size: 70, align: 'center', icon: 'mdi-bookmark', color: 'accent' },
          { type: 'icon', x: 50, y: 65, size: 70, align: 'center', icon: 'mdi-heart', color: 'accent2' },
          { type: 'icon', x: 62, y: 65, size: 70, align: 'center', icon: 'mdi-share-variant', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: '@tumarca' }
        ]
      }
    ]
  },
  {
    id: 'before-after-case',
    name: 'Antes vs Después (caso éxito)',
    description: 'Hook + situación inicial + cambio + resultado en métrica.',
    thumbColor: '#10b981',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'CASO REAL' },
          { type: 'text', x: 8, y: 45, w: 84, size: 70, weight: 900, color: 'text', text: 'Cómo María\npasó de cero ventas\na $50k/mes' },
          { type: 'text', x: 8, y: 80, size: 24, weight: 600, color: 'accent', text: 'En 90 días. Sin ads pagados.' }
        ]
      },
      {
        templateId: 'before-after',
        layers: [
          { type: 'text', x: 50, y: 8, align: 'center', size: 38, weight: 800, color: 'text', text: 'El cambio' },
          { type: 'split', x: 50, y: 50, w: 100, h: 70, leftLabel: 'ANTES', rightLabel: 'DESPUÉS', leftItems: ['Posts random', 'Sin sistema', '0 leads/semana'], rightItems: ['Carruseles diarios', 'Calendario editorial', '40+ leads/semana'] }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'QUÉ HIZO' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: '3 cambios clave' },
          { type: 'icon-list', x: 8, y: 40, w: 84, gap: 8, size: 28, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Definió 1 sola buyer persona' },
            { icon: 'mdi-numeric-2-circle', text: 'Usó plantillas (no diseñó cada post)' },
            { icon: 'mdi-numeric-3-circle', text: 'Publicó 5 días/semana sin falta' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'RESULTADO' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 180, weight: 900, color: 'accent', text: '+1,247%' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'crecimiento de revenue en 90 días' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: '¿Quieres lo mismo?' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Te dejo la guía completa en el link de la bio. Es gratis.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-link-variant', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: '@tumarca' }
        ]
      }
    ]
  },
  {
    id: 'feature-announce',
    name: 'Feature nueva',
    description: 'Anuncia un feature nuevo. Badge, qué hace, cómo usarlo, CTA.',
    thumbColor: '#818cf8',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 8, y: 10, text: 'JUST SHIPPED', color: 'accent' },
          { type: 'text', x: 8, y: 38, size: 100, weight: 900, color: 'text', text: 'Carrusel\nWizard 2.0' },
          { type: 'text', x: 8, y: 58, w: 80, size: 30, weight: 500, color: 'muted', text: 'Genera 10 slides en menos de un minuto.' },
          { type: 'gradient-blob', x: 80, y: 80, size: 55, opacity: 0.55 },
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'QUÉ TRAE' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'accent', text: '3 cosas nuevas' },
          { type: 'icon-list', x: 8, y: 40, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-magic-staff', text: 'Generador AI desde un prompt' },
            { icon: 'mdi-content-duplicate', text: '12 carruseles pre-armados' },
            { icon: 'mdi-export', text: 'Export ZIP numerado para subir' }
          ] }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'CÓMO USARLO' },
          { type: 'text', x: 8, y: 24, size: 56, weight: 800, color: 'text', text: 'En 3 clics' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Abre el editor' },
            { icon: 'mdi-numeric-2-circle', text: 'Elige carrusel pre-armado' },
            { icon: 'mdi-numeric-3-circle', text: 'Cambia textos y exporta' }
          ] }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 56, weight: 900, color: 'text', text: 'Pruébalo' },
          { type: 'text', x: 50, y: 48, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Es gratis. Sin login. Tus diseños no salen del navegador.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-rocket-launch', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'cometax-carousel.com' }
        ]
      }
    ]
  },
  {
    id: 'tutorial-3-steps',
    name: 'Mini tutorial 3 pasos',
    description: 'Cover + 3 pasos numerados + ya quedó. Educativo corto.',
    thumbColor: '#a78bfa',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'comet-trail', x: 70, y: 18, size: 50, opacity: 0.7 },
          { type: 'text', x: 8, y: 20, size: 22, weight: 700, color: 'muted', text: 'TUTORIAL' },
          { type: 'text', x: 8, y: 50, w: 84, size: 70, weight: 900, color: 'text', text: 'Cómo facturar\nCFDI en 3 pasos' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Desliza →' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'PASO 01 / 03' },
          { type: 'progress-dots', x: 8, y: 14, count: 3, active: 0 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Carga tu CSD\ndel SAT' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: 'Sube los archivos .cer y .key. Tu contraseña queda solo en tu navegador.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-file-key', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'PASO 02 / 03' },
          { type: 'progress-dots', x: 8, y: 14, count: 3, active: 1 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Captura\nla operación' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: 'RFC del cliente, productos, importes. El catálogo SAT autocompleta.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-pencil', color: 'accent' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'PASO 03 / 03' },
          { type: 'progress-dots', x: 8, y: 14, count: 3, active: 2 },
          { type: 'text', x: 8, y: 30, size: 56, weight: 800, color: 'text', text: 'Timbra\ny envía' },
          { type: 'text', x: 8, y: 55, w: 84, size: 28, weight: 500, color: 'muted', text: 'Un solo click. Recibes XML + PDF. WhatsApp opcional al cliente.' },
          { type: 'icon', x: 50, y: 80, size: 90, align: 'center', icon: 'mdi-check-decagram', color: 'accent' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 60, weight: 900, color: 'text', text: 'Ya quedó' },
          { type: 'text', x: 50, y: 48, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Sigue para más tutoriales de SAT y CFDI' },
          { type: 'icon', x: 50, y: 68, size: 100, align: 'center', icon: 'mdi-heart', color: 'accent2' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: '@tumarca' }
        ]
      }
    ]
  },
  {
    id: 'tools-recommendation',
    name: 'Recomendación de herramientas',
    description: '6 herramientas con descripción corta. Categoría dev/marketing/design.',
    thumbColor: '#34d399',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'GUARDA ESTE POST' },
          { type: 'text', x: 8, y: 45, w: 84, size: 70, weight: 900, color: 'text', text: '6 herramientas\ngratis para devs\nque cambian el juego' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Ninguna requiere tarjeta →' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'accent', text: '01' },
          { type: 'text', x: 8, y: 28, size: 80, weight: 900, color: 'text', text: 'Cursor' },
          { type: 'text', x: 8, y: 42, size: 28, weight: 600, color: 'accent', text: 'Editor de código con AI nativo' },
          { type: 'text', x: 8, y: 60, w: 84, size: 26, weight: 500, color: 'muted', text: 'Reemplaza VS Code. Tab para autocompletar funciones enteras. El plan free aguanta para uso casual.' },
          { type: 'icon', x: 80, y: 75, size: 120, align: 'center', icon: 'mdi-language-cpp', color: 'accent' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'accent', text: '02' },
          { type: 'text', x: 8, y: 28, size: 80, weight: 900, color: 'text', text: 'Vercel' },
          { type: 'text', x: 8, y: 42, size: 28, weight: 600, color: 'accent', text: 'Deploy en un git push' },
          { type: 'text', x: 8, y: 60, w: 84, size: 26, weight: 500, color: 'muted', text: 'SSL gratis, CDN global, build automático. Free tier brutal para proyectos personales.' },
          { type: 'icon', x: 80, y: 75, size: 120, align: 'center', icon: 'mdi-triangle', color: 'accent' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'accent', text: '03' },
          { type: 'text', x: 8, y: 28, size: 80, weight: 900, color: 'text', text: 'Neon' },
          { type: 'text', x: 8, y: 42, size: 28, weight: 600, color: 'accent', text: 'Postgres serverless' },
          { type: 'text', x: 8, y: 60, w: 84, size: 26, weight: 500, color: 'muted', text: 'Branching de DB como git. Suspende cuando no la usas. Free hasta 0.5 GB.' },
          { type: 'icon', x: 80, y: 75, size: 120, align: 'center', icon: 'mdi-database', color: 'accent' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'accent', text: '04' },
          { type: 'text', x: 8, y: 28, size: 80, weight: 900, color: 'text', text: 'Resend' },
          { type: 'text', x: 8, y: 42, size: 28, weight: 600, color: 'accent', text: 'Email transaccional' },
          { type: 'text', x: 8, y: 60, w: 84, size: 26, weight: 500, color: 'muted', text: 'API limpia, React Email para templates. 3,000 emails/mes gratis.' },
          { type: 'icon', x: 80, y: 75, size: 120, align: 'center', icon: 'mdi-email-fast', color: 'accent' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'accent', text: '05' },
          { type: 'text', x: 8, y: 28, size: 80, weight: 900, color: 'text', text: 'Sentry' },
          { type: 'text', x: 8, y: 42, size: 28, weight: 600, color: 'accent', text: 'Errores en tiempo real' },
          { type: 'text', x: 8, y: 60, w: 84, size: 26, weight: 500, color: 'muted', text: 'Te enteras del bug antes que el usuario te avise. Free 5k errores/mes.' },
          { type: 'icon', x: 80, y: 75, size: 120, align: 'center', icon: 'mdi-bug-outline', color: 'accent' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'accent', text: '06' },
          { type: 'text', x: 8, y: 28, size: 80, weight: 900, color: 'text', text: 'Plausible' },
          { type: 'text', x: 8, y: 42, size: 28, weight: 600, color: 'accent', text: 'Analytics sin cookies' },
          { type: 'text', x: 8, y: 60, w: 84, size: 26, weight: 500, color: 'muted', text: 'GDPR-friendly, dashboard simple. Self-host gratis u hosted desde $9/mes.' },
          { type: 'icon', x: 80, y: 75, size: 120, align: 'center', icon: 'mdi-chart-line', color: 'accent' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: '¿Cuál te falta?' },
          { type: 'text', x: 50, y: 48, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Comenta abajo. Si conoces otra que no esté, también.' },
          { type: 'icon', x: 50, y: 68, size: 100, align: 'center', icon: 'mdi-comment-text', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: '@tumarca' }
        ]
      }
    ]
  },
  {
    id: 'webinar-event',
    name: 'Webinar / evento',
    description: 'Save the date + agenda + speakers + CTA registro.',
    thumbColor: '#f59e0b',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 50, y: 12, text: 'WEBINAR GRATIS', color: 'accent', align: 'center' },
          { type: 'text', x: 50, y: 38, align: 'center', size: 70, weight: 900, color: 'text', text: 'Cómo lanzar\nun SaaS MX' },
          { type: 'text', x: 50, y: 60, w: 80, align: 'center', size: 30, weight: 500, color: 'muted', text: 'sin gastar más de $1,000 en infra' },
          { type: 'text', x: 50, y: 82, align: 'center', size: 36, weight: 700, color: 'accent', text: '15 mayo · 6:00 PM' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'AGENDA' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Lo que vas a ver' },
          { type: 'icon-list', x: 8, y: 40, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-clock-outline', text: '6:00 — Bienvenida' },
            { icon: 'mdi-rocket-launch', text: '6:10 — Demo en vivo' },
            { icon: 'mdi-cash-multiple', text: '6:35 — Stack y costos reales' },
            { icon: 'mdi-comment-question', text: '7:00 — Q&A abierto' }
          ] }
        ]
      },
      {
        templateId: 'testimonial',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'TU INVITADO' },
          { type: 'avatar', x: 50, y: 35, size: 140, align: 'center' },
          { type: 'text', x: 50, y: 55, align: 'center', size: 40, weight: 800, color: 'text', text: 'María R.' },
          { type: 'text', x: 50, y: 64, align: 'center', size: 22, weight: 600, color: 'accent', text: 'Founder · 4 SaaS lanzados en MX' },
          { type: 'text', x: 50, y: 80, w: 84, align: 'center', size: 22, weight: 500, color: 'muted', text: '"Te voy a enseñar lo que me hubiera ahorrado meses si alguien me lo decía cuando empecé."' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Aparta\ntu lugar' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Cupo limitado. Recibirás recordatorio 1h antes.' },
          { type: 'icon', x: 50, y: 68, size: 100, align: 'center', icon: 'mdi-calendar-check', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'Link en bio →' }
        ]
      }
    ]
  },
  {
    id: 'job-opening',
    name: 'Vacante / reclutamiento',
    description: 'Buscamos X. Perks. Requisitos. Cómo aplicar.',
    thumbColor: '#06b6d4',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 50, y: 12, text: 'ESTAMOS CONTRATANDO', color: 'accent', align: 'center' },
          { type: 'text', x: 50, y: 40, align: 'center', size: 80, weight: 900, color: 'text', text: 'Senior\nFull-stack' },
          { type: 'text', x: 50, y: 65, w: 80, align: 'center', size: 28, weight: 500, color: 'muted', text: '100% remoto · LATAM · USD' },
          { type: 'text', x: 50, y: 85, align: 'center', size: 24, weight: 700, color: 'accent', text: 'Desliza para detalles →' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'PERKS' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Por qué unirte' },
          { type: 'icon-list', x: 8, y: 40, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-currency-usd', text: '$3,500 - $5,000 USD/mes' },
            { icon: 'mdi-home', text: '100% remoto, async friendly' },
            { icon: 'mdi-beach', text: '30 días vacaciones pagadas' },
            { icon: 'mdi-laptop', text: 'Equipo y home office stipend' }
          ] }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'BUSCAMOS' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'accent', text: 'Si tienes' },
          { type: 'icon-list', x: 8, y: 40, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-check', text: '5+ años con TypeScript' },
            { icon: 'mdi-check', text: 'Experiencia con Postgres + ORM' },
            { icon: 'mdi-check', text: 'Has lanzado producto a producción' },
            { icon: 'mdi-check', text: 'Inglés conversacional' }
          ] }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Aplica\nantes del 30' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Manda CV + GitHub al link en la bio. Respondemos a todos.' },
          { type: 'icon', x: 50, y: 68, size: 100, align: 'center', icon: 'mdi-send', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: '@tumarca' }
        ]
      }
    ]
  },
  {
    id: 'testimonial-case',
    name: 'Testimonio cliente',
    description: 'Quote + foto/nombre + métrica resultado. 3 slides.',
    thumbColor: '#c084fc',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'testimonial',
        layers: [
          { type: 'text', x: 50, y: 12, align: 'center', size: 100, weight: 700, color: 'accent', text: '"' },
          { type: 'text', x: 50, y: 38, w: 84, align: 'center', size: 38, weight: 500, color: 'text', text: 'Pasé de 3 semanas a 1 día para lanzar mi MVP. CometaX me ahorró meses de trabajo.' },
          { type: 'avatar', x: 50, y: 70, size: 90, align: 'center' },
          { type: 'text', x: 50, y: 80, align: 'center', size: 26, weight: 700, color: 'text', text: 'María R.' },
          { type: 'text', x: 50, y: 85, align: 'center', size: 20, weight: 500, color: 'muted', text: 'Founder · Dev tools MX' }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'TIEMPO AHORRADO' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '21x' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'más rápido que armarlo a mano' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 30, align: 'center', size: 56, weight: 900, color: 'text', text: '¿Tu turno?' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Empieza gratis. Sin tarjeta. Sin compromiso.' },
          { type: 'icon', x: 50, y: 68, size: 100, align: 'center', icon: 'mdi-rocket-launch', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'Link en bio →' }
        ]
      }
    ]
  },
  {
    id: 'engagement-question',
    name: 'Pregunta / engagement',
    description: 'Pregunta provocadora + opciones + comenta abajo.',
    thumbColor: '#a3e635',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'text', x: 50, y: 18, align: 'center', size: 22, weight: 700, color: 'muted', text: 'PREGUNTA SERIA' },
          { type: 'text', x: 50, y: 50, w: 84, align: 'center', size: 70, weight: 900, color: 'text', text: '¿Qué prefieres:\nlanzar feo y rápido\no perfecto y tarde?' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 24, weight: 600, color: 'accent', text: 'Desliza →' }
        ]
      },
      {
        templateId: 'before-after',
        layers: [
          { type: 'text', x: 50, y: 8, align: 'center', size: 38, weight: 800, color: 'text', text: 'Las dos posturas' },
          { type: 'split', x: 50, y: 50, w: 100, h: 70, leftLabel: 'EQUIPO RÁPIDO', rightLabel: 'EQUIPO PULIDO', leftItems: ['Aprende del usuario', 'Itera con datos', 'Recauda más fácil'], rightItems: ['Mejor primera impresión', 'Marca cuidada', 'Menos refactor después'] }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: '¿Tú qué\nharías?' },
          { type: 'text', x: 50, y: 52, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Comenta abajo. Bonus si das ejemplo real.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-comment-text', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: '@tumarca' }
        ]
      }
    ]
  },
  {
    id: 'restaurant-promo',
    name: 'Restaurante / Food promo',
    description: 'Plato del día, precio, horario, ubicación. 4 slides.',
    thumbColor: '#fb923c',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 50, y: 12, text: 'HOY EN EL MENÚ', color: 'accent', align: 'center' },
          { type: 'text', x: 50, y: 42, align: 'center', size: 90, weight: 900, color: 'text', text: 'Tacos\nde birria' },
          { type: 'text', x: 50, y: 62, align: 'center', size: 32, weight: 500, color: 'muted', text: 'Receta de la abuela. 8h cocción.' },
          { type: 'icon', x: 50, y: 80, size: 100, align: 'center', icon: 'mdi-food', color: 'accent' }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 32, align: 'center', size: 26, weight: 700, color: 'muted', text: 'ORDEN DE 4 PIEZAS' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 220, weight: 900, color: 'accent', text: '$89' },
          { type: 'text', x: 50, y: 70, align: 'center', size: 28, weight: 500, color: 'text', text: 'Incluye consomé y guacamole' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'INFO' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Te esperamos' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 9, size: 28, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-clock-outline', text: 'Lun-Sáb · 12 PM - 9 PM' },
            { icon: 'mdi-map-marker', text: 'Av. Insurgentes 123, CDMX' },
            { icon: 'mdi-phone', text: '55 1234 5678 (pedidos)' }
          ] }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 60, weight: 900, color: 'text', text: 'Pídelos\nya' },
          { type: 'text', x: 50, y: 52, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Rappi, Didi, Uber Eats — o ven directo.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-silverware-fork-knife', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: '@tutaqueria' }
        ]
      }
    ]
  }
]

export function findPreset(id) {
  return CAROUSEL_PRESETS.find(p => p.id === id)
}
