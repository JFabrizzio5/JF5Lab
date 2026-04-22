import bcrypt
from core.pin_constant import PIN_HASH_HARDCODED


def verify_pin(plain: str) -> bool:
    if not plain or len(plain) != 8 or not plain.isdigit():
        return False
    return bcrypt.checkpw(plain.encode(), PIN_HASH_HARDCODED.encode())
