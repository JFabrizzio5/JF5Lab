"""Motor transaccional de stock.

Aplica un Movement y ajusta StockLevel de forma atómica bajo RLS.
Reglas:
 - IN:           +qty en to_location
 - OUT/CONSUME:  -qty en from_location (falla si stock insuficiente y qty>0)
 - TRANSFER:     -qty en from, +qty en to
 - ADJUST:       set absoluto en to (o from si to=None)
 - RESERVE:      +reserved en from
 - RELEASE:      -reserved en from
 - RETURN:       +qty en to
"""
from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from modules.inventory.models import Item, StockLevel, Movement, Location, MovementKind


async def _get_or_create_level(db: AsyncSession, tenant_id: str, item_id: UUID, location_id: UUID) -> StockLevel:
    result = await db.execute(
        select(StockLevel).where(
            StockLevel.item_id == item_id,
            StockLevel.location_id == location_id,
        )
    )
    level = result.scalar_one_or_none()
    if not level:
        level = StockLevel(
            tenant_id=tenant_id, item_id=item_id, location_id=location_id,
            qty=Decimal("0"), reserved=Decimal("0"),
        )
        db.add(level)
        await db.flush()
    return level


async def apply_movement(
    db: AsyncSession,
    tenant_id: str,
    *,
    item_id: UUID,
    kind: str,
    qty: Decimal,
    from_location_id: UUID | None,
    to_location_id: UUID | None,
    reason: str | None = None,
    ref_type: str | None = None,
    ref_id: str | None = None,
    user_id: str | None = None,
    source_event: dict | None = None,
) -> Movement:
    item = (await db.execute(select(Item).where(Item.id == item_id))).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    qty = Decimal(str(qty))
    if qty <= 0 and kind != "ADJUST":
        raise HTTPException(status_code=400, detail="qty debe ser > 0 (excepto ADJUST)")

    if kind in ("OUT", "CONSUME", "TRANSFER", "RESERVE", "RELEASE") and not from_location_id:
        raise HTTPException(status_code=400, detail=f"{kind} requiere from_location_id")
    if kind in ("IN", "TRANSFER", "RETURN", "ADJUST") and not to_location_id:
        raise HTTPException(status_code=400, detail=f"{kind} requiere to_location_id")

    if from_location_id:
        src = await _get_or_create_level(db, tenant_id, item_id, from_location_id)
    if to_location_id:
        dst = await _get_or_create_level(db, tenant_id, item_id, to_location_id)

    if kind == "IN":
        dst.qty += qty
    elif kind == "OUT" or kind == "CONSUME":
        if src.qty - qty < 0:
            raise HTTPException(status_code=409, detail="Stock insuficiente")
        src.qty -= qty
    elif kind == "TRANSFER":
        if src.qty - qty < 0:
            raise HTTPException(status_code=409, detail="Stock insuficiente en origen")
        src.qty -= qty
        dst.qty += qty
    elif kind == "ADJUST":
        dst.qty = qty
    elif kind == "RETURN":
        dst.qty += qty
    elif kind == "RESERVE":
        if src.qty - src.reserved - qty < 0:
            raise HTTPException(status_code=409, detail="No hay stock disponible para reservar")
        src.reserved += qty
    elif kind == "RELEASE":
        src.reserved = max(Decimal("0"), src.reserved - qty)
    else:
        raise HTTPException(status_code=400, detail=f"Tipo de movimiento desconocido: {kind}")

    mv = Movement(
        tenant_id=tenant_id, item_id=item_id, from_location_id=from_location_id,
        to_location_id=to_location_id, qty=qty, kind=kind, reason=reason,
        ref_type=ref_type, ref_id=ref_id, user_id=user_id, source_event=source_event,
    )
    db.add(mv)
    await db.commit()
    await db.refresh(mv)
    return mv
