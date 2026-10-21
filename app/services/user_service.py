from app.models.model_users import User
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    def get_all_users(self)->list[User]:
        return self.user_repo.get_all_users()
