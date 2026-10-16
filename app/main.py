from fastapi import FastAPI, Depends
from app.db.database_db import create_db_and_tables
from .api import users
from .api import auth
app = FastAPI()
app.title = "task_manager"
app.version = "1.0.0"


#Permite la impelemntacion de los endpoint 
app.include_router(users.router)
app.include_router(auth.router)