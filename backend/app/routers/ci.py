from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.database import models
from app.schemas import ci as schemas

router = APIRouter(prefix="/ci", tags=["Coeficiente Intelectual"])

@router.get("/", response_model=List[schemas.CI])
def get_cis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los registros de CI con paginación"""
    cis = db.query(models.Alumno).filter(models.Alumno.CI.isnot(None)).offset(skip).limit(limit).all()
    return [
        schemas.CI(
            CI_ID=alumno.Alumno_ID,
            Alumno_ID=alumno.Alumno_ID,
            Valor_CI=alumno.CI,
            Fecha_Test=None,
            Tipo_Test=None,
            Observaciones=None
        ) for alumno in cis
    ]

@router.get("/alumno/{alumno_id}", response_model=schemas.CI)
def get_ci_alumno(alumno_id: int, db: Session = Depends(get_db)):
    """Obtener el CI de un alumno específico"""
    # Verificar que el alumno existe
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    if alumno.CI is None:
        raise HTTPException(status_code=404, detail="El alumno no tiene registro de CI")
    
    return schemas.CI(
        CI_ID=alumno.Alumno_ID,
        Alumno_ID=alumno.Alumno_ID,
        Valor_CI=alumno.CI,
        Fecha_Test=None,
        Tipo_Test=None,
        Observaciones=None
    )

@router.post("/", response_model=schemas.CI)
def create_ci(ci_data: schemas.CICreate, db: Session = Depends(get_db)):
    """Crear o actualizar el CI de un alumno"""
    # Verificar que el alumno existe
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == ci_data.Alumno_ID).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    # Actualizar el CI del alumno
    alumno.CI = ci_data.Valor_CI
    db.commit()
    db.refresh(alumno)
    
    return schemas.CI(
        CI_ID=alumno.Alumno_ID,
        Alumno_ID=alumno.Alumno_ID,
        Valor_CI=alumno.CI,
        Fecha_Test=ci_data.Fecha_Test,
        Tipo_Test=ci_data.Tipo_Test,
        Observaciones=ci_data.Observaciones
    )

@router.put("/{alumno_id}", response_model=schemas.CI)
def update_ci(alumno_id: int, ci_data: schemas.CIUpdate, db: Session = Depends(get_db)):
    """Actualizar el CI de un alumno existente"""
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    # Actualizar solo los campos proporcionados
    update_data = ci_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "Valor_CI":
            setattr(alumno, "CI", value)
        # Los otros campos se pueden agregar a una tabla separada si es necesario
    
    db.commit()
    db.refresh(alumno)
    
    return schemas.CI(
        CI_ID=alumno.Alumno_ID,
        Alumno_ID=alumno.Alumno_ID,
        Valor_CI=alumno.CI,
        Fecha_Test=ci_data.Fecha_Test,
        Tipo_Test=ci_data.Tipo_Test,
        Observaciones=ci_data.Observaciones
    )

@router.delete("/{alumno_id}")
def delete_ci(alumno_id: int, db: Session = Depends(get_db)):
    """Eliminar el CI de un alumno (establecer como None)"""
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    alumno.CI = None
    db.commit()
    return {"message": "CI eliminado exitosamente"}

@router.get("/estadisticas/general")
def get_estadisticas_ci(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de CI"""
    alumnos_con_ci = db.query(models.Alumno).filter(models.Alumno.CI.isnot(None)).all()
    
    if not alumnos_con_ci:
        return {"message": "No hay datos de CI registrados"}
    
    valores_ci = [alumno.CI for alumno in alumnos_con_ci]
    promedio = sum(valores_ci) / len(valores_ci)
    maximo = max(valores_ci)
    minimo = min(valores_ci)
    
    # Categorizar CI
    categorias = {
        "Muy Superior": {"min": 130, "max": 200, "count": 0},
        "Superior": {"min": 120, "max": 129, "count": 0},
        "Promedio Alto": {"min": 110, "max": 119, "count": 0},
        "Promedio": {"min": 90, "max": 109, "count": 0},
        "Promedio Bajo": {"min": 80, "max": 89, "count": 0},
        "Bajo": {"min": 70, "max": 79, "count": 0},
        "Muy Bajo": {"min": 0, "max": 69, "count": 0}
    }
    
    for ci_valor in valores_ci:
        for categoria, rango in categorias.items():
            if rango["min"] <= ci_valor <= rango["max"]:
                rango["count"] += 1
                break
    
    return {
        "total_alumnos": len(alumnos_con_ci),
        "promedio_ci": round(promedio, 2),
        "ci_maximo": maximo,
        "ci_minimo": minimo,
        "rango_ci": {"minimo": minimo, "maximo": maximo},
        "alumnos_por_rango": categorias
    }

@router.get("/resumen/alumno/{alumno_id}")
def get_resumen_ci_alumno(alumno_id: int, db: Session = Depends(get_db)):
    """Obtener resumen de CI de un alumno específico"""
    alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    if alumno.CI is None:
        return {"message": "El alumno no tiene registro de CI"}
    
    # Determinar categoría
    ci_valor = alumno.CI
    if ci_valor >= 130:
        categoria = "Muy Superior"
    elif ci_valor >= 120:
        categoria = "Superior"
    elif ci_valor >= 110:
        categoria = "Promedio Alto"
    elif ci_valor >= 90:
        categoria = "Promedio"
    elif ci_valor >= 80:
        categoria = "Promedio Bajo"
    elif ci_valor >= 70:
        categoria = "Bajo"
    else:
        categoria = "Muy Bajo"
    
    # Calcular percentil aproximado
    todos_ci = db.query(models.Alumno.CI).filter(models.Alumno.CI.isnot(None)).all()
    valores_todos = [ci[0] for ci in todos_ci]
    valores_todos.sort()
    
    try:
        posicion = valores_todos.index(ci_valor)
        percentil = ((posicion + 1) / len(valores_todos)) * 100
    except ValueError:
        percentil = None
    
    return {
        "alumno_id": alumno_id,
        "nombre_alumno": alumno.Nombre,
        "valor_ci": ci_valor,
        "categoria": categoria,
        "percentil": round(percentil, 1) if percentil else None
    }

@router.get("/rango/{min_ci}/{max_ci}")
def get_alumnos_por_rango_ci(min_ci: int, max_ci: int, db: Session = Depends(get_db)):
    """Obtener alumnos dentro de un rango de CI específico"""
    alumnos = db.query(models.Alumno).filter(
        models.Alumno.CI >= min_ci,
        models.Alumno.CI <= max_ci
    ).all()
    
    return [
        {
            "alumno_id": alumno.Alumno_ID,
            "nombre": alumno.Nombre,
            "ci": alumno.CI
        } for alumno in alumnos
    ] 