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
          { type: 'logo', x: 92, y: 92, size: 40, align: 'right', brand: 'cometax' }
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
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right', brand: 'cometax' }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 20, size: 50, opacity: 0.4 },
          { type: 'text', x: 50, y: 32, align: 'center', size: 26, weight: 600, color: 'muted', text: 'TIEMPO AHORRADO' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '8h' },
          { type: 'text', x: 50, y: 67, align: 'center', size: 28, weight: 500, color: 'text', text: 'cada semana, en promedio' },
          { type: 'logo', x: 50, y: 90, size: 40, align: 'center', brand: 'cometax' }
        ]
      },
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 50, y: 12, text: 'PRECIO', color: 'accent', align: 'center' },
          { type: 'text', x: 50, y: 30, align: 'center', size: 36, weight: 700, color: 'muted', text: 'Empieza' },
          { type: 'text', x: 50, y: 48, align: 'center', size: 200, weight: 900, color: 'text', text: 'Gratis' },
          { type: 'text', x: 50, y: 70, align: 'center', size: 28, weight: 500, color: 'accent', text: 'Plan Pro desde $199 MXN/mes' },
          { type: 'logo', x: 50, y: 90, size: 40, align: 'center', brand: 'cometax' }
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
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right', brand: 'cometax' }
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

// ════════════════════════════════════════════════════════════════
// CometaX SaaS — un carrusel por producto explicando qué resuelve
// ════════════════════════════════════════════════════════════════

