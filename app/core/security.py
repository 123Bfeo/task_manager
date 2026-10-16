#Codificacion del modulo de seguridad para leer passwordhast 
#t generar Jwt
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from .config import settings

password_hash = PasswordHash.recommended()

#Hash ficticio para comparacion cuando el usuario no existe (evita timing attacks)
DUMMY_HASH = password_hash.hash("dummypassword")

def get_password_hash(password:str)->str:
      """
      Convierte contrasena en texto plano a su hash Aragon2
      """
      return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str)->bool:
     """
     Verifica si una contrasena en su texto plano coincide con su hash
     """
     return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict[str, Any], expires_delta:timedelta| None = None)->str:
      """
      Genera un JWT firmado con la clave secreta
      """
      to_encode = data.copy()
      expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
      )
      to_encode.update({"exp":expire})
      return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)