import sqlite3
import logging
import os
import sys

# Agregar el directorio padre al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_calificaciones():
    """Corregir calificaciones que están como números en lugar de letras"""
    
    # Conectar a la base de datos (ruta relativa desde scripts/)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'bdalumnas.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar calificaciones actuales
        cursor.execute("SELECT AlumnoCompetencia_ID, Calificacion FROM AlumnoCompetencia LIMIT 10")
        calificaciones_actuales = cursor.fetchall()
        
        logger.info("Calificaciones actuales (primeras 10):")
        for cal_id, cal in calificaciones_actuales:
            logger.info(f"ID: {cal_id}, Calificación: {cal} (tipo: {type(cal)})")
        
        # Mapeo de números a letras
        mapeo_numeros_a_letras = {
            1: 'D',
            2: 'C', 
            3: 'B',
            4: 'A',
            1.0: 'D',
            2.0: 'C',
            3.0: 'B',
            4.0: 'A'
        }
        
        # Obtener todas las calificaciones
        cursor.execute("SELECT AlumnoCompetencia_ID, Calificacion FROM AlumnoCompetencia")
        todas_calificaciones = cursor.fetchall()
        
        calificaciones_corregidas = 0
        
        for cal_id, cal in todas_calificaciones:
            # Verificar si la calificación es un número
            if isinstance(cal, (int, float)) or (isinstance(cal, str) and cal.isdigit()):
                # Convertir a número si es string
                if isinstance(cal, str):
                    cal_num = float(cal)
                else:
                    cal_num = cal
                
                # Mapear a letra
                nueva_cal = mapeo_numeros_a_letras.get(cal_num, 'C')  # Default a 'C' si no está en el mapeo
                
                # Actualizar en la base de datos
                cursor.execute(
                    "UPDATE AlumnoCompetencia SET Calificacion = ? WHERE AlumnoCompetencia_ID = ?",
                    (nueva_cal, cal_id)
                )
                
                calificaciones_corregidas += 1
                logger.info(f"Corregida calificación ID {cal_id}: {cal} -> {nueva_cal}")
        
        # Confirmar cambios
        conn.commit()
        
        logger.info(f"Proceso completado. {calificaciones_corregidas} calificaciones corregidas.")
        
        # Verificar resultado
        cursor.execute("SELECT AlumnoCompetencia_ID, Calificacion FROM AlumnoCompetencia LIMIT 10")
        calificaciones_finales = cursor.fetchall()
        
        logger.info("Calificaciones después de la corrección (primeras 10):")
        for cal_id, cal in calificaciones_finales:
            logger.info(f"ID: {cal_id}, Calificación: {cal}")
        
        # Estadísticas
        cursor.execute("SELECT Calificacion, COUNT(*) FROM AlumnoCompetencia GROUP BY Calificacion")
        estadisticas = cursor.fetchall()
        
        logger.info("Estadísticas de calificaciones:")
        for cal, count in estadisticas:
            logger.info(f"Calificación {cal}: {count} registros")
        
    except Exception as e:
        logger.error(f"Error durante la corrección: {str(e)}")
        conn.rollback()
        raise e
    finally:
        conn.close()

def verificar_calificaciones():
    """Verificar el estado actual de las calificaciones"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'bdalumnas.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Obtener estadísticas
        cursor.execute("SELECT Calificacion, COUNT(*) FROM AlumnoCompetencia GROUP BY Calificacion")
        estadisticas = cursor.fetchall()
        
        logger.info("Estado actual de calificaciones:")
        for cal, count in estadisticas:
            logger.info(f"Calificación '{cal}' (tipo: {type(cal)}): {count} registros")
        
        # Verificar si hay números
        cursor.execute("SELECT COUNT(*) FROM AlumnoCompetencia WHERE Calificacion IN ('1', '2', '3', '4', '1.0', '2.0', '3.0', '4.0')")
        numeros_count = cursor.fetchone()[0]
        
        if numeros_count > 0:
            logger.warning(f"Se encontraron {numeros_count} calificaciones como números que necesitan corrección")
        else:
            logger.info("Todas las calificaciones están en formato correcto (A, B, C, D)")
            
    except Exception as e:
        logger.error(f"Error durante la verificación: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== Verificación inicial ===")
    verificar_calificaciones()
    
    print("\n=== Iniciando corrección ===")
    fix_calificaciones()
    
    print("\n=== Verificación final ===")
    verificar_calificaciones() 