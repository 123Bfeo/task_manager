#Para para la creacion de nuestros endpoint 
#Usamos APIRouter de la siguiente manera
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/users")
async def get_users():
    """"
     Controlador para obtener los usuarios de la aplicacion
    """
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/perfil")
async def get_perfil():
    """"
    Controlador que permite traer los datos del perfil del usuario
    """
    return [{"username": "Rick"}, {"username": "Morty"}, {"edad":15}]