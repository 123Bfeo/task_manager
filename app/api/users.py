#Para para la creacion de nuestros endpoint 
#Usamos APIRouter de la siguiente manera
from fastapi import APIRouter, Depends
from typing import Annotated
from app.repositories.user_repository import UserRepository
from app.api.deps import get_user_repository
from app.services.user_service import UserService
from app.schemas.user import UserPublic
from fastapi import APIRouter, Depends, HTTPException, status



router = APIRouter(prefix="/users", tags=["Users"])


def get_auth_service(
        user_repo: Annotated[UserRepository, Depends(get_user_repository)]
)->UserService:
    return UserService(user_repo)


@router.get("/users", response_model= list[UserPublic])
async def get_users(
    user_service: Annotated[UserService, Depends(get_auth_service)]
):
    """"
     Controlador para obtener los usuarios de la aplicacion
    """
    try:
       return user_service.get_all_users();
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.get("/perfil")
async def get_perfil():
    """"
    Controlador que permite traer los datos del perfil del usuario
    """
    return [{"username": "Rick"}, {"username": "Morty"}, {"edad":15}]