CAROUSEL_PRESETS.push(
  {
    id: 'cometax-stocklink',
    name: 'StockLink — pitch',
    description: 'Inventario multi-tenant MX para tiendita, restaurante, paquetería, constructora. 5 slides.',
    thumbColor: '#6366f1',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 8, y: 10, text: 'STOCKLINK', color: 'accent' },
          { type: 'text', x: 8, y: 36, size: 90, weight: 900, color: 'text', text: 'Tu inventario\nse te escapa\nde las manos.' },
          { type: 'text', x: 8, y: 62, w: 80, size: 28, weight: 500, color: 'muted', text: 'Excel ya no aguanta. Y los sistemas grandes cuestan $5,000 al mes.' },
          { type: 'gradient-blob', x: 80, y: 80, size: 55, opacity: 0.55 },
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right', brand: 'stocklink' }
        ]
      },
      {
        templateId: 'before-after',
        layers: [
          { type: 'text', x: 50, y: 8, align: 'center', size: 38, weight: 800, color: 'text', text: 'StockLink vs Excel' },
          { type: 'split', x: 50, y: 50, w: 100, h: 70, leftLabel: 'EXCEL', rightLabel: 'STOCKLINK', leftItems: ['Sin alertas', 'No multi-sucursal', 'No QR/barcode', 'Pierdes stock'], rightItems: ['Alertas auto', 'Multi-tenant + RLS', 'QR + NFC + barcode', 'Movimientos atómicos'] }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'PARA QUIÉN' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'accent', text: 'Una sola app\n4 industrias' },
          { type: 'icon-list', x: 8, y: 45, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-store', text: 'Tiendita / Abarrotes' },
            { icon: 'mdi-silverware-fork-knife', text: 'Restaurante (decuento auto por venta)' },
            { icon: 'mdi-truck-delivery', text: 'Paquetería / Bodega' },
            { icon: 'mdi-hammer-wrench', text: 'Construcción / Taller' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'PRECIO MENOR' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '$499' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'MXN/mes · Plan Starter' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'gradient-blob', x: 50, y: 50, size: 80, opacity: 0.5 },
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Demo gratis\ncon datos reales' },
          { type: 'text', x: 50, y: 52, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Carga tu industria, vemos cómo se ve con tus SKUs.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-package-variant', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'stocklink.mx' }
        ]
      }
    ]
  },
  {
    id: 'cometax-notamx',
    name: 'NotaMX — pitch',
    description: 'POS + notas de venta + WhatsApp + CFDI 4.0 para freelancers y PYME MX. 5 slides.',
    thumbColor: '#10b981',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'NOTAMX' },
          { type: 'text', x: 8, y: 45, w: 84, size: 70, weight: 900, color: 'text', text: '¿Cobras\npor WhatsApp\ny olvidas la factura?' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Hay solución →' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'TODO EN UNO' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Cobra y factura\ndesde un solo lugar' },
          { type: 'icon-list', x: 8, y: 45, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-whatsapp', text: 'Mandas link de pago por WhatsApp' },
            { icon: 'mdi-credit-card', text: 'Stripe + Conekta (OXXO/SPEI/tarjeta)' },
            { icon: 'mdi-receipt-text', text: 'CFDI 4.0 timbrado automático' },
            { icon: 'mdi-file-pdf-box', text: 'PDF + XML al cliente, sin tocar nada' }
          ] }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'CÓMO' },
          { type: 'text', x: 8, y: 22, size: 56, weight: 800, color: 'text', text: 'En 30 segundos' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Capturas el monto y cliente' },
            { icon: 'mdi-numeric-2-circle', text: 'Mandas link por WhatsApp' },
            { icon: 'mdi-numeric-3-circle', text: 'Cliente paga, factura sale sola' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'EMPIEZA EN' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 220, weight: 900, color: 'accent', text: '$0' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: '5 facturas/mes gratis. Después $1.50 c/u.' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Sin contador.\nSin sistema caro.' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'NotaMX. Para freelancers, talleres, consultorios y PYMEs MX.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-receipt', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'notamx.com' }
        ]
      }
    ]
  },
  {
    id: 'cometax-porcobrar',
    name: 'PorCobrar — pitch',
    description: 'Cobranza automática + scoring deudores + dunning. Para CFOs y contadores MX. 5 slides.',
    thumbColor: '#f59e0b',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'PORCOBRAR' },
          { type: 'text', x: 8, y: 45, w: 84, size: 64, weight: 900, color: 'text', text: '¿Tu cartera\nvencida\nya pasa los\n$200,000?' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Hay forma de cobrarla →' }
        ]
      },
      {
        templateId: 'before-after',
        layers: [
          { type: 'text', x: 50, y: 8, align: 'center', size: 38, weight: 800, color: 'text', text: 'Antes vs Con PorCobrar' },
          { type: 'split', x: 50, y: 50, w: 100, h: 70, leftLabel: 'AHORA', rightLabel: 'CON PORCOBRAR', leftItems: ['Persigues por WA', 'Excel de vencimientos', 'Olvidas seguimientos', '0 score de deudor'], rightItems: ['Dunning auto', 'Subes CFDI XML', 'Recordatorios 1/3/7/15d', 'Score IA por deudor'] }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'CÓMO FUNCIONA' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'accent', text: '4 pasos' },
          { type: 'icon-list', x: 8, y: 45, w: 84, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Subes tus CFDI XML (parser auto)' },
            { icon: 'mdi-numeric-2-circle', text: 'Eliges flow de cobranza' },
            { icon: 'mdi-numeric-3-circle', text: 'Mandamos WA/email + link Stripe' },
            { icon: 'mdi-numeric-4-circle', text: 'Cobras. Score se actualiza solo' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'RECUPERAS EN PROMEDIO' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '67%' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'de tu cartera vencida en 30 días' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Para CFOs\ny contadores MX' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Demo con tus XMLs. Si no recuperamos, no pagas.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-cash-fast', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'porcobrar.mx' }
        ]
      }
    ]
  },
  {
    id: 'cometax-pulsomx',
    name: 'PulsoMX — pitch',
    description: 'Software para gym, yoga, coworking, dojos. Sin pagar Mindbody. 5 slides.',
    thumbColor: '#ec4899',
    presetKey: 'sunset',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'product-launch',
        layers: [
          { type: 'badge', x: 8, y: 10, text: 'PULSOMX', color: 'accent' },
          { type: 'text', x: 8, y: 38, size: 80, weight: 900, color: 'text', text: 'Mindbody\ncuesta\n$3,500/mes.\nPulsoMX no.' },
          { type: 'text', x: 8, y: 75, w: 80, size: 28, weight: 500, color: 'muted', text: 'Para gyms, yoga studios, coworkings y dojos en MX.' },
          { type: 'logo', x: 92, y: 92, size: 36, align: 'right', brand: 'pulsomx' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'INCLUYE' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Todo lo que necesitas' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-account-group', text: 'Membresías + planes recurrentes' },
            { icon: 'mdi-calendar-clock', text: 'Reservas de clases + cupos' },
            { icon: 'mdi-qrcode-scan', text: 'Check-in con QR en la puerta' },
            { icon: 'mdi-credit-card', text: 'Stripe + Conekta (OXXO/SPEI)' },
            { icon: 'mdi-chart-line', text: 'Dashboard MRR + churn' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'AHORRO ANUAL VS MINDBODY' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 180, weight: 900, color: 'accent', text: '$36,000' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'MXN/año en software' }
        ]
      },
      {
        templateId: 'tip-tutorial',
        layers: [
          { type: 'text', x: 8, y: 8, size: 22, weight: 700, color: 'accent', text: 'SETUP' },
          { type: 'text', x: 8, y: 22, size: 56, weight: 800, color: 'text', text: 'Listo en 1 día' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Cargas tus clases y horarios' },
            { icon: 'mdi-numeric-2-circle', text: 'Cargas planes (mensual, paquete 10)' },
            { icon: 'mdi-numeric-3-circle', text: 'Compartes link a tus alumnos' }
          ] }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Demo gratis\n14 días' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Sin tarjeta. Migración asistida si vienes de Mindbody.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-dumbbell', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'pulsomx.com' }
        ]
      }
    ]
  },
  {
    id: 'cometax-agendapro',
    name: 'AgendaPro — pitch',
    description: 'Reservas con pago anticipado para barberos, dentistas, vets, coaches. 5 slides.',
    thumbColor: '#1e40af',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'comet-trail', x: 70, y: 18, size: 50, opacity: 0.7 },
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'AGENDAPRO' },
          { type: 'text', x: 8, y: 48, w: 84, size: 64, weight: 900, color: 'text', text: '40% de tus citas\nno llegan.\nY no avisan.' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Solución: pago anticipado →' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'CÓMO' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Solo paga, solo asiste' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-calendar-check', text: 'Cliente reserva en tu link' },
            { icon: 'mdi-credit-card', text: 'Paga el 100% o un anticipo' },
            { icon: 'mdi-whatsapp', text: 'Recordatorio WA 24h y 1h antes' },
            { icon: 'mdi-star-outline', text: 'Pide review en Google al terminar' }
          ] }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'PARA QUIÉN' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'accent', text: 'Tú, si tu chamba\nes con cita' },
          { type: 'icon-list', x: 8, y: 45, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-content-cut', text: 'Barbería / estética' },
            { icon: 'mdi-tooth', text: 'Dentista / médico' },
            { icon: 'mdi-paw', text: 'Veterinaria' },
            { icon: 'mdi-meditation', text: 'Coach / terapeuta' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'BAJA NO-SHOWS' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '-87%' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'cuando cobras anticipo' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Tu agenda,\ncon dinero\nadelantado' },
          { type: 'text', x: 50, y: 60, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'AgendaPro. Reservas que sí pagan.' },
          { type: 'icon', x: 50, y: 78, size: 80, align: 'center', icon: 'mdi-calendar-clock', color: 'accent' },
          { type: 'text', x: 50, y: 92, align: 'center', size: 26, weight: 700, color: 'accent', text: 'agendapro.mx' }
        ]
      }
    ]
  },
  {
    id: 'cometax-rentafacil',
    name: 'RentaFacil — pitch',
    description: 'Admin inmobiliario para arrendadores: contratos, pagos, inquilinos. 4 slides.',
    thumbColor: '#84cc16',
    presetKey: 'forest',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'RENTAFACIL' },
          { type: 'text', x: 8, y: 45, w: 84, size: 70, weight: 900, color: 'text', text: 'Tienes 5 deptos.\nY un Excel\nque ya odias.' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Hay vida después de Excel →' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'INCLUYE' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Renta sin pelearte' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-home-city', text: 'Multi-propiedad' },
            { icon: 'mdi-file-document-edit', text: 'Contratos PDF/DOCX al instante' },
            { icon: 'mdi-cash-multiple', text: 'Recordatorio de pago + recibo CFDI' },
            { icon: 'mdi-account-multiple', text: 'Histórico de inquilinos' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'AHORRAS' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '12h' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'al mes en cobranza y papeleo' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: '$199/mes\npor 5 deptos' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Sin permanencia. Cancela cuando quieras.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-home', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'rentafacil.mx' }
        ]
      }
    ]
  },
  {
    id: 'cometax-rankit',
    name: 'RanKiT — pitch',
    description: 'Tracker de visibilidad SEO. Pega tu dominio y ve dónde apareces. 4 slides.',
    thumbColor: '#22d3ee',
    presetKey: 'midnight',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'comet-trail', x: 75, y: 20, size: 50, opacity: 0.7 },
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'RANKIT' },
          { type: 'text', x: 8, y: 50, w: 84, size: 64, weight: 900, color: 'text', text: '¿En qué keywords\napareces realmente\nen Google?' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Lo sabrás en 30 seg →' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'TE DA' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Score SEO real' },
          { type: 'icon-list', x: 8, y: 42, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-google', text: 'Posiciones de tus keywords' },
            { icon: 'mdi-trending-up', text: 'Cambios diarios + alertas' },
            { icon: 'mdi-eye', text: 'Quién te roba tráfico' },
            { icon: 'mdi-file-export', text: 'Reportes PDF para el cliente' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'VS SEMRUSH' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 180, weight: 900, color: 'accent', text: '1/10' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'del precio. Mismas métricas core.' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Pega\ntu dominio' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: '5 keywords gratis. Sin cuenta. Sin tarjeta.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-magnify', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'rankit.mx' }
        ]
      }
    ]
  },
  {
    id: 'cometax-consultoria',
    name: 'ConsultorIA — pitch',
    description: 'Consultor IA: pídele estrategia de negocio MX y te responde con plan accionable. 4 slides.',
    thumbColor: '#a855f7',
    presetKey: 'cosmic',
    sizeKey: 'post',
    slides: [
      {
        templateId: 'cosmic-quote',
        layers: [
          { type: 'comet-trail', x: 70, y: 18, size: 60, opacity: 0.8 },
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'CONSULTORIA · IA' },
          { type: 'text', x: 8, y: 48, w: 84, size: 64, weight: 900, color: 'text', text: 'Un consultor de\nnegocios IA\nentrenado en MX' },
          { type: 'text', x: 8, y: 88, size: 24, weight: 600, color: 'accent', text: 'Disponible 24/7 →' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'text', x: 8, y: 10, size: 22, weight: 700, color: 'muted', text: 'TE RESUELVE' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Lo que un consultor\ncobra en $50,000' },
          { type: 'icon-list', x: 8, y: 45, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-bullseye-arrow', text: 'Define tu nicho y buyer persona' },
            { icon: 'mdi-chart-bar', text: 'Sugiere precios MX por benchmark' },
            { icon: 'mdi-rocket-launch', text: 'Plan 90 días con KPIs' },
            { icon: 'mdi-file-tree', text: 'Estructura legal/fiscal MX recomendada' }
          ] }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'gradient-blob', x: 80, y: 25, size: 55, opacity: 0.5 },
          { type: 'text', x: 50, y: 30, align: 'center', size: 26, weight: 700, color: 'muted', text: 'VS CONSULTOR HUMANO' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 200, weight: 900, color: 'accent', text: '99%' },
          { type: 'text', x: 50, y: 68, align: 'center', size: 28, weight: 500, color: 'text', text: 'más barato. Mismo framework.' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'text', x: 50, y: 28, align: 'center', size: 56, weight: 900, color: 'text', text: 'Pregúntale\nahora' },
          { type: 'text', x: 50, y: 50, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: '3 sesiones gratis. Después $99/mes ilimitado.' },
          { type: 'icon', x: 50, y: 70, size: 100, align: 'center', icon: 'mdi-robot-happy', color: 'accent' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 700, color: 'accent', text: 'consultor.cometax.mx' }
        ]
      }
    ]
  }
)

