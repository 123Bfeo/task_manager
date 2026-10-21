from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    get_password_hash,
    verify_password
)
from app.models.model_users import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

class AuthService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    def register_user(self, data:UserCreate)->User:
        if self.user_repo.get_by_email(data.email):
            raise ValueError("El email ya esta registado")
        user = User(
            email= data.email,
            full_name= data.full_name,
            password_hash= get_password_hash(data.password)
        )

        return self.user_repo.create(user)

    def authenticate(self, email:str, password:str)->User | None:
        user = self.user_repo.get_by_email(email)
         
        #si el usuario no existe, verificamos conta DUMMY_HASH
        #para mantener el tiempo de respuesta constante

        if not user:
            verify_password(password, DUMMY_HASH)
            return None

        if not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        return user

    def create_token_for_user(self, user:User)->str:
        #El "sub" debe ser un string unico en toda la app
        return create_access_token(data={"sub": str(user.id)})

    