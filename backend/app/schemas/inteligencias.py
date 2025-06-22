from pydantic import BaseModel
from typing import Optional

class InteligenciaBase(BaseModel):
    Alumno_ID: int
    Tipo_Inteligencia: str
    Puntaje: float

class InteligenciaCreate(InteligenciaBase):
    pass

class InteligenciaUpdate(BaseModel):
    Alumno_ID: Optional[int] = None
    Tipo_Inteligencia: Optional[str] = None
    Puntaje: Optional[float] = None

class Inteligencia(InteligenciaBase):
    Inteligencia_ID: int

    class Config:
        from_attributes = True

class InteligenciaEstadisticas(BaseModel):
    alumno_id: int
    nombre_alumno: str
    total_inteligencias: int
    puntaje_maximo: float
    inteligencia_maxima: str
    puntaje_minimo: float
    promedio: float
    inteligencias: list[dict]

class TiposInteligencia(BaseModel):
    tipos_inteligencia: list[str] 