// ════════════════════════════════════════════════════════════════
// Showcase visual — demuestran waves, half-split, blur, brand logos
// ════════════════════════════════════════════════════════════════

CAROUSEL_PRESETS.push(
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
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'muted', text: 'PARA CREADORES' },
          { type: 'text', x: 8, y: 38, w: 84, size: 88, weight: 900, color: 'text', text: 'Diseña posts\nque parecen\nde agencia' },
          { type: 'text', x: 8, y: 70, w: 80, size: 26, weight: 500, color: 'muted', text: 'Sin Photoshop. Sin Canva Pro. Sin login.' },
          { type: 'wave-bottom', h: 28, opacity: 0.7 },
          { type: 'logo', x: 8, y: 92, size: 44, brand: 'cometax', text: 'CometaX' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 135, opacity: 0.3 },
          { type: 'shine-line', y: 25, opacity: 0.6 },
          { type: 'text', x: 8, y: 12, size: 22, weight: 700, color: 'accent', text: 'INCLUYE' },
          { type: 'text', x: 8, y: 22, size: 50, weight: 800, color: 'text', text: 'Estilos\nde verdad' },
          { type: 'icon-list', x: 8, y: 50, w: 84, gap: 7, size: 26, color: 'text', accent: 'accent', items: [
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
          { type: 'text', x: 50, y: 35, align: 'center', size: 64, weight: 900, color: 'text', text: 'Tu turno' },
          { type: 'text', x: 50, y: 52, w: 80, align: 'center', size: 28, weight: 500, color: 'muted', text: 'Abre el editor. Cambia el texto. Exporta. 2 minutos.' },
          { type: 'icon', x: 50, y: 72, size: 110, align: 'center', icon: 'mdi-rocket-launch', color: 'accent' },
          { type: 'logo', x: 50, y: 92, size: 40, align: 'center', brand: 'cometax' }
        ]
      }
    ]
  },
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
          { type: 'avatar', x: 50, y: 30, size: 180, align: 'center', src: '/people/02.svg' },
          { type: 'text', x: 50, y: 12, align: 'center', size: 22, weight: 700, color: 'muted', text: 'TESTIMONIO REAL' },
          { type: 'text', x: 50, y: 58, w: 84, align: 'center', size: 32, weight: 500, color: 'text', text: '"En 90 días pasé de cero a $50k/mes. Solo cambié los carruseles que publicaba."' },
          { type: 'text', x: 50, y: 82, align: 'center', size: 28, weight: 800, color: 'text', text: 'María R.' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 20, weight: 500, color: 'accent', text: 'Founder · Agencia digital MX' },
          { type: 'wave-bottom', h: 12, opacity: 0.5 }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.25 },
          { type: 'dots-pattern', gap: 28, opacity: 0.15 },
          { type: 'text', x: 50, y: 25, align: 'center', size: 26, weight: 700, color: 'muted', text: 'CRECIMIENTO REAL' },
          { type: 'text', x: 50, y: 50, align: 'center', size: 220, weight: 900, color: 'accent', text: '+847%' },
          { type: 'text', x: 50, y: 70, align: 'center', size: 28, weight: 500, color: 'text', text: 'engagement promedio en 30 días' },
          { type: 'wave-bottom', h: 18, opacity: 0.6, variant: 'soft' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'diagonal-band', y: 50, h: 14, angle: -8, text: 'Empieza gratis' },
          { type: 'text', x: 50, y: 25, align: 'center', size: 60, weight: 900, color: 'text', text: 'Sin agencia.\nSin diseñador.' },
          { type: 'avatar', x: 35, y: 75, size: 80, align: 'center', src: '/people/01.svg' },
          { type: 'avatar', x: 50, y: 75, size: 80, align: 'center', src: '/people/02.svg' },
          { type: 'avatar', x: 65, y: 75, size: 80, align: 'center', src: '/people/03.svg' },
          { type: 'text', x: 50, y: 90, align: 'center', size: 24, weight: 700, color: 'accent', text: '+2,400 creadores ya lo usan' }
        ]
      }
    ]
  },
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
          { type: 'text', x: 8, y: 18, size: 22, weight: 700, color: 'accent', text: 'EDICIÓN PRO' },
          { type: 'text', x: 8, y: 42, w: 84, size: 90, weight: 900, color: 'text', text: 'Geometría\nlimpia.\nIdeas claras.' },
          { type: 'text', x: 8, y: 80, w: 80, size: 26, weight: 500, color: 'muted', text: 'Plantillas con jerarquía visual de verdad.' },
          { type: 'shine-line', y: 88, opacity: 0.7 }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'diagonal-band', y: 18, h: 10, angle: -6, text: 'Disponible ya', fontSize: 22 },
          { type: 'text', x: 8, y: 38, size: 50, weight: 800, color: 'text', text: 'Para todo tipo\nde marca' },
          { type: 'icon-list', x: 8, y: 58, w: 84, gap: 6, size: 24, color: 'text', accent: 'accent', items: [
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
          { type: 'text', x: 50, y: 32, align: 'center', size: 64, weight: 900, color: 'text', text: 'Hazlo\ndiferente' },
          { type: 'text', x: 50, y: 56, w: 80, align: 'center', size: 26, weight: 500, color: 'muted', text: 'Tu marca merece más que una plantilla genérica.' },
          { type: 'icon', x: 50, y: 76, size: 100, align: 'center', icon: 'mdi-creation', color: 'accent2' },
          { type: 'wave-bottom', h: 14, opacity: 0.6 }
        ]
      }
    ]
  }
)

