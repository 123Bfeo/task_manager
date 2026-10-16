from fastapi import FastAPI, Depends
from app.db.database_db import create_db_and_tables
from .api import users

app = FastAPI()
app.title = "task_manager"
app.version = "1.0.0"

app.include_router(users.router)
