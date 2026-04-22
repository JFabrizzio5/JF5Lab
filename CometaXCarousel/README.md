# CometaX Carousel

Generador de carruseles para Instagram. Vue 3 + Vite, 100% client-side.

## Stack

- Vue 3.5 (Composition API + `<script setup>`)
- Vite 6 + Pinia + Vue Router
- `html-to-image` para export PNG/JPG
- `jszip` para empaquetar slides
- `@mdi/font` (sin emojis)
- Nginx alpine en producción

## Características

- 10 plantillas SVG editables (quote, lista, stat, code, before/after, testimonial, launch, tutorial, meme, CTA)
- 5 paletas (Cosmic, Light, Sunset, Midnight, Forest) + colores custom
- 3 tamaños IG (post 4:5, square 1:1, story 9:16)
- Logo + handle persistentes cross-slides
- Reorder, duplicar, eliminar slides
- Export slide individual o ZIP completo numerado
- Sin login, sin backend, datos jamás salen del navegador

## Desarrollo

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

## Producción (Docker)

```bash
docker compose up -d --build
# http://localhost:3070
```

Sirve build estático Nginx con gzip + cache headers.

## Puerto

`3070` (no colisiona con: 3001 Editorial, 3002 RentaFacil, 3005 ServiLink, 3010 EduLink, 3015 NegocioOS, 3020 SalonOS, 3025 ConventionOS, 3030 RentaMe, 3035 HubOS, 3040 StockLink, 3045 PulsoMX, 3050 NotaMX, 3055 AgendaPro, 3060 PorCobrar, 3065 HolaClaude).

## Estructura

```
frontend/
├── src/
│   ├── components/        # SlideCanvas, TemplatePicker, BrandPanel, LayerEditor, SlideStrip, ExportModal
│   ├── views/             # HomeView, EditorView, PricingView
│   ├── stores/carousel.js # Pinia state
│   ├── templates/index.js # 10 plantillas + 5 paletas + 3 tamaños
│   ├── router/index.js
│   ├── assets/styles.css  # CSS vars marca CometaX
│   ├── App.vue
│   └── main.js
├── public/favicon.svg     # marca cometa
├── package.json
├── vite.config.js
└── index.html
```

## Roadmap

- [ ] Templates extra: poll IG, infografía, calendar grid, comparison table
- [ ] Persistencia local (IndexedDB) — guardar diseños
- [ ] Stripe MX para plan Pro (sin marca CometaX, slides ilimitados)
- [ ] Subir foto y aplicar máscaras
- [ ] Animaciones para Reels (export MP4 vía ffmpeg WASM)
- [ ] AI: generar copy de slides desde un prompt

## Marca

Brand tokens (sincronizados con hub CometaX):

```
Gradiente:  #6366f1 → #a855f7
BG dark:    #0a0e1a
Card:       #1e293b
Accent:     #818cf8 / #c084fc
Font:       -apple-system, Inter
Motif:      cola de cometa (logo SVG)
```
