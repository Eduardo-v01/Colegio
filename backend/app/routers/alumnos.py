from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models, crud
from app.schemas import alumno

router = APIRouter()

@router.get("/alumnos/")
def read_alumnos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alumnos = crud.get_alumnos(db, skip=skip, limit=limit)
    # Convertir a formato JSON compatible
    result = []
    for alum in alumnos:
        # Obtener inteligencias del alumno
        inteligencias = db.query(models.Inteligencia).filter(
            models.Inteligencia.Alumno_ID == alum.Alumno_ID
        ).all()
        
        inteligencias_data = []
        for intel in inteligencias:
            inteligencias_data.append({
                "Inteligencia_ID": intel.Inteligencia_ID,
                "Tipo_Inteligencia": intel.Tipo_Inteligencia,
                "Puntaje": intel.Puntaje
            })
        
        result.append({
            "id": alum.Alumno_ID,
            "nombre": alum.Nombre,
            "apellido": "",  # El nombre completo está en Nombre
            "email": "",  # No hay campo email en el modelo
            "edad": None,  # No hay campo edad en el modelo
            "Alumno_ID": alum.Alumno_ID,
            "Nombre": alum.Nombre,
            "Promedio_Calificaciones": alum.Promedio_Calificaciones,
            "Cantidad_Competencias": alum.Cantidad_Competencias,
            "CI": alum.CI,
            "Cluster_KMeans": alum.Cluster_KMeans,
            "Cluster_DBSCAN": alum.Cluster_DBSCAN,
            "Recomendaciones_Basicas": alum.Recomendaciones_Basicas,
            "inteligencias": inteligencias_data
        })
    return result

@router.get("/alumnos/{alumno_id}")
def read_alumno(alumno_id: int, db: Session = Depends(get_db)):
    db_alumno = crud.get_alumno(db, alumno_id=alumno_id)
    if db_alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    # Obtener inteligencias del alumno
    inteligencias = db.query(models.Inteligencia).filter(
        models.Inteligencia.Alumno_ID == alumno_id
    ).all()
    
    inteligencias_data = []
    for intel in inteligencias:
        inteligencias_data.append({
            "Inteligencia_ID": intel.Inteligencia_ID,
            "Tipo_Inteligencia": intel.Tipo_Inteligencia,
            "Puntaje": intel.Puntaje
        })
    
    return {
        "id": db_alumno.Alumno_ID,
        "nombre": db_alumno.Nombre,
        "apellido": "",
        "email": "",
        "edad": None,
        "Alumno_ID": db_alumno.Alumno_ID,
        "Nombre": db_alumno.Nombre,
        "Promedio_Calificaciones": db_alumno.Promedio_Calificaciones,
        "Cantidad_Competencias": db_alumno.Cantidad_Competencias,
        "CI": db_alumno.CI,
        "Cluster_KMeans": db_alumno.Cluster_KMeans,
        "Cluster_DBSCAN": db_alumno.Cluster_DBSCAN,
        "Recomendaciones_Basicas": db_alumno.Recomendaciones_Basicas,
        "inteligencias": inteligencias_data
    }

@router.post("/alumnos/")
def create_alumno(alumno_data: alumno.AlumnoCreate, db: Session = Depends(get_db)):
    return crud.create_alumno(db=db, alumno=alumno_data)

@router.put("/alumnos/{alumno_id}")
def update_alumno(alumno_id: int, alumno_data: alumno.AlumnoUpdate, db: Session = Depends(get_db)):
    db_alumno = crud.get_alumno(db, alumno_id=alumno_id)
    if db_alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return crud.update_alumno(db=db, alumno_id=alumno_id, alumno=alumno_data)

@router.delete("/alumnos/{alumno_id}")
def delete_alumno(alumno_id: int, db: Session = Depends(get_db)):
    db_alumno = crud.get_alumno(db, alumno_id=alumno_id)
    if db_alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    crud.delete_alumno(db=db, alumno_id=alumno_id)
    return {"message": "Alumno eliminado exitosamente"}

@router.get("/alumnos/nombres/")
def get_alumnos_nombres(db: Session = Depends(get_db)):
    alumnos = db.query(models.Alumno.Alumno_ID, models.Alumno.Nombre).all()
    return [{"Alumno_ID": a.Alumno_ID, "Nombre": a.Nombre} for a in alumnos]