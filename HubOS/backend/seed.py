"""Bootstrap data: demo workspace + admin user + starter templates."""
from database import SessionLocal, engine, Base
import models
from auth import hash_password

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        if db.query(models.User).count() > 0:
            print("[seed] ya hay datos — skip")
            return

        ws = models.Workspace(name="HubOS Demo", slug="hubos-demo", plan="pro")
        db.add(ws)
        db.flush()

        admin = models.User(
            workspace_id=ws.id,
            email="admin@hubos.dev",
            password_hash=hash_password("admin123"),
            name="Admin Demo",
            role="owner",
        )
        db.add(admin)

        pipe = models.Pipeline(
            workspace_id=ws.id,
            name="Ventas",
            stages=["Nuevo", "Contactado", "Propuesta", "Negociación", "Ganado", "Perdido"],
        )
        db.add(pipe)
        db.flush()

        # Sample contacts
        contacts = [
            models.Contact(workspace_id=ws.id, owner_id=admin.id, name="María López", email="maria@acme.mx", phone="5215512345001", company="Acme", source="manual"),
            models.Contact(workspace_id=ws.id, owner_id=admin.id, name="Carlos Ruiz", email="carlos@globex.mx", phone="5215512345002", company="Globex", source="whatsapp"),
            models.Contact(workspace_id=ws.id, owner_id=admin.id, name="Ana Torres", email="ana@initech.mx", phone="5215512345003", company="Initech", source="web"),
        ]
        for c in contacts:
            db.add(c)
        db.flush()

        # Sample deals across stages
        for i, (stage, title, value) in enumerate([
            ("Nuevo", "Licencia anual Acme", 45000),
            ("Contactado", "Onboarding Globex", 120000),
            ("Propuesta", "Integración Initech", 78000),
            ("Ganado", "Expansión Acme", 300000),
        ]):
            db.add(models.Deal(
                workspace_id=ws.id, pipeline_id=pipe.id,
                contact_id=contacts[i % len(contacts)].id,
                title=title, value=value, stage=stage,
                status="won" if stage == "Ganado" else "open",
                owner_id=admin.id,
            ))

        # Starter templates
        db.add(models.Template(
            workspace_id=ws.id, created_by=admin.id,
            name="Respuesta de bienvenida",
            category="support",
            description="Plantilla para recibir un ticket nuevo",
            variables=[
                {"key": "customer_name", "label": "Nombre del cliente", "default": "Cliente"},
                {"key": "agent_name", "label": "Nombre del agente", "default": "Soporte"},
            ],
            blocks=[
                {"type": "heading", "content": "Hola {{customer_name}}"},
                {"type": "text", "content": "Gracias por escribirnos. Soy {{agent_name}} y voy a ayudarte con tu caso."},
                {"type": "text", "content": "¿Podrías darme más detalles del problema que estás experimentando?"},
            ],
        ))
        db.add(models.Template(
            workspace_id=ws.id, created_by=admin.id,
            name="Presentación comercial",
            category="presentation",
            description="Slides introductorias para prospectos",
            variables=[
                {"key": "company", "label": "Empresa", "default": "Tu Empresa"},
                {"key": "value_prop", "label": "Propuesta de valor", "default": ""},
            ],
            blocks=[
                {"type": "heading", "content": "{{company}}"},
                {"type": "text", "content": "{{value_prop}}"},
                {"type": "callout", "content": "Agendemos una demo"},
            ],
        ))
        db.add(models.Template(
            workspace_id=ws.id, created_by=admin.id,
            name="Documentación técnica — API",
            category="tech_doc",
            description="Esqueleto para documentar un endpoint",
            variables=[
                {"key": "endpoint", "label": "Endpoint", "default": "/api/..."},
                {"key": "method", "label": "Método HTTP", "default": "GET"},
            ],
            blocks=[
                {"type": "heading", "content": "{{method}} {{endpoint}}"},
                {"type": "text", "content": "Descripción del endpoint."},
                {"type": "code", "content": "curl -X {{method}} https://api.tudominio.com{{endpoint}}"},
                {"type": "heading", "content": "Parámetros"},
                {"type": "text", "content": "Listar parámetros..."},
            ],
        ))

        # Sample content
        db.add(models.Content(
            workspace_id=ws.id, author_id=admin.id,
            kind="page", title="Bienvenido a HubOS", slug="bienvenido",
            status="published",
            blocks=[
                {"type": "heading", "content": "Bienvenido"},
                {"type": "text", "content": "Este es tu CMS. Edita los bloques para personalizar el contenido."},
            ],
        ))

        db.commit()
        print("[seed] demo listo. Usuario: admin@hubos.dev / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    run()
