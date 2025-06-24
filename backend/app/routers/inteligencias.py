from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.database import models
from app.schemas import inteligencias as schemas

router = APIRouter(prefix="/inteligencias", tags=["Inteligencias"])

@router.get("/", response_model=List[schemas.Inteligencia])
def get_inteligencias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todas las inteligencias con paginación"""
    inteligencias = db.query(models.Inteligencia).offset(skip).limit(limit).all()
    return inteligencias

@router.get("/alumno/{alumno_id}", response_model=List[schemas.Inteligencia])
def get_inteligencias_alumno(alumno_id: int, db: Session = Depends(get_db)):
    """Obtener todas las inteligencias de un alumno específico"""
    # Verificar que el alumno existe
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    inteligencias = db.query(models.Inteligencia).filter(models.Inteligencia.Alumno_ID == alumno_id).all()
    return inteligencias

@router.get("/{inteligencia_id}", response_model=schemas.Inteligencia)
def get_inteligencia(inteligencia_id: int, db: Session = Depends(get_db)):
    """Obtener una inteligencia específica por ID"""
    inteligencia = db.query(models.Inteligencia).filter(models.Inteligencia.Inteligencia_ID == inteligencia_id).first()
    if not inteligencia:
        raise HTTPException(status_code=404, detail="Inteligencia no encontrada")
    return inteligencia

@router.post("/", response_model=schemas.Inteligencia)
def create_inteligencia(inteligencia: schemas.InteligenciaCreate, db: Session = Depends(get_db)):
    """Crear una nueva inteligencia"""
    # Verificar que el alumno existe
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == inteligencia.Alumno_ID).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    db_inteligencia = models.Inteligencia(**inteligencia.dict())
    db.add(db_inteligencia)
    db.commit()
    db.refresh(db_inteligencia)
    return db_inteligencia

@router.put("/{inteligencia_id}", response_model=schemas.Inteligencia)
def update_inteligencia(inteligencia_id: int, inteligencia: schemas.InteligenciaUpdate, db: Session = Depends(get_db)):
    """Actualizar una inteligencia existente"""
    db_inteligencia = db.query(models.Inteligencia).filter(models.Inteligencia.Inteligencia_ID == inteligencia_id).first()
    if not db_inteligencia:
        raise HTTPException(status_code=404, detail="Inteligencia no encontrada")
    
    # Actualizar solo los campos proporcionados
    update_data = inteligencia.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_inteligencia, field, value)
    
    db.commit()
    db.refresh(db_inteligencia)
    return db_inteligencia

@router.delete("/{inteligencia_id}")
def delete_inteligencia(inteligencia_id: int, db: Session = Depends(get_db)):
    """Eliminar una inteligencia"""
    db_inteligencia = db.query(models.Inteligencia).filter(models.Inteligencia.Inteligencia_ID == inteligencia_id).first()
    if not db_inteligencia:
        raise HTTPException(status_code=404, detail="Inteligencia no encontrada")
    
    db.delete(db_inteligencia)
    db.commit()
    return {"message": "Inteligencia eliminada exitosamente"}

@router.delete("/alumno/{alumno_id}")
def delete_inteligencias_alumno(alumno_id: int, db: Session = Depends(get_db)):
    """Eliminar todas las inteligencias de un alumno"""
    # Verificar que el alumno existe
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    inteligencias = db.query(models.Inteligencia).filter(models.Inteligencia.Alumno_ID == alumno_id).all()
    for inteligencia in inteligencias:
        db.delete(inteligencia)
    
    db.commit()
    return {"message": f"Se eliminaron {len(inteligencias)} inteligencias del alumno"}

@router.get("/tipos/lista")
def get_tipos_inteligencia(db: Session = Depends(get_db)):
    """Obtener lista de todos los tipos de inteligencia únicos"""
    tipos = db.query(models.Inteligencia.Tipo_Inteligencia).distinct().all()
    return {"tipos_inteligencia": [tipo[0] for tipo in tipos]}

@router.get("/estadisticas/alumno/{alumno_id}")
def get_estadisticas_inteligencia_alumno(alumno_id: int, db: Session = Depends(get_db)):
    """Obtener estadísticas de inteligencias de un alumno"""
    # Verificar que el alumno existe
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    inteligencias = db.query(models.Inteligencia).filter(models.Inteligencia.Alumno_ID == alumno_id).all()
    
    if not inteligencias:
        return {"message": "El alumno no tiene datos de inteligencias registrados"}
    
    puntajes = [intel.Puntaje for intel in inteligencias]
    max_puntaje = max(puntajes)
    min_puntaje = min(puntajes)
    promedio = sum(puntajes) / len(puntajes)
    
    # Encontrar la inteligencia más alta
    inteligencia_max = next(intel for intel in inteligencias if intel.Puntaje == max_puntaje)
    
    return {
        "alumno_id": alumno_id,
        "nombre_alumno": alumno.Nombre,
        "total_inteligencias": len(inteligencias),
        "puntaje_maximo": max_puntaje,
        "inteligencia_maxima": inteligencia_max.Tipo_Inteligencia,
        "puntaje_minimo": min_puntaje,
        "promedio": round(promedio, 2),
        "inteligencias": [
            {
                "tipo": intel.Tipo_Inteligencia,
                "puntaje": intel.Puntaje
            } for intel in inteligencias
        ]
    } 