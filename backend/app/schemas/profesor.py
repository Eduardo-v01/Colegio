from pydantic import BaseModel
from typing import Optional, List

class ProfesorBase(BaseModel):
    Nombre: str
    DNI: str

class ProfesorCreate(ProfesorBase):
    Contrasena: str

class ProfesorUpdate(BaseModel):
    Nombre: Optional[str] = None
    DNI: Optional[str] = None
    Contrasena: Optional[str] = None

class Profesor(ProfesorBase):
    Profesor_ID: int

    class Config:
        from_attributes = True

class CursoInfo(BaseModel):
    Curso_ID: int
    Nombre: str

    class Config:
        from_attributes = True

class ProfesorConCursos(Profesor):
    cursos: List[CursoInfo] = []

    class Config:
        from_attributes = True

class ProfesorEstadisticas(BaseModel):
    profesor_id: int
    nombre: str
    total_cursos: int
    cursos_asignados: List[CursoInfo]
    total_alumnos: int
    promedio_calificaciones: float

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    dni: Optional[str] = None

class LoginData(BaseModel):
    DNI: str
    password: str

class AsignacionCurso(BaseModel):
    profesor_id: int
    curso_id: int 