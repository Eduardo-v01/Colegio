from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models, crud
from app.schemas import competencia

router = APIRouter()

@router.get("/competencias/")
def read_competencias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    competencias = crud.get_competencias(db, skip=skip, limit=limit)
    # Convertir a formato JSON compatible
    result = []
    for comp in competencias:
        result.append({
            "id": comp.CompetenciaPlantilla_ID,
            "nombre": comp.Codigo_Competencia,
            "descripcion": comp.Descripcion,
            "CompetenciaPlantilla_ID": comp.CompetenciaPlantilla_ID,
            "Curso_ID": comp.Curso_ID,
            "Codigo_Competencia": comp.Codigo_Competencia,
            "Descripcion": comp.Descripcion
        })
    return result

@router.get("/competencias/{competencia_id}")
def read_competencia(competencia_id: int, db: Session = Depends(get_db)):
    db_competencia = crud.get_competencia(db, competencia_id=competencia_id)
    if db_competencia is None:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    
    return {
        "id": db_competencia.CompetenciaPlantilla_ID,
        "nombre": db_competencia.Codigo_Competencia,
        "descripcion": db_competencia.Descripcion,
        "CompetenciaPlantilla_ID": db_competencia.CompetenciaPlantilla_ID,
        "Curso_ID": db_competencia.Curso_ID,
        "Codigo_Competencia": db_competencia.Codigo_Competencia,
        "Descripcion": db_competencia.Descripcion
    }

@router.post("/competencias/")
def create_competencia(competencia_data: competencia.CompetenciaCreate, db: Session = Depends(get_db)):
    return crud.create_competencia(db=db, competencia=competencia_data)

@router.put("/competencias/{competencia_id}")
def update_competencia(competencia_id: int, competencia_data: competencia.CompetenciaUpdate, db: Session = Depends(get_db)):
    db_competencia = crud.get_competencia(db, competencia_id=competencia_id)
    if db_competencia is None:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    return crud.update_competencia(db=db, competencia_id=competencia_id, competencia=competencia_data)

@router.delete("/competencias/{competencia_id}")
def delete_competencia(competencia_id: int, db: Session = Depends(get_db)):
    db_competencia = crud.get_competencia(db, competencia_id=competencia_id)
    if db_competencia is None:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    crud.delete_competencia(db=db, competencia_id=competencia_id)
    return {"message": "Competencia eliminada exitosamente"}
