from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

""""
Detalles importantes:

table=True le dice a SQLModel que esto es una tabla de base de datos, no solo un modelo Pydantic 
Field(default=None, primary_key=True) en el id permite que la base de datos lo autoincremente 
unique=True en email evita duplicados a nivel de base de datos
index=True acelera búsquedas por email
"""

class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key = True)
    email: str = Field(unique=True, index = True)
    password_hash:str
    full_name: str
    is_active: bool = Field(default = True)
    is_verified: bool = Field(default = False)
    created_at:  datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

