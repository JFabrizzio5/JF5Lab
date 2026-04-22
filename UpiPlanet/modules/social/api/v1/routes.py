from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_sql_db
from modules.social.models.models import User, Post, Comment, Like, Follow
from modules.social.services.auth import hash_password, verify_password, issue_token, decode_token
from modules.social.services.demo import ensure_seed

router = APIRouter()


class RegisterIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    display_name: str = Field(..., min_length=2, max_length=80)
    password: str = Field(..., min_length=6, max_length=120)
    bio: str | None = Field(None, max_length=280)
    avatar_icon: str | None = Field(None, max_length=40)


class LoginIn(BaseModel):
    username: str
    password: str


class PostIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    mood_icon: str | None = Field(None, max_length=40)


class CommentIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


async def _current_user(authorization: str | None = Header(None), db: AsyncSession = Depends(get_sql_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "token requerido")
    uid = decode_token(authorization.removeprefix("Bearer ").strip())
    if not uid:
        raise HTTPException(401, "token invalido")
    u = (await db.execute(select(User).where(User.id == uid))).scalar_one_or_none()
    if not u:
        raise HTTPException(401, "usuario inexistente")
    return u


def _user_card(u: User) -> dict:
    return {
        "id": str(u.id),
        "username": u.username,
        "display_name": u.display_name,
        "bio": u.bio,
        "avatar_icon": u.avatar_icon,
    }


@router.post("/demo/seed")
async def demo_seed(db: AsyncSession = Depends(get_sql_db)):
    return await ensure_seed(db)


@router.post("/auth/register")
async def register(body: RegisterIn, db: AsyncSession = Depends(get_sql_db)):
    existing = (await db.execute(select(User).where(User.username == body.username))).scalar_one_or_none()
    if existing:
        raise HTTPException(409, "username ocupado")
    u = User(
        username=body.username,
        display_name=body.display_name,
        bio=body.bio,
        avatar_icon=body.avatar_icon or "account-circle",
        password_hash=hash_password(body.password),
    )
    db.add(u)
    await db.commit()
    await db.refresh(u)
    return {"token": issue_token(u.id), "user": _user_card(u)}


@router.post("/auth/login")
async def login(body: LoginIn, db: AsyncSession = Depends(get_sql_db)):
    u = (await db.execute(select(User).where(User.username == body.username))).scalar_one_or_none()
    if not u or not verify_password(body.password, u.password_hash):
        raise HTTPException(401, "credenciales invalidas")
    return {"token": issue_token(u.id), "user": _user_card(u)}


@router.get("/auth/me")
async def me(user: User = Depends(_current_user)):
    return _user_card(user)


@router.get("/feed")
async def feed(limit: int = 30, db: AsyncSession = Depends(get_sql_db)):
    # Public feed — sin auth necesario para demo
    q = (
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .order_by(desc(Post.created_at))
        .limit(min(limit, 100))
    )
    rows = (await db.execute(q)).all()
    post_ids = [p.id for p, _ in rows]

    likes_q = await db.execute(
        select(Like.post_id, func.count(Like.id)).where(Like.post_id.in_(post_ids)).group_by(Like.post_id)
    )
    likes = {pid: n for pid, n in likes_q.all()}

    comments_q = await db.execute(
        select(Comment.post_id, func.count(Comment.id)).where(Comment.post_id.in_(post_ids)).group_by(Comment.post_id)
    )
    comments = {pid: n for pid, n in comments_q.all()}

    return [
        {
            "id": str(p.id),
            "content": p.content,
            "mood_icon": p.mood_icon,
            "created_at": p.created_at.isoformat(),
            "author": _user_card(u),
            "likes": likes.get(p.id, 0),
            "comments": comments.get(p.id, 0),
        }
        for p, u in rows
    ]


@router.post("/posts")
async def create_post(body: PostIn, user: User = Depends(_current_user), db: AsyncSession = Depends(get_sql_db)):
    p = Post(author_id=user.id, content=body.content, mood_icon=body.mood_icon)
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return {
        "id": str(p.id),
        "content": p.content,
        "mood_icon": p.mood_icon,
        "created_at": p.created_at.isoformat(),
        "author": _user_card(user),
        "likes": 0,
        "comments": 0,
    }


@router.post("/posts/{post_id}/like")
async def toggle_like(post_id: str, user: User = Depends(_current_user), db: AsyncSession = Depends(get_sql_db)):
    existing = (
        await db.execute(select(Like).where(Like.post_id == post_id, Like.user_id == user.id))
    ).scalar_one_or_none()
    if existing:
        await db.delete(existing)
        await db.commit()
        liked = False
    else:
        db.add(Like(post_id=post_id, user_id=user.id))
        await db.commit()
        liked = True
    total = (await db.execute(select(func.count(Like.id)).where(Like.post_id == post_id))).scalar_one()
    return {"liked": liked, "total": total}


@router.get("/posts/{post_id}/comments")
async def list_comments(post_id: str, db: AsyncSession = Depends(get_sql_db)):
    q = (
        select(Comment, User)
        .join(User, User.id == Comment.author_id)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
    )
    rows = (await db.execute(q)).all()
    return [
        {"id": str(c.id), "content": c.content, "created_at": c.created_at.isoformat(), "author": _user_card(u)}
        for c, u in rows
    ]


@router.post("/posts/{post_id}/comments")
async def add_comment(post_id: str, body: CommentIn, user: User = Depends(_current_user), db: AsyncSession = Depends(get_sql_db)):
    c = Comment(post_id=post_id, author_id=user.id, content=body.content)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return {"id": str(c.id), "content": c.content, "created_at": c.created_at.isoformat(), "author": _user_card(user)}


@router.get("/users/{username}")
async def user_profile(username: str, db: AsyncSession = Depends(get_sql_db)):
    u = (await db.execute(select(User).where(User.username == username))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "no existe")
    posts = (
        await db.execute(select(Post).where(Post.author_id == u.id).order_by(desc(Post.created_at)).limit(50))
    ).scalars().all()
    followers = (await db.execute(select(func.count(Follow.id)).where(Follow.followed_id == u.id))).scalar_one()
    following = (await db.execute(select(func.count(Follow.id)).where(Follow.follower_id == u.id))).scalar_one()
    return {
        "user": _user_card(u),
        "followers": followers,
        "following": following,
        "posts": [
            {
                "id": str(p.id),
                "content": p.content,
                "mood_icon": p.mood_icon,
                "created_at": p.created_at.isoformat(),
            }
            for p in posts
        ],
    }


@router.get("/users")
async def users_directory(q: str = "", db: AsyncSession = Depends(get_sql_db)):
    query = select(User).order_by(User.display_name).limit(40)
    if q:
        pat = f"%{q.lower()}%"
        query = select(User).where(
            func.lower(User.username).like(pat) | func.lower(User.display_name).like(pat)
        ).order_by(User.display_name).limit(40)
    rows = (await db.execute(query)).scalars().all()
    return [_user_card(u) for u in rows]
