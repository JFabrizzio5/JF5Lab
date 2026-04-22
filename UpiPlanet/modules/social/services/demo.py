import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.social.models.models import User, Post, Comment, Like, Follow
from modules.social.services.auth import hash_password


DEMO_USERS = [
    {"username": "nova",     "display_name": "Nova Rivera",     "bio": "Explorando UpiPlanet desde el norte",   "icon": "rocket-launch"},
    {"username": "orion",    "display_name": "Orión Vega",      "bio": "Astrónomo amateur y cafeinado",         "icon": "star-four-points"},
    {"username": "lyra",     "display_name": "Lyra Méndez",     "bio": "Música espacial y senderos",            "icon": "music"},
    {"username": "kai",      "display_name": "Kai Nakamura",    "bio": "Diseño, UX y planetas lejanos",         "icon": "palette"},
    {"username": "mira",     "display_name": "Mira Holt",       "bio": "Comunidad y conexiones humanas",        "icon": "account-heart"},
    {"username": "atlas",    "display_name": "Atlas Pérez",     "bio": "Ingeniero de sistemas y café",          "icon": "earth"},
    {"username": "sol",      "display_name": "Sol Vargas",      "bio": "Fotografía urbana y amaneceres",        "icon": "white-balance-sunny"},
    {"username": "nebula",   "display_name": "Nébula Quinn",    "bio": "Curiosidad perpetua",                    "icon": "shimmer"},
]

DEMO_POSTS = [
    ("nova",   "Hoy UpiPlanet me recibió con un cielo morado perfecto. Quién más ve el atardecer?", "weather-sunset"),
    ("orion",  "Telescopio listo, la luna se ve increíble esta noche. Saludos desde el observatorio.", "telescope"),
    ("lyra",   "Nueva playlist para trabajar. Cada canción suena a galaxia.", "headphones"),
    ("kai",    "Terminé el rediseño del onboarding. Menos fricción, más magia.", "lightbulb-on"),
    ("mira",   "Red social sin drama, solo conversaciones reales. Gracias por construir esto en comunidad.", "heart"),
    ("atlas",  "Levanté un nuevo microservicio en minutos con CometaX. Esta cosa vuela.", "server"),
    ("sol",    "Probando una cámara vieja. La luz tiene memoria.", "camera"),
    ("nebula", "Pequeño reto del día: escribir algo creativo en menos de 100 palabras.", "pencil"),
    ("nova",   "Alguien más atrapado en un bucle de Anchorage -> mate -> código? No estás solo.", "cup"),
    ("orion",  "Dato del día: Júpiter tiene tormentas tan grandes que la Tierra cabe adentro.", "planet"),
]


async def ensure_seed(db: AsyncSession) -> dict:
    existing = (await db.execute(select(User).limit(1))).scalar_one_or_none()
    if existing:
        return {"seeded": False, "reason": "ya hay datos"}

    users = {}
    for u in DEMO_USERS:
        user = User(
            username=u["username"],
            display_name=u["display_name"],
            bio=u["bio"],
            avatar_icon=u["icon"],
            password_hash=hash_password("upiplanet"),
        )
        db.add(user)
        users[u["username"]] = user
    await db.flush()

    posts = []
    for author, content, mood in DEMO_POSTS:
        p = Post(author_id=users[author].id, content=content, mood_icon=mood)
        db.add(p)
        posts.append(p)
    await db.flush()

    # Random likes
    for p in posts:
        for u in random.sample(list(users.values()), k=random.randint(1, 5)):
            if u.id == p.author_id:
                continue
            db.add(Like(post_id=p.id, user_id=u.id))

    # Random comments
    comment_pool = [
        "Me encanta esto!",
        "Totalmente de acuerdo.",
        "Cuéntame más, me intriga.",
        "Ka-chow, justo lo que necesitaba hoy.",
        "Bienvenidos al planeta.",
        "Demasiado cierto.",
    ]
    for p in posts[:6]:
        for u in random.sample(list(users.values()), k=random.randint(1, 3)):
            db.add(Comment(post_id=p.id, author_id=u.id, content=random.choice(comment_pool)))

    # Some follows
    user_list = list(users.values())
    for u in user_list:
        targets = random.sample([x for x in user_list if x.id != u.id], k=random.randint(2, 4))
        for t in targets:
            db.add(Follow(follower_id=u.id, followed_id=t.id))

    await db.commit()
    return {"seeded": True, "users": len(users), "posts": len(posts)}
