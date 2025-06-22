from sqlalchemy.orm import Session
from app.database import models
from app.schemas import alumno, competencia

# Funciones para Alumnos
def get_alumno(db: Session, alumno_id: int):
    return db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()

def get_alumnos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Alumno).offset(skip).limit(limit).all()

def create_alumno(db: Session, alumno_data: alumno.AlumnoCreate):
    db_alumno = models.Alumno(
        Nombre=f"{alumno_data.nombre} {alumno_data.apellido}",
        Promedio_Calificaciones=0.0,
        Cantidad_Competencias=0,
        CI=0,
        Cluster_KMeans=0,
        Cluster_DBSCAN=0,
        Recomendaciones_Basicas=""
    )
    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)
    return db_alumno

def update_alumno(db: Session, alumno_id: int, alumno_data: alumno.AlumnoUpdate):
    db_alumno = get_alumno(db, alumno_id)
    if db_alumno:
        if alumno_data.nombre and alumno_data.apellido:
            db_alumno.Nombre = f"{alumno_data.nombre} {alumno_data.apellido}"
        db.commit()
        db.refresh(db_alumno)
    return db_alumno

def delete_alumno(db: Session, alumno_id: int):
    db_alumno = get_alumno(db, alumno_id)
    if db_alumno:
        db.delete(db_alumno)
        db.commit()
    return db_alumno

# Funciones para Competencias (usando CompetenciaPlantilla)
def get_competencia(db: Session, competencia_id: int):
    return db.query(models.CompetenciaPlantilla).filter(models.CompetenciaPlantilla.CompetenciaPlantilla_ID == competencia_id).first()

def get_competencias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CompetenciaPlantilla).offset(skip).limit(limit).all()

def create_competencia(db: Session, competencia_data: competencia.CompetenciaCreate):
    db_competencia = models.CompetenciaPlantilla(
        Codigo_Competencia=competencia_data.nombre,
        Descripcion=competencia_data.descripcion,
        Curso_ID=1  # Default course ID
    )
    db.add(db_competencia)
    db.commit()
    db.refresh(db_competencia)
    return db_competencia

def update_competencia(db: Session, competencia_id: int, competencia_data: competencia.CompetenciaUpdate):
    db_competencia = get_competencia(db, competencia_id)
    if db_competencia:
        if competencia_data.nombre:
            db_competencia.Codigo_Competencia = competencia_data.nombre
        if competencia_data.descripcion:
            db_competencia.Descripcion = competencia_data.descripcion
        db.commit()
        db.refresh(db_competencia)
    return db_competencia

def delete_competencia(db: Session, competencia_id: int):
    db_competencia = get_competencia(db, competencia_id)
    if db_competencia:
        db.delete(db_competencia)
        db.commit()
    return db_competencia

# Funciones para Cursos
def get_curso(db: Session, curso_id: int):
    return db.query(models.Curso).filter(models.Curso.Curso_ID == curso_id).first()

def get_cursos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Curso).offset(skip).limit(limit).all()

def create_curso(db: Session, curso: dict):
    db_curso = models.Curso(**curso)
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def update_curso(db: Session, curso_id: int, curso: dict):
    db_curso = get_curso(db, curso_id)
    if db_curso:
        for key, value in curso.items():
            setattr(db_curso, key, value)
        db.commit()
        db.refresh(db_curso)
    return db_curso

def delete_curso(db: Session, curso_id: int):
    db_curso = get_curso(db, curso_id)
    if db_curso:
        db.delete(db_curso)
        db.commit()
    return db_curso
