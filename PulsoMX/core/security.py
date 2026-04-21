import os
import jwt
from typing import Optional, Dict
from fastapi import HTTPException, status
import logging

logger = logging.getLogger("security")

# RS256: Solo usamos la LLAVE PÚBLICA para validar (Seguridad Asimétrica)
AUTH_PUBLIC_KEY = os.getenv("AUTH_PUBLIC_KEY", "")
ALGORITHM = "RS256"

def decode_access_token(token: str) -> Optional[Dict]:
    """Valida un token JWT con la llave pública de ApiIam."""
    try:
        if not AUTH_PUBLIC_KEY:
            logger.error("❌ [SECURITY] AUTH_PUBLIC_KEY no configurada")
            return None
        
        # El token puede venir con saltos de línea o formato PEM, lo manejamos
        public_key = AUTH_PUBLIC_KEY.replace("\\n", "\n")
        
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("⚠️ [SECURITY] Token expirado")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"❌ [SECURITY] Token inválido: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ [SECURITY] Error inesperado validando token: {e}")
        return None
