from pydantic import BaseModel
from typing import Optional

class CompetenciaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CompetenciaCreate(CompetenciaBase):
    pass

class CompetenciaUpdate(CompetenciaBase):
    nombre: Optional[str] = None

class Competencia(CompetenciaBase):
    id: int
    # Campos adicionales para mapear con la base de datos
    CompetenciaPlantilla_ID: Optional[int] = None
    Curso_ID: Optional[int] = None
    Codigo_Competencia: Optional[str] = None
    Descripcion: Optional[str] = None

    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        # Mapear los campos de la base de datos al schema
        return cls(
            id=obj.CompetenciaPlantilla_ID,
            nombre=obj.Codigo_Competencia,
            descripcion=obj.Descripcion,
            CompetenciaPlantilla_ID=obj.CompetenciaPlantilla_ID,
            Curso_ID=obj.Curso_ID,
            Codigo_Competencia=obj.Codigo_Competencia,
            Descripcion=obj.Descripcion
        )