// ════════════════════════════════════════════════════════════════
// Designer-grade — fotos reales Unsplash + pravatar + 3D iso shapes
// ════════════════════════════════════════════════════════════════

CAROUSEL_PRESETS.push(
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
          { type: 'photo-bg', query: 'office,laptop,workspace', seed: 11, overlayAngle: 0, overlayOpacity: 0.55 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Edición #042 · Mensual' },
          { type: 'text', x: 8, y: 38, w: 84, size: 96, weight: 900, color: 'text', text: 'El estado\ndel SaaS\nen México.' },
          { type: 'text', x: 8, y: 70, w: 80, size: 26, weight: 500, color: 'muted', text: 'Datos, fundadores y números reales del último trimestre.' },
          { type: 'shine-line', y: 86, opacity: 0.7 },
          { type: 'text', x: 8, y: 92, size: 20, weight: 700, color: 'accent', text: 'COMETAX · INSIGHTS' }
        ]
      },
      {
        templateId: 'stat-card',
        layers: [
          { type: 'photo-bg', query: 'minimal,abstract,gradient', seed: 22, overlayAngle: 135, overlayOpacity: 0.7 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Dato del trimestre' },
          { type: 'big-number', x: 50, y: 50, align: 'center', size: 320, text: '847' },
          { type: 'text', x: 50, y: 70, align: 'center', size: 28, weight: 500, color: 'muted', text: 'SaaS mexicanos lanzados en Q1 2026' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 18, weight: 700, color: 'accent', text: 'FUENTE · COMETAX RESEARCH' }
        ]
      },
      {
        templateId: 'testimonial',
        layers: [
          { type: 'photo-bg', query: 'portrait,professional,woman', seed: 33, overlayAngle: 0, overlayOpacity: 0.6, overlayGrad: 'linear-gradient(0deg, #020617 0%, transparent 60%)' },
          { type: 'text', x: 8, y: 75, w: 84, size: 38, weight: 600, color: 'text', text: '"En 6 meses pasé de idea a $80,000 MXN/mes. Sin levantar capital."' },
          { type: 'text', x: 8, y: 90, size: 24, weight: 800, color: 'text', text: 'Andrea M.' },
          { type: 'text', x: 8, y: 95, size: 18, weight: 500, color: 'accent', text: 'Founder · Fintech CDMX' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'half-split', angle: 90, opacity: 0.3 },
          { type: 'iso-cube', x: 78, y: 30, size: 220 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Lo que aprendimos' },
          { type: 'text', x: 8, y: 26, size: 56, weight: 900, color: 'text', text: '3 patrones\nrepetidos.' },
          { type: 'icon-list', x: 8, y: 55, w: 60, gap: 8, size: 24, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-numeric-1-circle', text: 'Empezaron solos, no en equipo' },
            { icon: 'mdi-numeric-2-circle', text: 'Cobraron antes de pulir' },
            { icon: 'mdi-numeric-3-circle', text: 'Distribuyeron 10x más de lo que crearon' }
          ] }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'mountain,sunset,horizon', seed: 44, overlayAngle: 0, overlayOpacity: 0.5 },
          { type: 'glossy-ball', x: 80, y: 25, size: 140 },
          { type: 'text', x: 8, y: 50, w: 80, size: 80, weight: 900, color: 'text', text: 'Tu turno\nde aparecer\nen la lista.' },
          { type: 'text', x: 8, y: 80, size: 24, weight: 500, color: 'muted', text: 'Lee el reporte completo' },
          { type: 'text', x: 8, y: 88, size: 32, weight: 800, color: 'accent', text: 'cometax.mx/insights →' }
        ]
      }
    ]
  },
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
          { type: 'photo-bg', query: 'minimal,light,studio', seed: 55, overlayAngle: 180, overlayOpacity: 0.7 },
          { type: 'iso-card', x: 50, y: 45, size: 320, icon: 'mdi-rocket-launch', rotateY: -16, rotateX: 6 },
          { type: 'tag-pill', x: 50, y: 78, align: 'center', text: 'Disponible en MX' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 64, weight: 900, color: 'text', text: 'Gen 2.' },
          { type: 'text', x: 50, y: 95, align: 'center', size: 18, weight: 600, color: 'muted', text: 'Más rápido. Más simple. Más tuyo.' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'photo-bg', query: 'gradient,colorful,abstract', seed: 66, overlayOpacity: 0.85, overlayAngle: 90 },
          { type: 'iso-cube', x: 80, y: 25, size: 180 },
          { type: 'glossy-ball', x: 20, y: 75, size: 100 },
          { type: 'text', x: 8, y: 14, size: 22, weight: 700, color: 'accent', text: '— LO QUE CAMBIA' },
          { type: 'text', x: 8, y: 28, w: 70, size: 60, weight: 900, color: 'text', text: 'Velocidad,\ndiseño,\ndetalle.' },
          { type: 'icon-list', x: 8, y: 60, w: 80, gap: 8, size: 26, color: 'text', accent: 'accent', items: [
            { icon: 'mdi-flash', text: '4× más rápido en exportar' },
            { icon: 'mdi-palette', text: '12 paletas premium nuevas' },
            { icon: 'mdi-cube-outline', text: 'Formas 3D editables' }
          ] }
        ]
      },
      {
        templateId: 'testimonial',
        layers: [
          { type: 'photo-bg', query: 'portrait,man,beard,creative', seed: 77, overlayAngle: 0, overlayOpacity: 0.7, overlayGrad: 'linear-gradient(0deg, #0a0e1a 0%, transparent 50%)' },
          { type: 'tag-pill', x: 8, y: 12, text: 'Tester · Beta gen 2' },
          { type: 'text', x: 8, y: 70, w: 84, size: 36, weight: 500, color: 'text', text: '"Lo probé 30 minutos y borré mi suscripción de Canva."' },
          { type: 'text', x: 8, y: 88, size: 26, weight: 800, color: 'text', text: 'Diego R.' },
          { type: 'text', x: 8, y: 93, size: 18, weight: 500, color: 'accent', text: 'Diseñador · Studio Monterrey' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'aurora,northern,lights,purple', seed: 88, overlayOpacity: 0.6 },
          { type: 'glossy-ball', x: 50, y: 30, size: 180 },
          { type: 'text', x: 50, y: 60, align: 'center', size: 72, weight: 900, color: 'text', text: 'Pruébalo' },
          { type: 'text', x: 50, y: 75, w: 80, align: 'center', size: 24, weight: 500, color: 'muted', text: 'Sin tarjeta. Sin login. 100% en tu navegador.' },
          { type: 'text', x: 50, y: 88, align: 'center', size: 28, weight: 800, color: 'accent', text: 'cometax.mx/carousel' }
        ]
      }
    ]
  },
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
          { type: 'photo-bg', query: 'team,office,collaboration', seed: 91, overlayOpacity: 0.65 },
          { type: 'tag-pill', x: 8, y: 12, text: 'Buscamos talento' },
          { type: 'text', x: 8, y: 38, w: 84, size: 110, weight: 900, color: 'text', text: 'Únete\nal equipo.' },
          { type: 'text', x: 8, y: 75, w: 80, size: 26, weight: 500, color: 'muted', text: 'Posiciones abiertas en ingeniería, diseño y producto.' },
          { type: 'text', x: 8, y: 92, size: 22, weight: 800, color: 'accent', text: 'COMETAX · CAREERS' }
        ]
      },
      {
        templateId: 'feature-list',
        layers: [
          { type: 'photo-bg', query: 'workspace,laptop,cafe,minimal', seed: 92, overlayOpacity: 0.85, overlayAngle: 135 },
          { type: 'iso-card', x: 78, y: 32, size: 200, icon: 'mdi-laptop' },
          { type: 'tag-pill', x: 8, y: 14, text: 'Por qué unirte' },
          { type: 'text', x: 8, y: 28, w: 60, size: 54, weight: 900, color: 'text', text: 'Trabajo\ncomo debe ser.' },
          { type: 'icon-list', x: 8, y: 56, w: 60, gap: 7, size: 24, color: 'text', accent: 'accent', items: [
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
          { type: 'photo-bg', query: 'portrait,professional,smiling', seed: 93, overlayOpacity: 0.55 },
          { type: 'avatar', x: 50, y: 28, size: 160, align: 'center', src: 'https://i.pravatar.cc/300?img=15' },
          { type: 'text', x: 50, y: 12, align: 'center', size: 20, weight: 800, color: 'accent', text: 'TEAM · CTO' },
          { type: 'text', x: 50, y: 56, w: 84, align: 'center', size: 32, weight: 500, color: 'text', text: '"Es el lugar donde finalmente puedo trabajar como ingeniero senior, sin reuniones inútiles."' },
          { type: 'text', x: 50, y: 84, align: 'center', size: 26, weight: 800, color: 'text', text: 'Roberto K.' },
          { type: 'text', x: 50, y: 90, align: 'center', size: 18, weight: 500, color: 'accent', text: 'CTO · 4 años en CometaX' }
        ]
      },
      {
        templateId: 'cta-final',
        layers: [
          { type: 'photo-bg', query: 'sunrise,window,morning,light', seed: 94, overlayOpacity: 0.5 },
          { type: 'glossy-ball', x: 70, y: 30, size: 160 },
          { type: 'text', x: 8, y: 50, w: 80, size: 60, weight: 900, color: 'text', text: 'Aplica\nantes del 30.' },
          { type: 'text', x: 8, y: 80, size: 22, weight: 500, color: 'muted', text: 'Mandamos respuesta a todos. Promesa.' },
          { type: 'text', x: 8, y: 90, size: 28, weight: 800, color: 'accent', text: 'cometax.mx/jobs →' }
        ]
      }
    ]
  }
)

export function findPreset(id) {
  return CAROUSEL_PRESETS.find(p => p.id === id)
}
