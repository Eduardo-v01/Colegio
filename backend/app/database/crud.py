from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models
from app.schemas import alumno, competencia, profesor as profesor_schema, conversacion as conversacion_schema
from app.services.auth import get_password_hash
import json
from datetime import datetime
from typing import Dict
import logging

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

def update_alumno_clusters(db: Session, alumno_id: int, cluster_kmeans: int, cluster_dbscan: int):
    """
    Actualiza los clusters de un alumno específico
    """
    try:
        db_alumno = get_alumno(db, alumno_id)
        if db_alumno:
            db_alumno.Cluster_KMeans = cluster_kmeans
            db_alumno.Cluster_DBSCAN = cluster_dbscan
            db.commit()
            db.refresh(db_alumno)
            logging.info(f"Clusters actualizados para alumno {alumno_id}: KMeans={cluster_kmeans}, DBSCAN={cluster_dbscan}")
            return db_alumno
        return None
    except Exception as e:
        logging.error(f"Error actualizando clusters para alumno {alumno_id}: {str(e)}")
        raise

def update_all_alumno_clusters(db: Session, clustering_results: Dict):
    """
    Actualiza los clusters de todos los alumnos basado en los resultados del clustering
    """
    try:
        updated_count = 0
        
        # Obtener resultados de K-Means
        kmeans_data = clustering_results.get("clusters", {}).get("kmeans", {})
        kmeans_clusters = kmeans_data.get("clusters", [])
        kmeans_alumno_ids = kmeans_data.get("alumno_ids", [])
        
        # Obtener resultados de DBSCAN
        dbscan_data = clustering_results.get("clusters", {}).get("dbscan", {})
        dbscan_clusters = dbscan_data.get("clusters", [])
        dbscan_alumno_ids = dbscan_data.get("alumno_ids", [])
        
        # Actualizar cada alumno
        for i, alumno_id in enumerate(kmeans_alumno_ids):
            if i < len(kmeans_clusters) and i < len(dbscan_clusters):
                cluster_kmeans = kmeans_clusters[i]
                cluster_dbscan = dbscan_clusters[i]
                
                updated_alumno = update_alumno_clusters(db, alumno_id, cluster_kmeans, cluster_dbscan)
                if updated_alumno:
                    updated_count += 1
        
        logging.info(f"Clusters actualizados para {updated_count} alumnos")
        return updated_count
        
    except Exception as e:
        logging.error(f"Error actualizando clusters de todos los alumnos: {str(e)}")
        raise

