"""Idempotent seed script for NegocioOS demo data."""
from database import SessionLocal, engine, Base
import models
from auth import hash_password
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ── Users ────────────────────────────────────────────────────────────────────
def seed_users():
    demo_users = [
        {"email": "admin@negocio.mx", "name": "Administrador", "role": models.UserRole.admin, "business_name": "NegocioOS"},
        {"email": "dueno@negocio.mx", "name": "Dueño Demo", "role": models.UserRole.owner, "business_name": "Tienda Demo"},
        {"email": "cajero@negocio.mx", "name": "Cajero Demo", "role": models.UserRole.employee, "business_name": "Tienda Demo"},
    ]
    for u in demo_users:
        if not db.query(models.User).filter_by(email=u["email"]).first():
            db.add(models.User(
                email=u["email"],
                name=u["name"],
                password_hash=hash_password("demo123"),
                role=u["role"],
                business_name=u["business_name"],
                is_active=True,
            ))
    db.commit()

# ── Categories ────────────────────────────────────────────────────────────────
def seed_categories():
    cats = [
        {"name": "Electrónica", "color": "#6366f1"},
        {"name": "Ropa", "color": "#f97316"},
        {"name": "Alimentos", "color": "#22c55e"},
    ]
    for c in cats:
        if not db.query(models.Category).filter_by(name=c["name"]).first():
            db.add(models.Category(**c))
    db.commit()

# ── Products ──────────────────────────────────────────────────────────────────
def seed_products():
    cat_e = db.query(models.Category).filter_by(name="Electrónica").first()
    cat_r = db.query(models.Category).filter_by(name="Ropa").first()
    cat_a = db.query(models.Category).filter_by(name="Alimentos").first()

    products = [
        {"name": "Audífonos Bluetooth", "sku": "ELEC-001", "description": "Audífonos inalámbricos con cancelación de ruido", "category_id": cat_e.id, "price": 599.0, "cost": 320.0, "stock": 25, "min_stock": 5},
        {"name": "Cable USB-C", "sku": "ELEC-002", "description": "Cable USB-C de carga rápida 2m", "category_id": cat_e.id, "price": 149.0, "cost": 60.0, "stock": 3, "min_stock": 10},
        {"name": "Cargador Inalámbrico", "sku": "ELEC-003", "description": "Cargador Qi 15W compatible", "category_id": cat_e.id, "price": 399.0, "cost": 180.0, "stock": 12, "min_stock": 5},
        {"name": "Funda para Celular", "sku": "ELEC-004", "description": "Funda protectora universal", "category_id": cat_e.id, "price": 89.0, "cost": 30.0, "stock": 2, "min_stock": 8},
        {"name": "Playera Básica", "sku": "ROPA-001", "description": "Playera de algodón 100%", "category_id": cat_r.id, "price": 199.0, "cost": 80.0, "stock": 40, "min_stock": 10},
        {"name": "Pantalón Casual", "sku": "ROPA-002", "description": "Pantalón de mezclilla slim fit", "category_id": cat_r.id, "price": 549.0, "cost": 220.0, "stock": 15, "min_stock": 5},
        {"name": "Sudadera con Capucha", "sku": "ROPA-003", "description": "Sudadera unisex talla M-XL", "category_id": cat_r.id, "price": 349.0, "cost": 140.0, "stock": 4, "min_stock": 6},
        {"name": "Café Gourmet 250g", "sku": "ALIM-001", "description": "Café de especialidad tueste medio", "category_id": cat_a.id, "price": 129.0, "cost": 55.0, "stock": 30, "min_stock": 10},
        {"name": "Granola Artesanal", "sku": "ALIM-002", "description": "Granola con frutos secos 500g", "category_id": cat_a.id, "price": 89.0, "cost": 35.0, "stock": 1, "min_stock": 5},
        {"name": "Botella Reutilizable", "sku": "ALIM-003", "description": "Botella acero inoxidable 750ml", "category_id": cat_a.id, "price": 279.0, "cost": 110.0, "stock": 18, "min_stock": 5},
    ]
    for p in products:
        if not db.query(models.Product).filter_by(sku=p["sku"]).first():
            db.add(models.Product(**p))
    db.commit()

