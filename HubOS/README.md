# HubOS

CRM + CMS + WhatsApp (Evolution API multi-sesión) + Armador de plantillas.
Sigue el patrón CometaX Microservices (FastAPI + Vue 3 + PostgreSQL).

## Puertos

| Servicio           | Puerto |
|--------------------|--------|
| Frontend (nginx)   | 3035   |
| Backend (FastAPI)  | 8075   |
| Postgres (interno) | 5432   |

No colisiona con: SalonOS (3020/8050), NegocioOS (3015/8041), ConventionOS (3025/8060), RentaMe (3030/8070), EduLink (3010), RentaFacil (3002), ServiLink (3005), Editorial (3001), Hub (8888).

## Levantar

```bash
cd /root/CometaXMicroservices/HubOS
docker compose up -d --build
```

El seed crea:
- Workspace demo: `hubos-demo`
- Usuario: `admin@hubos.dev` / `admin123`
- Pipeline "Ventas" con etapas pre-configuradas
- 3 contactos + 4 deals de ejemplo
- 3 plantillas starter (soporte, presentación, doc técnica)

## Evolution API

Configura en `docker-compose.yml` o con variables de entorno:

```bash
EVOLUTION_API_URL=http://host:8080     # URL de tu Evolution
EVOLUTION_API_KEY=tu_api_key
EVOLUTION_WEBHOOK_BASE=http://hubos_backend:8075   # cómo Evolution nos llega
```

Cada agente crea su propia instance desde `Chat → +`. Al crear, HubOS llama a
`POST /instance/create` con un `instanceName` único (`hubos_<ws>_<user>_<rand>`) y
registra un webhook en `/api/chat/webhook/{instance_name}`. El QR aparece en la
UI; cuando escanea, la sesión pasa a `connected` y los mensajes entrantes van al
endpoint correcto vía webhook.

## Módulos backend

- `routers/auth.py` — registro + login, devuelve JWT con `workspace_id`
- `routers/contacts.py` — CRUD CRM
- `routers/deals.py` — pipelines, deals, mover de etapa
- `routers/content.py` — CMS (páginas / posts / snippets), endpoint público
- `routers/templates.py` — constructor de plantillas con variables `{{token}}`
- `routers/chat.py` — sesiones Evolution, conversaciones, mensajes, WebSocket
- `evolution_client.py` — wrapper httpx del Evolution API

## Componentes frontend reutilizables

- `AppSidebar.vue` — sidebar global (nav + usuario)
- `DataTable.vue` — tabla con slots por columna
- `FormField.vue` — input / textarea / select unificado
- `Modal.vue` — modal con footer slot
- `BlockEditor.vue` — editor de bloques (heading / text / callout / code / image / divider)

## Landing

`/` → `LandingView.vue` con parallax 3D: lata "HubOS" renderizada en CSS puro,
layers con mousemove tracking, orbs con blur, particles. Tailwind vía CDN,
iconos vía Lucide CDN. Sin emojis.

## URLs útiles

- App: `http://localhost:3035`
- API: `http://localhost:8075/health`
- Swagger: `http://localhost:8075/docs`
- CMS público: `GET /api/content/public/{workspace_slug}/{slug}`

## Dev local sin Docker

```bash
# backend
cd backend
pip install -r requirements.txt
DB_HOST=localhost uvicorn main:app --reload --port 8075

# frontend
cd frontend
npm install
npm run dev
```