def get_alumnos_with_clusters(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los alumnos con información de clusters
    """
    try:
        alumnos = db.query(models.Alumno).offset(skip).limit(limit).all()
        
        # Enriquecer con datos de inteligencias y calificaciones
        enriched_alumnos = []
        for alumno in alumnos:
            # Obtener inteligencias
            inteligencias = db.query(models.Inteligencia).filter(
                models.Inteligencia.Alumno_ID == alumno.Alumno_ID
            ).all()
            
            # Obtener calificaciones
            calificaciones = db.query(models.AlumnoCompetencia).join(
                models.CompetenciaPlantilla
            ).filter(
                models.AlumnoCompetencia.Alumno_ID == alumno.Alumno_ID
            ).all()
            
            # Convertir a diccionario
            alumno_dict = {
                "alumno_id": alumno.Alumno_ID,
                "nombre": alumno.Nombre,
                "ci": alumno.CI,
                "promedio_calificaciones": alumno.Promedio_Calificaciones,
                "cantidad_competencias": alumno.Cantidad_Competencias,
                "cluster_kmeans": alumno.Cluster_KMeans,
                "cluster_dbscan": alumno.Cluster_DBSCAN,
                "recomendaciones_basicas": alumno.Recomendaciones_Basicas,
                "inteligencias": [
                    {
                        "tipo": intel.Tipo_Inteligencia,
                        "puntaje": intel.Puntaje
                    } for intel in inteligencias
                ],
                "calificaciones": [
                    {
                        "competencia": cal.competencia.Codigo_Competencia,
                        "calificacion": cal.Calificacion,
                        "descripcion": cal.competencia.Descripcion
                    } for cal in calificaciones
                ]
            }
            
            enriched_alumnos.append(alumno_dict)
        
        return enriched_alumnos
        
    except Exception as e:
        logging.error(f"Error obteniendo alumnos con clusters: {str(e)}")
        raise

def get_cluster_statistics(db: Session):
    """
    Obtiene estadísticas de los clusters
    """
    try:
        # Estadísticas de K-Means
        kmeans_stats = db.query(
            models.Alumno.Cluster_KMeans,
            func.count(models.Alumno.Alumno_ID).label('count'),
            func.avg(models.Alumno.CI).label('avg_ci'),
            func.avg(models.Alumno.Promedio_Calificaciones).label('avg_grades')
        ).filter(models.Alumno.Cluster_KMeans.isnot(None)).group_by(models.Alumno.Cluster_KMeans).all()
        
        # Estadísticas de DBSCAN
        dbscan_stats = db.query(
            models.Alumno.Cluster_DBSCAN,
            func.count(models.Alumno.Alumno_ID).label('count'),
            func.avg(models.Alumno.CI).label('avg_ci'),
            func.avg(models.Alumno.Promedio_Calificaciones).label('avg_grades')
        ).filter(models.Alumno.Cluster_DBSCAN.isnot(None)).group_by(models.Alumno.Cluster_DBSCAN).all()
        
        return {
            "kmeans": [
                {
                    "cluster": stat.Cluster_KMeans,
                    "count": stat.count,
                    "avg_ci": float(stat.avg_ci) if stat.avg_ci is not None else 0,
                    "avg_grades": float(stat.avg_grades) if stat.avg_grades is not None else 0
                } for stat in kmeans_stats
            ],
            "dbscan": [
                {
                    "cluster": stat.Cluster_DBSCAN,
                    "count": stat.count,
                    "avg_ci": float(stat.avg_ci) if stat.avg_ci is not None else 0,
                    "avg_grades": float(stat.avg_grades) if stat.avg_grades is not None else 0
                } for stat in dbscan_stats
            ]
        }
        
    except Exception as e:
        logging.error(f"Error obteniendo estadísticas de clusters: {str(e)}")
        raise

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

def get_profesor_by_dni(db: Session, dni: str):
    return db.query(models.Profesor).filter(models.Profesor.DNI == dni).first()

def get_profesor_by_dni_or_name(db: Session, identifier: str):
    """Busca un profesor por DNI o por nombre"""
    return db.query(models.Profesor).filter(
        (models.Profesor.DNI == identifier) | 
        (models.Profesor.Nombre.ilike(f"%{identifier}%"))
    ).first()

def get_profesor(db: Session, profesor_id: int):
    """Obtener profesor por ID"""
    return db.query(models.Profesor).filter(models.Profesor.Profesor_ID == profesor_id).first()

def get_profesores(db: Session, skip: int = 0, limit: int = 100):
    """Obtener lista de profesores"""
    return db.query(models.Profesor).offset(skip).limit(limit).all()

def create_profesor(db: Session, profesor: profesor_schema.ProfesorCreate):
    hashed_password = get_password_hash(profesor.Contrasena)
    db_profesor = models.Profesor(
        Nombre=profesor.Nombre,
        DNI=profesor.DNI,
        Contrasena_Hash=hashed_password.encode('utf-8')  # Guardar como bytes
    )
    db.add(db_profesor)
    db.commit()
    db.refresh(db_profesor)
    return db_profesor

def update_profesor(db: Session, profesor_id: int, profesor: profesor_schema.ProfesorUpdate):
    """Actualizar información de un profesor"""
    db_profesor = get_profesor(db, profesor_id=profesor_id)
    if not db_profesor:
        return None
    
    if profesor.Nombre is not None:
        db_profesor.Nombre = profesor.Nombre
    if profesor.DNI is not None:
        db_profesor.DNI = profesor.DNI
    if profesor.Contrasena is not None:
        hashed_password = get_password_hash(profesor.Contrasena)
        db_profesor.Contrasena_Hash = hashed_password.encode('utf-8')
    
    db.commit()
    db.refresh(db_profesor)
    return db_profesor

def delete_profesor(db: Session, profesor_id: int):
    """Eliminar un profesor"""
    db_profesor = get_profesor(db, profesor_id=profesor_id)
    if not db_profesor:
        return False
    
    db.delete(db_profesor)
    db.commit()
    return True

def get_profesor_cursos(db: Session, profesor_id: int):
    """Obtener cursos asignados a un profesor"""
    cursos = db.query(models.Curso).join(
        models.ProfesorCurso
    ).filter(
        models.ProfesorCurso.Profesor_ID == profesor_id
    ).all()
    return cursos

def asignar_curso_profesor(db: Session, profesor_id: int, curso_id: int):
    """Asignar un curso a un profesor"""
    try:
        # Verificar que el profesor y curso existen
        profesor = get_profesor(db, profesor_id=profesor_id)
        curso = get_curso(db, curso_id=curso_id)
        
        if not profesor or not curso:
            return False
        
        # Verificar que no esté ya asignado
        asignacion_existente = db.query(models.ProfesorCurso).filter(
            models.ProfesorCurso.Profesor_ID == profesor_id,
            models.ProfesorCurso.Curso_ID == curso_id
        ).first()
        
        if asignacion_existente:
            return False
        
        # Crear nueva asignación
        nueva_asignacion = models.ProfesorCurso(
            Profesor_ID=profesor_id,
            Curso_ID=curso_id
        )
        db.add(nueva_asignacion)
        db.commit()
        return True
        
    except Exception as e:
        logging.error(f"Error asignando curso a profesor: {str(e)}")
        return False

def desasignar_curso_profesor(db: Session, profesor_id: int, curso_id: int):
    """Desasignar un curso de un profesor"""
    try:
        asignacion = db.query(models.ProfesorCurso).filter(
            models.ProfesorCurso.Profesor_ID == profesor_id,
            models.ProfesorCurso.Curso_ID == curso_id
        ).first()
        
        if not asignacion:
            return False
        
        db.delete(asignacion)
        db.commit()
        return True
        
    except Exception as e:
        logging.error(f"Error desasignando curso de profesor: {str(e)}")
        return False

def get_cursos_disponibles(db: Session):
    """Obtener todos los cursos disponibles"""
    return db.query(models.Curso).all()

def get_profesor_estadisticas(db: Session, profesor_id: int):
    """Obtener estadísticas de un profesor"""
    try:
        profesor = get_profesor(db, profesor_id=profesor_id)
        if not profesor:
            return None
        
        # Obtener cursos asignados
        cursos_asignados = get_profesor_cursos(db, profesor_id=profesor_id)
        
        # Obtener estadísticas de alumnos y calificaciones
        # (Esto dependerá de cómo quieras calcular las estadísticas)
        total_cursos = len(cursos_asignados)
        total_alumnos = 0  # Implementar según lógica de negocio
        promedio_calificaciones = 0.0  # Implementar según lógica de negocio
        
        return {
            "profesor_id": profesor_id,
            "nombre": profesor.Nombre,
            "total_cursos": total_cursos,
            "cursos_asignados": cursos_asignados,
            "total_alumnos": total_alumnos,
            "promedio_calificaciones": promedio_calificaciones
        }
        
    except Exception as e:
        logging.error(f"Error obteniendo estadísticas del profesor: {str(e)}")
        return None

# Funciones para Conversaciones de IA
def create_conversacion_message(db: Session, conversacion: conversacion_schema.ConversacionCreate, profesor_id: int, contexto_alumno: str = None):
    """Crear un nuevo mensaje en la conversación de IA"""
    db_conversacion = models.ConversacionIA(
        Alumno_ID=conversacion.alumno_id,
        Profesor_ID=profesor_id,
        Mensaje=conversacion.mensaje,
        Es_Usuario=1 if conversacion.es_usuario else 0,
        Fecha_Creacion=datetime.now().isoformat(),
        Contexto_Alumno=contexto_alumno
    )
    db.add(db_conversacion)
    db.commit()
    db.refresh(db_conversacion)
    return db_conversacion

def get_conversacion_history(db: Session, alumno_id: int, profesor_id: int):
    """Obtener el historial completo de conversación de un alumno específico"""
    conversaciones = db.query(models.ConversacionIA).filter(
        models.ConversacionIA.Alumno_ID == alumno_id,
        models.ConversacionIA.Profesor_ID == profesor_id
    ).order_by(models.ConversacionIA.Fecha_Creacion).all()
    
    return conversaciones

def get_alumno_conversacion_context(db: Session, alumno_id: int):
    """Obtener el contexto más reciente de un alumno para la IA"""
    # Obtener datos del alumno
    alumno = get_alumno(db, alumno_id)
    if not alumno:
        return None
    
    # Obtener inteligencias
    inteligencias = db.query(models.Inteligencia).filter(
        models.Inteligencia.Alumno_ID == alumno_id
    ).all()
    
    # Obtener calificaciones
    calificaciones = db.query(models.AlumnoCompetencia).join(
        models.CompetenciaPlantilla
    ).filter(
        models.AlumnoCompetencia.Alumno_ID == alumno_id
    ).all()
    
    # Determinar categoría del CI basada en el valor
    ci_categoria = ""
    if alumno.CI:
        if alumno.CI >= 130:
            ci_categoria = "Muy Superior"
        elif alumno.CI >= 120:
            ci_categoria = "Superior"
        elif alumno.CI >= 110:
            ci_categoria = "Arriba del Promedio"
        elif alumno.CI >= 90:
            ci_categoria = "Promedio"
        elif alumno.CI >= 80:
            ci_categoria = "Abajo del Promedio"
        elif alumno.CI >= 70:
            ci_categoria = "Bajo"
        else:
            ci_categoria = "Muy Bajo"
    
    context = {
        "alumno_id": alumno.Alumno_ID,
        "nombre": alumno.Nombre,
        "ci": alumno.CI,
        "categoria_ci": ci_categoria,
        "inteligencias": [
            {
                "tipo": intel.Tipo_Inteligencia,
                "puntaje": intel.Puntaje
            } for intel in inteligencias
        ],
        "calificaciones": [
            {
                "competencia": cal.competencia.Codigo_Competencia,
                "calificacion": cal.Calificacion,
                "descripcion": cal.competencia.Descripcion
            } for cal in calificaciones
        ],
        "recomendaciones_basicas": alumno.Recomendaciones_Basicas
    }
    
    return context

def clear_conversacion_alumno(db: Session, alumno_id: int, profesor_id: int):
    """Limpiar toda la conversación de un alumno específico"""
    db.query(models.ConversacionIA).filter(
        models.ConversacionIA.Alumno_ID == alumno_id,
        models.ConversacionIA.Profesor_ID == profesor_id
    ).delete()
    db.commit()
    return True
