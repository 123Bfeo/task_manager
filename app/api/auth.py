##Importar dependencias para manejo de rutas 
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login():
    """
    Controller que permite el login de los usuarios
    """
    return [{"status": 200}, {"message": "User logueado"}]

@router.post("/register")
async def register():
    """
    Controller que permiteb el registro de usuarios
    """
    return [{"status": 200}, {"message": "User register"}]