import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from database import get_db
import models
import auth as auth_utils
import anthropic

router = APIRouter(prefix="/rag", tags=["rag"])

_client: Optional[anthropic.Anthropic] = None


def get_client() -> Optional[anthropic.Anthropic]:
    global _client
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return None
    if _client is None:
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


class UserProfile(BaseModel):
    business_name: str = ""
    top_products: list = []
    low_stock_count: int = 0


class RAGRequest(BaseModel):
    query: str
    user_profile: Optional[UserProfile] = None


def build_context(db: Session) -> str:
    since_30 = datetime.utcnow() - timedelta(days=30)

    # Low stock products
    low_stock = db.query(models.Product).filter(
        models.Product.is_active == True,
        models.Product.stock < models.Product.min_stock,
    ).all()

    # Top selling products (last 30 days)
    top_rows = (
        db.query(
            models.Product.name,
            func.sum(models.SaleItem.quantity).label("qty"),
            func.sum(models.SaleItem.subtotal).label("rev"),
        )
        .join(models.SaleItem, models.SaleItem.product_id == models.Product.id)
        .join(models.Sale, models.Sale.id == models.SaleItem.sale_id)
        .filter(
            models.Sale.created_at >= since_30,
            models.Sale.status == models.SaleStatus.completed,
        )
        .group_by(models.Product.id, models.Product.name)
        .order_by(func.sum(models.SaleItem.quantity).desc())
        .limit(5)
        .all()
    )

    # Recent sales summary
    total_sales = (
        db.query(func.sum(models.Sale.total))
        .filter(
            models.Sale.created_at >= since_30,
            models.Sale.status == models.SaleStatus.completed,
        )
        .scalar() or 0
    )
    sales_count = (
        db.query(func.count(models.Sale.id))
        .filter(
            models.Sale.created_at >= since_30,
            models.Sale.status == models.SaleStatus.completed,
        )
        .scalar() or 0
    )

    # RAG tips
    tips = db.query(models.RAGContext).filter_by(content_type=models.ContentType.tip).limit(3).all()

    context_parts = []

    if low_stock:
        context_parts.append("PRODUCTOS CON BAJO INVENTARIO:")
        for p in low_stock:
            context_parts.append(f"  - {p.name} (SKU: {p.sku}): {p.stock} unidades (mínimo: {p.min_stock})")

    if top_rows:
        context_parts.append("\nPRODUCTOS MÁS VENDIDOS (últimos 30 días):")
        for r in top_rows:
            context_parts.append(f"  - {r.name}: {int(r.qty)} unidades vendidas, ${round(r.rev, 2)} ingresos")

    context_parts.append(f"\nRESUMEN DE VENTAS (últimos 30 días):")
    context_parts.append(f"  - Total ventas: {sales_count}")
    context_parts.append(f"  - Ingresos totales: ${round(total_sales, 2)}")

    if tips:
        context_parts.append("\nCONSEJOS DE NEGOCIO:")
        for t in tips:
            context_parts.append(f"  - {t.content}")

    return "\n".join(context_parts)


def ask_rag(query: str, context: str) -> str:
    client = get_client()
    if not client:
        return "RAG no disponible: configura ANTHROPIC_API_KEY en el entorno."
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=f"""Eres un asesor de negocios experto. Analiza los datos del negocio del usuario y responde en español de forma concisa y práctica.

DATOS DEL NEGOCIO:
{context}""",
            messages=[{"role": "user", "content": query}],
        )
        return message.content[0].text
    except Exception as e:
        return f"Error al consultar el asistente: {str(e)}"


@router.post("/ask")
def ask(
    req: RAGRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    context = build_context(db)
    if req.user_profile and req.user_profile.business_name:
        context = f"Negocio: {req.user_profile.business_name}\n\n" + context
    response = ask_rag(req.query, context)
    return {"query": req.query, "response": response, "context_preview": context[:300]}


# Re-export SaleStatus for use in this module
from models import SaleStatus  # noqa
