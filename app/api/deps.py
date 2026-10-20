import jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.config import settings
from app.db.database_db import get_session
from app.models.model_users import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData


oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_user_repository(session:Annotated[Session, Depends(get_session)])-> UserRepository:
    """
        Proveer el repositorio
        Necesitas una sesión de base de datos para usar el repositorio.
        Esta función inyecta la sesión y devuelve el repositorio listo.
    """
    return UserRepository(session)

def get_current_user(
        token: Annotated[str, Depends(oauth_schema)],
        user_repo: Annotated[UserRepository, Depends(get_user_repository)]
        )->User:
    """
    Esta función hace todo el proceso de verificación:
    Extrae el token que envía el cliente.
    Lo decodifica con tu clave secreta y algoritmo → obtiene el user_id guardado dentro.
    Si el token está mal, caducado o le falta información → lanza error 401 No autorizado.
    Con el user_id, consulta en la base de datos si ese usuario existe.
    Devuelve el objeto completo del usuario si todo está bien.
    
    """
    credential_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credential_exception
        token_data = TokenData(user_id=int(user_id_str))
 
    except(InvalidTokenError, ValueError):
        raise credential_exception

    user = user_repo.get_by_id(token_data.user_id)
    if user is None:
        raise credential_exception

    return user

def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
        )->User :
    """
    Toda ruta que necesite "saber quién está conectado" usará esta dependencia
    Se apoya en la anterior: primero comprueba que haya sesión, luego verifica que is_active sea True.
    Útil si en el futuro quieres desactivar cuentas sin borrarlas: el usuario no podrá acceder aunque tenga token válido.

    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user
