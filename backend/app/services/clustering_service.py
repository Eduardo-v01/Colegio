import logging
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import Dict, List, Tuple
import json

logger = logging.getLogger(__name__)

class ClusteringService:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        
    def prepare_data_for_clustering(self, alumnos_data: List[Dict]) -> Tuple[np.ndarray, List[int]]:
        """
        Prepara los datos de los alumnos para clustering
        """
        try:
            features = []
            alumno_ids = []
            
            for alumno in alumnos_data:
                # Extraer características numéricas
                features_row = []
                
                # CI (normalizado)
                ci = alumno.get('ci', 100)
                features_row.append(ci)
                
                # Inteligencias múltiples (promedio y máximo)
                inteligencias = alumno.get('inteligencias', [])
                if inteligencias:
                    puntajes = [intel['puntaje'] for intel in inteligencias]
                    features_row.extend([
                        np.mean(puntajes),  # Promedio
                        np.max(puntajes),   # Máximo
                        np.std(puntajes),   # Desviación estándar
                        len(puntajes)       # Cantidad de inteligencias
                    ])
                else:
                    features_row.extend([0, 0, 0, 0])
                
                # Calificaciones (convertir A=4, B=3, C=2, D=1)
                calificaciones = alumno.get('calificaciones', [])
                if calificaciones:
                    calif_numericas = []
                    for cal in calificaciones:
                        calif = cal.get('calificacion', 'C')
                        if calif == 'A':
                            calif_numericas.append(4)
                        elif calif == 'B':
                            calif_numericas.append(3)
                        elif calif == 'C':
                            calif_numericas.append(2)
                        elif calif == 'D':
                            calif_numericas.append(1)
                        else:
                            calif_numericas.append(2)  # Default
                    
                    features_row.extend([
                        np.mean(calif_numericas),  # Promedio calificaciones
                        np.max(calif_numericas),   # Mejor calificación
                        len(calif_numericas)       # Cantidad de calificaciones
                    ])
                else:
                    features_row.extend([2, 2, 0])
                
                # Promedio de calificaciones (si existe)
                promedio = alumno.get('promedio_calificaciones', 0)
                features_row.append(promedio)
                
                features.append(features_row)
                alumno_ids.append(alumno['alumno_id'])
            
            # Convertir a numpy array
            features_array = np.array(features)
            
            # Normalizar datos
            features_scaled = self.scaler.fit_transform(features_array)
            
            logger.info(f"Datos preparados para clustering: {features_scaled.shape}")
            return features_scaled, alumno_ids
            
        except Exception as e:
            logger.error(f"Error preparando datos para clustering: {str(e)}")
            raise
    
    def apply_kmeans_clustering(self, features: np.ndarray, n_clusters: int = 3) -> np.ndarray:
        """
        Aplica clustering K-Means
        """
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(features)
            
            logger.info(f"K-Means clustering aplicado: {n_clusters} clusters")
            return clusters
            
        except Exception as e:
            logger.error(f"Error en K-Means clustering: {str(e)}")
            raise
    
    def apply_dbscan_clustering(self, features: np.ndarray, eps: float = 0.5, min_samples: int = 2) -> np.ndarray:
        """
        Aplica clustering DBSCAN
        """
        try:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            clusters = dbscan.fit_predict(features)
            
            # DBSCAN puede devolver -1 para puntos de ruido, convertimos a números positivos
            unique_clusters = np.unique(clusters)
            cluster_mapping = {cluster: i for i, cluster in enumerate(unique_clusters)}
            clusters_mapped = np.array([cluster_mapping[c] for c in clusters])
            
            logger.info(f"DBSCAN clustering aplicado: {len(unique_clusters)} clusters")
            return clusters_mapped
            
        except Exception as e:
            logger.error(f"Error en DBSCAN clustering: {str(e)}")
            raise
    
    def analyze_clusters(self, features: np.ndarray, clusters: np.ndarray, 
                        cluster_type: str, alumnos_data: List[Dict]) -> Dict:
        """
        Analiza los clusters generados
        """
        try:
            analysis = {
                "cluster_type": cluster_type,
                "n_clusters": len(np.unique(clusters)),
                "cluster_distribution": {},
                "cluster_characteristics": {}
            }
            
            # Distribución de clusters
            unique, counts = np.unique(clusters, return_counts=True)
            for cluster, count in zip(unique, counts):
                analysis["cluster_distribution"][f"Cluster {cluster}"] = int(count)
            
            # Características de cada cluster
            for cluster in unique:
                cluster_mask = clusters == cluster
                cluster_features = features[cluster_mask]
                
                # Calcular estadísticas del cluster
                cluster_stats = {
                    "size": int(np.sum(cluster_mask)),
                    "mean_ci": float(np.mean(cluster_features[:, 0])),
                    "mean_intelligence": float(np.mean(cluster_features[:, 1])),
                    "mean_grades": float(np.mean(cluster_features[:, 5]))
                }
                
                analysis["cluster_characteristics"][f"Cluster {cluster}"] = cluster_stats
            
            logger.info(f"Análisis de clusters {cluster_type} completado")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando clusters: {str(e)}")
            raise
    
    def generate_cluster_recommendations(self, cluster_analysis: Dict, 
                                       cluster_type: str) -> Dict:
        """
        Genera recomendaciones basadas en el análisis de clusters
        """
        try:
            recommendations = {
                "cluster_type": cluster_type,
                "general_insights": [],
                "cluster_recommendations": {}
            }
            
            n_clusters = cluster_analysis["n_clusters"]
            
            # Insights generales
            if n_clusters == 2:
                recommendations["general_insights"].append(
                    "Se identificaron dos grupos principales de alumnos con perfiles distintos"
                )
            elif n_clusters == 3:
                recommendations["general_insights"].append(
                    "Se identificaron tres grupos de alumnos: alto, medio y bajo rendimiento"
                )
            else:
                recommendations["general_insights"].append(
                    f"Se identificaron {n_clusters} grupos de alumnos con características únicas"
                )
            
            # Recomendaciones por cluster
            for cluster_name, stats in cluster_analysis["cluster_characteristics"].items():
                cluster_recs = []
                
                if stats["mean_ci"] > 110:
                    cluster_recs.append("Alumnos con alto potencial intelectual")
                elif stats["mean_ci"] < 90:
                    cluster_recs.append("Alumnos que requieren apoyo adicional")
                
                if stats["mean_intelligence"] > 7:
                    cluster_recs.append("Fortalezas en inteligencias múltiples")
                elif stats["mean_intelligence"] < 5:
                    cluster_recs.append("Oportunidad de desarrollo en inteligencias múltiples")
                
                if stats["mean_grades"] > 3:
                    cluster_recs.append("Buen rendimiento académico")
                elif stats["mean_grades"] < 2.5:
                    cluster_recs.append("Necesita mejorar el rendimiento académico")
                
                recommendations["cluster_recommendations"][cluster_name] = cluster_recs
            
            logger.info(f"Recomendaciones de clusters {cluster_type} generadas")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generando recomendaciones: {str(e)}")
            raise
    
    def process_all_clustering(self, alumnos_data: List[Dict]) -> Dict:
        """
        Procesa clustering completo para todos los alumnos
        """
        try:
            logger.info(f"Iniciando procesamiento de clustering para {len(alumnos_data)} alumnos")
            
            # Preparar datos
            features, alumno_ids = self.prepare_data_for_clustering(alumnos_data)
            
            # Aplicar K-Means
            kmeans_clusters = self.apply_kmeans_clustering(features)
            
            # Aplicar DBSCAN
            dbscan_clusters = self.apply_dbscan_clustering(features)
            
            # Analizar clusters
            kmeans_analysis = self.analyze_clusters(features, kmeans_clusters, "K-Means", alumnos_data)
            dbscan_analysis = self.analyze_clusters(features, dbscan_clusters, "DBSCAN", alumnos_data)
            
            # Generar recomendaciones
            kmeans_recommendations = self.generate_cluster_recommendations(kmeans_analysis, "K-Means")
            dbscan_recommendations = self.generate_cluster_recommendations(dbscan_analysis, "DBSCAN")
            
            # Preparar resultados
            results = {
                "success": True,
                "alumnos_processed": len(alumnos_data),
                "clusters": {
                    "kmeans": {
                        "clusters": kmeans_clusters.tolist(),
                        "alumno_ids": alumno_ids,
                        "analysis": kmeans_analysis,
                        "recommendations": kmeans_recommendations
                    },
                    "dbscan": {
                        "clusters": dbscan_clusters.tolist(),
                        "alumno_ids": alumno_ids,
                        "analysis": dbscan_analysis,
                        "recommendations": dbscan_recommendations
                    }
                }
            }
            
            logger.info("Procesamiento de clustering completado exitosamente")
            return results
            
        except Exception as e:
            logger.error(f"Error en procesamiento de clustering: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Instancia global del servicio
clustering_service = ClusteringService() 