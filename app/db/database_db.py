""""
SQLModel: proporciona la base para definir los modelos y registrar sus tablas.
create_engine: crea el motor que administra las conexiones a la base de datos.
Session: permite realizar operaciones de lectura y escritura.
"""
from sqlmodel import SQLModel, create_engine, Session

#Defines el nombre del archivo de la base de datos y construyes su URL de conexión.
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine =   create_engine(sqlite_url, connect_args=connect_args)

#create_engine() configura el motor que SQLModel utilizará para comunicarse con SQLite.
#check_same_thread=False permite utilizar una conexión SQLite desde distintos hilos, algo útil en ciertos escenarios de FastAPI.

#Esta función crea las tablas que SQLModel conoce a través de sus modelos registrados.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

""""
Su propósito es proporcionar una sesión de base de datos a quien la necesite y cerrarla cuando termine su uso.
Veamos cómo funciona:
1. Session(engine) crea una sesión asociada al motor.
2. with garantiza que la sesión se cierre al salir del bloque.
3. yield session entrega la sesión al consumidor sin terminar inmediatamente la función.
4. Cuando FastAPI termina de gestionar la dependencia, la ejecución continúa y la sesión se cierra.
"""

