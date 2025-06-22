from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models, crud

router = APIRouter()

@router.get("/cursos/")
def read_cursos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cursos = crud.get_cursos(db, skip=skip, limit=limit)
    return cursos

@router.get("/cursos/{curso_id}")
def read_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = crud.get_curso(db, curso_id=curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_curso

@router.post("/cursos/")
def create_curso(curso_data: dict, db: Session = Depends(get_db)):
    return crud.create_curso(db=db, curso=curso_data)

@router.put("/cursos/{curso_id}")
def update_curso(curso_id: int, curso_data: dict, db: Session = Depends(get_db)):
    db_curso = crud.get_curso(db, curso_id=curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return crud.update_curso(db=db, curso_id=curso_id, curso=curso_data)

@router.delete("/cursos/{curso_id}")
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = crud.get_curso(db, curso_id=curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    crud.delete_curso(db=db, curso_id=curso_id)
    return {"message": "Curso eliminado exitosamente"}
