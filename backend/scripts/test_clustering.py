#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del clustering
"""

import sys
import os
import requests
import json
import time

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import database, models
from app.services.clustering_service import clustering_service

def test_clustering_service():
    """Prueba el servicio de clustering directamente"""
    print("🧪 Probando servicio de clustering...")
    
    try:
        # Crear sesión de base de datos
        db = database.SessionLocal()
        
        # Obtener datos de alumnos
        from app.database import crud
        alumnos_data = crud.get_alumnos_with_clusters(db)
        
        if not alumnos_data:
            print("❌ No hay alumnos para procesar clustering")
            return False
        
        print(f"📊 Procesando clustering para {len(alumnos_data)} alumnos...")
        
        # Procesar clustering
        start_time = time.time()
        clustering_results = clustering_service.process_all_clustering(alumnos_data)
        end_time = time.time()
        
        if not clustering_results["success"]:
            print(f"❌ Error en clustering: {clustering_results['error']}")
            return False
        
        print(f"✅ Clustering completado en {end_time - start_time:.2f} segundos")
        print(f"📈 Alumnos procesados: {clustering_results['alumnos_processed']}")
        
        # Mostrar análisis
        kmeans_analysis = clustering_results["clusters"]["kmeans"]["analysis"]
        dbscan_analysis = clustering_results["clusters"]["dbscan"]["analysis"]
        
        print(f"\n📊 Análisis K-Means:")
        print(f"   - Clusters: {kmeans_analysis['n_clusters']}")
        print(f"   - Distribución: {kmeans_analysis['cluster_distribution']}")
        
        print(f"\n📊 Análisis DBSCAN:")
        print(f"   - Clusters: {dbscan_analysis['n_clusters']}")
        print(f"   - Distribución: {dbscan_analysis['cluster_distribution']}")
        
        # Mostrar recomendaciones
        kmeans_recs = clustering_results["clusters"]["kmeans"]["recommendations"]
        dbscan_recs = clustering_results["clusters"]["dbscan"]["recommendations"]
        
        print(f"\n💡 Recomendaciones K-Means:")
        for insight in kmeans_recs["general_insights"]:
            print(f"   - {insight}")
        
        print(f"\n💡 Recomendaciones DBSCAN:")
        for insight in dbscan_recs["general_insights"]:
            print(f"   - {insight}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de clustering: {str(e)}")
        return False

def test_clustering_api():
    """Prueba la API de clustering"""
    print("\n🌐 Probando API de clustering...")
    
    base_url = "http://127.0.0.1:8001/api"
    
    try:
        # Probar endpoint de procesamiento
        print("📤 Enviando solicitud de procesamiento...")
        response = requests.post(f"{base_url}/clustering/process", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Procesamiento exitoso")
            print(f"   - Mensaje: {result['message']}")
            print(f"   - Alumnos procesados: {result['alumnos_procesados']}")
            print(f"   - Alumnos actualizados: {result['alumnos_actualizados']}")
        else:
            print(f"❌ Error en procesamiento: {response.status_code}")
            print(f"   - Respuesta: {response.text}")
            return False
        
        # Probar endpoint de estadísticas
        print("\n📊 Obteniendo estadísticas...")
        response = requests.get(f"{base_url}/clustering/statistics")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas")
            print(f"   - K-Means clusters: {len(stats['statistics']['kmeans'])}")
            print(f"   - DBSCAN clusters: {len(stats['statistics']['dbscan'])}")
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
            return False
        
        # Probar endpoint de análisis
        print("\n📈 Obteniendo análisis completo...")
        response = requests.get(f"{base_url}/clustering/analysis")
        
        if response.status_code == 200:
            analysis = response.json()
            print("✅ Análisis obtenido")
            print(f"   - Total alumnos: {analysis['analysis']['total_alumnos']}")
            print(f"   - Clusters K-Means: {analysis['analysis']['clusters_kmeans']}")
            print(f"   - Clusters DBSCAN: {analysis['analysis']['clusters_dbscan']}")
        else:
            print(f"❌ Error obteniendo análisis: {response.status_code}")
            return False
        
        # Probar endpoint de alumnos con clusters
        print("\n👥 Obteniendo alumnos con clusters...")
        response = requests.get(f"{base_url}/clustering/alumnos")
        
        if response.status_code == 200:
            alumnos = response.json()
            print("✅ Alumnos obtenidos")
            print(f"   - Total: {alumnos['total']}")
            
            # Mostrar algunos ejemplos
            if alumnos['alumnos']:
                print("   - Ejemplos:")
                for i, alumno in enumerate(alumnos['alumnos'][:3]):
                    print(f"     {i+1}. {alumno['nombre']} - KMeans: {alumno['cluster_kmeans']}, DBSCAN: {alumno['cluster_dbscan']}")
        else:
            print(f"❌ Error obteniendo alumnos: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté ejecutándose en http://127.0.0.1:8001")
        return False
    except Exception as e:
        print(f"❌ Error en prueba de API: {str(e)}")
        return False

def test_cluster_data_integrity():
    """Prueba la integridad de los datos de clusters en la base de datos"""
    print("\n🔍 Verificando integridad de datos de clusters...")
    
    try:
        db = database.SessionLocal()
        
        # Verificar que los alumnos tengan clusters asignados
        alumnos = db.query(models.Alumno).all()
        
        alumnos_con_clusters = 0
        alumnos_sin_clusters = 0
        
        for alumno in alumnos:
            if alumno.Cluster_KMeans is not None and alumno.Cluster_DBSCAN is not None:
                alumnos_con_clusters += 1
            else:
                alumnos_sin_clusters += 1
        
        print(f"📊 Estadísticas de clusters:")
        print(f"   - Alumnos con clusters: {alumnos_con_clusters}")
        print(f"   - Alumnos sin clusters: {alumnos_sin_clusters}")
        print(f"   - Total alumnos: {len(alumnos)}")
        
        if alumnos_con_clusters > 0:
            print("✅ Hay alumnos con clusters asignados")
            
            # Verificar distribución de clusters
            kmeans_distribution = {}
            dbscan_distribution = {}
            
            for alumno in alumnos:
                if alumno.Cluster_KMeans is not None:
                    kmeans_distribution[alumno.Cluster_KMeans] = kmeans_distribution.get(alumno.Cluster_KMeans, 0) + 1
                if alumno.Cluster_DBSCAN is not None:
                    dbscan_distribution[alumno.Cluster_DBSCAN] = dbscan_distribution.get(alumno.Cluster_DBSCAN, 0) + 1
            
            print(f"   - Distribución K-Means: {kmeans_distribution}")
            print(f"   - Distribución DBSCAN: {dbscan_distribution}")
            
        else:
            print("⚠️  No hay alumnos con clusters asignados")
        
        db.close()
        return alumnos_con_clusters > 0
        
    except Exception as e:
        print(f"❌ Error verificando integridad: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de clustering...")
    print("=" * 50)
    
    # Prueba 1: Servicio de clustering
    test1_success = test_clustering_service()
    
    # Prueba 2: API de clustering
    test2_success = test_clustering_api()
    
    # Prueba 3: Integridad de datos
    test3_success = test_cluster_data_integrity()
    
    print("\n" + "=" * 50)
    print("📋 Resumen de pruebas:")
    print(f"   - Servicio de clustering: {'✅ PASÓ' if test1_success else '❌ FALLÓ'}")
    print(f"   - API de clustering: {'✅ PASÓ' if test2_success else '❌ FALLÓ'}")
    print(f"   - Integridad de datos: {'✅ PASÓ' if test3_success else '❌ FALLÓ'}")
    
    if test1_success and test2_success and test3_success:
        print("\n🎉 ¡Todas las pruebas pasaron! El clustering está funcionando correctamente.")
        return True
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 