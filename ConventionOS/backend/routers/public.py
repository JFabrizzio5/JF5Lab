from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import json

router = APIRouter(prefix="/public", tags=["public"])


def full_convention_dict(c: models.Convention, db: Session):
    stages = db.query(models.Stage).filter(
        models.Stage.convention_id == c.id,
        models.Stage.is_active == True
    ).all()
    sessions = db.query(models.Session).filter(
        models.Session.convention_id == c.id,
        models.Session.is_active == True
    ).order_by(models.Session.start_time).all()
    speakers = db.query(models.Speaker).filter(
        models.Speaker.convention_id == c.id,
        models.Speaker.is_active == True
    ).all()
    stands = db.query(models.Stand).filter(
        models.Stand.convention_id == c.id
    ).all()
    sponsors = db.query(models.Sponsor).filter(
        models.Sponsor.convention_id == c.id,
        models.Sponsor.is_active == True
    ).all()
    ticket_types = db.query(models.TicketType).filter(
        models.TicketType.convention_id == c.id,
        models.TicketType.is_active == True
    ).all()
    tournaments = db.query(models.Tournament).filter(
        models.Tournament.convention_id == c.id,
        models.Tournament.is_active == True
    ).all()

    stages_out = []
    for s in stages:
        stage_sessions = [sess for sess in sessions if sess.stage_id == s.id]
        sessions_out = []
        for sess in stage_sessions:
            sessions_out.append({
                "id": sess.id,
                "title": sess.title,
                "description": sess.description,
                "session_type": sess.session_type,
                "start_time": sess.start_time.isoformat() if sess.start_time else None,
                "end_time": sess.end_time.isoformat() if sess.end_time else None,
                "tags_json": sess.tags_json,
                "speaker": {
                    "id": sess.speaker.id,
                    "name": sess.speaker.name,
                    "photo_url": sess.speaker.photo_url,
                    "title": sess.speaker.title,
                    "company": sess.speaker.company,
                } if sess.speaker else None,
            })
        stages_out.append({
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "capacity": s.capacity,
            "color": s.color,
            "location_in_venue": s.location_in_venue,
            "stream_url": s.stream_url,
            "sessions": sessions_out,
        })

    return {
        "id": c.id,
        "name": c.name,
        "slug": c.slug,
        "edition": c.edition,
        "tagline": c.tagline,
        "description": c.description,
        "logo_url": c.logo_url,
        "cover_url": c.cover_url,
        "banner_url": c.banner_url,
        "theme_color": c.theme_color,
        "accent_color": c.accent_color,
        "bg_color": c.bg_color,
        "font_style": c.font_style,
        "venue_name": c.venue_name,
        "address": c.address,
        "city": c.city,
        "lat": c.lat,
        "lng": c.lng,
        "start_date": c.start_date.isoformat() if c.start_date else None,
        "end_date": c.end_date.isoformat() if c.end_date else None,
        "status": c.status,
        "max_attendees": c.max_attendees,
        "website": c.website,
        "social_json": c.social_json,
        "rules_text": c.rules_text,
        "stripe_onboarding_complete": c.stripe_onboarding_complete,
        "platform_fee_percent": c.platform_fee_percent,
        "stages": stages_out,
        "speakers": [
            {
                "id": sp.id,
                "name": sp.name,
                "bio": sp.bio,
                "photo_url": sp.photo_url,
                "title": sp.title,
                "company": sp.company,
                "twitter": sp.twitter,
                "is_keynote": sp.is_keynote,
            }
            for sp in speakers
        ],
        "stands": [
            {
                "id": st.id,
                "number": st.number,
                "name": st.name,
                "category": st.category,
                "size": st.size,
                "price": st.price,
                "status": st.status,
                "x_pos": st.x_pos,
                "y_pos": st.y_pos,
                "width": st.width,
                "height": st.height,
                "description": st.description,
            }
            for st in stands
        ],
        "sponsors": [
            {
                "id": sp.id,
                "name": sp.name,
                "logo_url": sp.logo_url,
                "website": sp.website,
                "tier": sp.tier,
            }
            for sp in sponsors
        ],
        "ticket_types": [
            {
                "id": tt.id,
                "name": tt.name,
                "description": tt.description,
                "price": tt.price,
                "quantity_total": tt.quantity_total,
                "quantity_sold": tt.quantity_sold,
                "benefits_json": tt.benefits_json,
                "color": tt.color,
                "sale_start": tt.sale_start.isoformat() if tt.sale_start else None,
                "sale_end": tt.sale_end.isoformat() if tt.sale_end else None,
            }
            for tt in ticket_types
        ],
        "tournaments": [
            {
                "id": t.id,
                "name": t.name,
                "game": t.game,
                "format": t.format,
                "max_participants": t.max_participants,
                "participants_count": t.participants_count,
                "prize_pool": t.prize_pool,
                "prize_description": t.prize_description,
                "entry_fee": t.entry_fee,
                "start_time": t.start_time.isoformat() if t.start_time else None,
                "status": t.status,
            }
            for t in tournaments
        ],
    }


@router.get("/conventions")
def list_public_conventions(db: Session = Depends(get_db)):
    convs = db.query(models.Convention).filter(
        models.Convention.status.in_(["published", "live"]),
        models.Convention.is_active == True
    ).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "edition": c.edition,
            "tagline": c.tagline,
            "logo_url": c.logo_url,
            "cover_url": c.cover_url,
            "theme_color": c.theme_color,
            "accent_color": c.accent_color,
            "city": c.city,
            "start_date": c.start_date.isoformat() if c.start_date else None,
            "end_date": c.end_date.isoformat() if c.end_date else None,
            "status": c.status,
        }
        for c in convs
    ]


@router.get("/convention/{slug}")
def get_public_convention(slug: str, db: Session = Depends(get_db)):
    c = db.query(models.Convention).filter(
        models.Convention.slug == slug,
        models.Convention.is_active == True
    ).first()
    if not c:
        raise HTTPException(404, "Convention not found")
    return full_convention_dict(c, db)
