from sqlmodel import Session, select
from app.models.model_users import User

class UserRepository:
    def __init__(self, session:Session):
        self.session = session

    def get_by_email(self, email:str)->User | None:
        #Obtenemos el usuario por email
        statement =  select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_by_id(self, user_id:int)->User | None:
         #Obtenemos el usuario por id
         return self.session.get(User, user_id)

    def create(self, user:User)->User:
        #Creamos un nuevo usuario
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_all_users(self)->list[User]:
        statement = select(User)
        return self.session.exec(statement).all()