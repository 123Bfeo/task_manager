##Importar dependencias para manejo de rutas 
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from app.api.deps import get_user_repository, get_current_active_user
from app.models.model_users import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserPublic
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])

def get_auth_service(
        user_repo: Annotated[UserRepository, Depends(get_user_repository)]
)->AuthService:
    return AuthService(user_repo)



@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """
    Controller que permite el login de los usuarios
    """
    user = auth_service.authenticate(
        email= form_data.username, 
        password= form_data.password
    )

    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_token_for_user(user)
    return Token(access_token=access_token)


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    auth_service: Annotated[AuthService,Depends(get_auth_service)]
):
    """
    Controller que permiteb el registro de usuarios
    """
    try:
        return auth_service.register_user(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/me", response_model=UserPublic)
def read_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

