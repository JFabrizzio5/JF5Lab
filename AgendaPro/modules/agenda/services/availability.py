"""Availability slot calculation — respeta rules + exceptions + appointments existentes."""
from __future__ import annotations
from datetime import datetime, timedelta, date as DateType, time
from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from modules.agenda.models import (
    Staff, Service, AvailabilityRule, AvailabilityException, Appointment,
)


SLOT_INTERVAL_MIN = 15  # granularidad de slots


async def compute_slots(
    db: AsyncSession,
    service_id: UUID,
    date_from: DateType,
    date_to: DateType,
    staff_id: UUID | None = None,
) -> list[dict]:
    """Devuelve slots disponibles agrupados por fecha (ISO) para un servicio.

    Retorna: [{date: 'YYYY-MM-DD', slots: [{starts_at, ends_at, staff_id, staff_name}]}]
    """
    # 1. Servicio
    svc = (await db.execute(select(Service).where(Service.id == service_id))).scalar_one_or_none()
    if not svc:
        return []

    # 2. Staff elegible
    staff_q = select(Staff).where(Staff.active == True)  # noqa
    if staff_id:
        staff_q = staff_q.where(Staff.id == staff_id)
    elif svc.staff_ids:
        staff_q = staff_q.where(Staff.id.in_(svc.staff_ids))
    staff_list = (await db.execute(staff_q)).scalars().all()
    if not staff_list:
        return []

    staff_ids = [s.id for s in staff_list]
    staff_map = {s.id: s for s in staff_list}

    # 3. Rules
    rules_r = await db.execute(
        select(AvailabilityRule).where(
            AvailabilityRule.staff_id.in_(staff_ids),
            AvailabilityRule.active == True,  # noqa
        )
    )
    rules = rules_r.scalars().all()

    # 4. Exceptions en rango
    exc_r = await db.execute(
        select(AvailabilityException).where(
            AvailabilityException.staff_id.in_(staff_ids),
            AvailabilityException.date >= date_from,
            AvailabilityException.date <= date_to,
        )
    )
    exceptions = exc_r.scalars().all()

    # 5. Appointments en rango (no canceladas)
    dt_from = datetime.combine(date_from, time.min)
    dt_to = datetime.combine(date_to, time.max)
    appt_r = await db.execute(
        select(Appointment).where(
            Appointment.staff_id.in_(staff_ids),
            Appointment.starts_at >= dt_from,
            Appointment.starts_at <= dt_to,
            Appointment.status.in_(["pending_payment", "confirmed"]),
        )
    )
    appts = appt_r.scalars().all()

    duration = svc.duration_minutes
    buffer = svc.buffer_minutes or 0

    out_by_date: dict[str, list[dict]] = {}

    day = date_from
    while day <= date_to:
        wday = day.weekday()
        key = day.isoformat()
        out_by_date[key] = []

        for st in staff_list:
            # Blocks del staff este día
            blocks: list[tuple[time, time]] = []
            for r in rules:
                if r.staff_id == st.id and r.weekday == wday:
                    blocks.append((r.start_time, r.end_time))
            # Excepciones
            extras = []
            blocked_ranges: list[tuple[time, time]] = []
            for e in exceptions:
                if e.staff_id != st.id or e.date != day:
                    continue
                if e.kind == "extra" and e.start_time and e.end_time:
                    extras.append((e.start_time, e.end_time))
                elif e.kind == "blocked":
                    if e.start_time and e.end_time:
                        blocked_ranges.append((e.start_time, e.end_time))
                    else:
                        blocks = []  # día completo bloqueado
                        break
            blocks.extend(extras)

            # Appointments de este staff este día
            day_appts = [a for a in appts if a.staff_id == st.id and a.starts_at.date() == day]

            for bstart, bend in blocks:
                cursor = datetime.combine(day, bstart)
                block_end = datetime.combine(day, bend)
                while cursor + timedelta(minutes=duration) <= block_end:
                    slot_end = cursor + timedelta(minutes=duration + buffer)
                    # no en el pasado
                    if cursor < datetime.utcnow():
                        cursor += timedelta(minutes=SLOT_INTERVAL_MIN)
                        continue
                    # colisión con blocked_range
                    conflict = False
                    for br_s, br_e in blocked_ranges:
                        br_sd = datetime.combine(day, br_s)
                        br_ed = datetime.combine(day, br_e)
                        if cursor < br_ed and slot_end > br_sd:
                            conflict = True; break
                    if conflict:
                        cursor += timedelta(minutes=SLOT_INTERVAL_MIN); continue
                    # colisión con appointments
                    for a in day_appts:
                        if cursor < a.ends_at and slot_end > a.starts_at:
                            conflict = True; break
                    if conflict:
                        cursor += timedelta(minutes=SLOT_INTERVAL_MIN); continue

                    out_by_date[key].append({
                        "starts_at": cursor.isoformat(),
                        "ends_at": (cursor + timedelta(minutes=duration)).isoformat(),
                        "staff_id": str(st.id),
                        "staff_name": st.name,
                    })
                    cursor += timedelta(minutes=SLOT_INTERVAL_MIN)

        # orden por hora
        out_by_date[key].sort(key=lambda s: s["starts_at"])
        day += timedelta(days=1)

    return [{"date": d, "slots": s} for d, s in out_by_date.items()]


async def has_conflict(db: AsyncSession, staff_id: UUID, starts_at: datetime, ends_at: datetime,
                      exclude_id: UUID | None = None) -> bool:
    q = select(Appointment).where(
        Appointment.staff_id == staff_id,
        Appointment.starts_at < ends_at,
        Appointment.ends_at > starts_at,
        Appointment.status.in_(["pending_payment", "confirmed"]),
    )
    if exclude_id:
        q = q.where(Appointment.id != exclude_id)
    r = await db.execute(q)
    return r.scalars().first() is not None
