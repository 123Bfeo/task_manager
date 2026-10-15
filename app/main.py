from fastapi import FastAPI
from app.db.database_db import create_db_and_tables



app = FastAPI()
app.title = "task_manager"
app.version = "1.0.0"

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
  

@app.get("/health", tags=["Home"])
def health_check():
    return {"status":"ok"}


@app.get("/home", tags=["Home"])
def perfil():
    return {"Home":"ok"}

@app.get("/perfil", tags=["Users"])
def perfil():
    return {"perfil":"ok"}
#listo