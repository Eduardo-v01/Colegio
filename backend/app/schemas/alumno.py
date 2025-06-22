from pydantic import BaseModel
from typing import Optional

class AlumnoBase(BaseModel):
    nombre: str
    apellido: str
    email: Optional[str] = None
    edad: Optional[int] = None

class AlumnoCreate(AlumnoBase):
    pass

class AlumnoUpdate(AlumnoBase):
    nombre: Optional[str] = None
    apellido: Optional[str] = None

class Alumno(AlumnoBase):
    id: int

    class Config:
        from_attributes = True
