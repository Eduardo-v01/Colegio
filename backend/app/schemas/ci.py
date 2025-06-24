from pydantic import BaseModel
from typing import Optional

class CIBase(BaseModel):
    Alumno_ID: int
    Valor_CI: int
    Fecha_Test: Optional[str] = None
    Tipo_Test: Optional[str] = None
    Observaciones: Optional[str] = None

class CICreate(CIBase):
    pass

class CIUpdate(BaseModel):
    Alumno_ID: Optional[int] = None
    Valor_CI: Optional[int] = None
    Fecha_Test: Optional[str] = None
    Tipo_Test: Optional[str] = None
    Observaciones: Optional[str] = None

class CI(CIBase):
    CI_ID: int

    class Config:
        from_attributes = True

class CIEstadisticas(BaseModel):
    total_alumnos: int
    promedio_ci: float
    ci_maximo: int
    ci_minimo: int
    rango_ci: dict
    alumnos_por_rango: dict

class CIResumen(BaseModel):
    alumno_id: int
    nombre_alumno: str
    valor_ci: int
    categoria: str
    percentil: Optional[float] = None 