import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.database import crud, database, models
from app.services.clustering_service import clustering_service

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/clustering",
    tags=["clustering"],
)

@router.post("/process")
async def process_clustering(db: Session = Depends(database.get_db)):
    """
    Procesa clustering de todos los alumnos y actualiza la base de datos
    """
    try:
        logger.info("Iniciando procesamiento de clustering")
        
        # Obtener todos los alumnos con datos enriquecidos
        alumnos_data = crud.get_alumnos_with_clusters(db)
        
        if not alumnos_data:
            raise HTTPException(status_code=404, detail="No hay alumnos para procesar")
        
        logger.info(f"Procesando clustering para {len(alumnos_data)} alumnos")
        
        # Procesar clustering
        clustering_results = clustering_service.process_all_clustering(alumnos_data)
        
        if not clustering_results["success"]:
            raise HTTPException(status_code=500, detail=clustering_results["error"])
        
        # Actualizar clusters en la base de datos
        updated_count = crud.update_all_alumno_clusters(db, clustering_results)
        
        logger.info(f"Clustering completado: {updated_count} alumnos actualizados")
        
        return {
            "success": True,
            "message": f"Clustering procesado exitosamente para {updated_count} alumnos",
            "alumnos_procesados": clustering_results["alumnos_processed"],
            "alumnos_actualizados": updated_count,
            "analisis": {
                "kmeans": clustering_results["clusters"]["kmeans"]["analysis"],
                "dbscan": clustering_results["clusters"]["dbscan"]["analysis"]
            },
            "recomendaciones": {
                "kmeans": clustering_results["clusters"]["kmeans"]["recommendations"],
                "dbscan": clustering_results["clusters"]["dbscan"]["recommendations"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en procesamiento de clustering: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/statistics")
async def get_cluster_statistics(db: Session = Depends(database.get_db)):
    """
    Obtiene estadísticas de los clusters actuales
    """
    try:
        stats = crud.get_cluster_statistics(db)
        
        return {
            "success": True,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas de clusters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/alumnos")
async def get_alumnos_with_clusters(db: Session = Depends(database.get_db)):
    """
    Obtiene todos los alumnos con información de clusters
    """
    try:
        alumnos = crud.get_alumnos_with_clusters(db)
        
        return {
            "success": True,
            "alumnos": alumnos,
            "total": len(alumnos)
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo alumnos con clusters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/alumnos/{alumno_id}")
async def get_alumno_clusters(alumno_id: int, db: Session = Depends(database.get_db)):
    """
    Obtiene información de clusters de un alumno específico
    """
    try:
        alumno = crud.get_alumno(db, alumno_id)
        
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
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
        
        alumno_data = {
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
        
        return {
            "success": True,
            "alumno": alumno_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo clusters del alumno {alumno_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/analysis")
async def get_clustering_analysis(db: Session = Depends(database.get_db)):
    """
    Obtiene un análisis completo de los clusters actuales
    """
    try:
        # Obtener estadísticas
        stats = crud.get_cluster_statistics(db)
        
        # Obtener todos los alumnos
        alumnos = crud.get_alumnos_with_clusters(db)
        
        # Procesar análisis adicional
        analysis = {
            "total_alumnos": len(alumnos),
            "clusters_kmeans": len(set(alumno["cluster_kmeans"] for alumno in alumnos)),
            "clusters_dbscan": len(set(alumno["cluster_dbscan"] for alumno in alumnos)),
            "estadisticas": stats,
            "distribucion_kmeans": {},
            "distribucion_dbscan": {}
        }
        
        # Calcular distribución de clusters
        for alumno in alumnos:
            kmeans_cluster = alumno["cluster_kmeans"]
            dbscan_cluster = alumno["cluster_dbscan"]
            
            analysis["distribucion_kmeans"][f"Cluster {kmeans_cluster}"] = \
                analysis["distribucion_kmeans"].get(f"Cluster {kmeans_cluster}", 0) + 1
            
            analysis["distribucion_dbscan"][f"Cluster {dbscan_cluster}"] = \
                analysis["distribucion_dbscan"].get(f"Cluster {dbscan_cluster}", 0) + 1
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo análisis de clustering: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}") 