# ── Customers ────────────────────────────────────────────────────────────────
def seed_customers():
    customers = [
        {"name": "María García", "email": "maria@example.com", "phone": "555-1001", "notes": "Cliente frecuente"},
        {"name": "Juan Pérez", "email": "juan@example.com", "phone": "555-1002", "notes": "Prefiere pago con tarjeta"},
        {"name": "Ana López", "email": "ana@example.com", "phone": "555-1003", "notes": ""},
        {"name": "Carlos Ruiz", "email": "carlos@example.com", "phone": "555-1004", "notes": "Compras corporativas"},
        {"name": "Elena Torres", "email": "elena@example.com", "phone": "555-1005", "notes": "Cliente VIP"},
    ]
    for c in customers:
        if not db.query(models.Customer).filter_by(email=c["email"]).first():
            db.add(models.Customer(**c))
    db.commit()

# ── Sales ────────────────────────────────────────────────────────────────────
def seed_sales():
    if db.query(models.Sale).count() >= 15:
        return

    cashier = db.query(models.User).filter_by(email="cajero@negocio.mx").first()
    products = db.query(models.Product).all()
    customers = db.query(models.Customer).all()
    methods = [models.PaymentMethod.cash, models.PaymentMethod.card, models.PaymentMethod.transfer]

    for i in range(15):
        days_ago = random.randint(0, 29)
        sale_date = datetime.utcnow() - timedelta(days=days_ago)
        num_items = random.randint(1, 3)
        chosen = random.sample(products, min(num_items, len(products)))
        customer = random.choice(customers + [None])

        sale = models.Sale(
            user_id=cashier.id,
            customer_id=customer.id if customer else None,
            subtotal=0,
            tax=0,
            total=0,
            payment_method=random.choice(methods),
            status=models.SaleStatus.completed,
            created_at=sale_date,
        )
        db.add(sale)
        db.flush()

        subtotal = 0.0
        for prod in chosen:
            qty = random.randint(1, 3)
            item_sub = prod.price * qty
            subtotal += item_sub
            db.add(models.SaleItem(
                sale_id=sale.id,
                product_id=prod.id,
                quantity=qty,
                unit_price=prod.price,
                subtotal=item_sub,
            ))
            db.add(models.InventoryLog(
                product_id=prod.id,
                change_qty=-qty,
                reason=models.InventoryReason.sale,
                reference_id=sale.id,
                created_at=sale_date,
            ))

        tax = round(subtotal * 0.16, 2)
        sale.subtotal = round(subtotal, 2)
        sale.tax = tax
        sale.total = round(subtotal + tax, 2)

        if customer:
            customer.total_purchases += sale.total

    db.commit()

# ── RAG Tips ─────────────────────────────────────────────────────────────────
def seed_rag_tips():
    tips = [
        "Mantén siempre un stock mínimo de seguridad para evitar quiebres de inventario en productos de alta rotación.",
        "Analiza tus ventas semanalmente para identificar tendencias y ajustar pedidos a tiempo.",
        "Ofrece descuentos en productos de baja rotación para liberar capital de inventario.",
        "Un cliente fidelizado gasta en promedio 67% más que uno nuevo. Implementa un programa de lealtad.",
        "Registra los costos de tus productos correctamente para calcular márgenes reales.",
    ]
    for tip in tips:
        if not db.query(models.RAGContext).filter_by(embedding_text=tip[:50]).first():
            db.add(models.RAGContext(
                content_type=models.ContentType.tip,
                content=tip,
                embedding_text=tip[:50],
            ))
    db.commit()


if __name__ == "__main__":
    print("Seeding database...")
    seed_users()
    seed_categories()
    seed_products()
    seed_customers()
    seed_sales()
    seed_rag_tips()
    db.close()
    print("Seed completado.")
