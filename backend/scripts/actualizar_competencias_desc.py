import sqlite3
import logging
import os
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapeo completo de competencias
COMPETENCIAS_DESC_COMPLETO = {
    # Matemáticas
    "1_matematicas_c1": "Resuelve problemas de cantidad",
    "1_matematicas_c2": "Resuelve problemas de regularidad, equivalencia y cambio",
    "1_matematicas_c3": "Resuelve problemas de forma, movimiento y localización",
    "1_matematicas_c4": "Resuelve problemas de gestión de datos e incertidumbre",
    
    # Comunicación
    "1_comunicacion_c1": "Se comunica oralmente en su lengua materna",
    "1_comunicacion_c2": "Lee diversos tipos de textos escritos en lengua materna",
    "1_comunicacion_c3": "Escribe diversos tipos de textos en lengua materna",
    
    # Inglés
    "1_ingles_c1": "Se comunica oralmente en inglés como lengua extranjera",
    "1_ingles_c2": "Lee diversos tipos de textos escritos en inglés como lengua extranjera",
    "1_ingles_c3": "Escribe diversos tipos de textos en inglés como lengua extranjera",
    
    # Arte
    "1_arte_c1": "Aprecia de manera crítica manifestaciones artístico-culturales",
    "1_arte_c2": "Crea proyectos desde los lenguajes artísticos",
    
    # Ciencias Sociales
    "1_sociales_c1": "Construye interpretaciones históricas",
    "1_sociales_c2": "Gestiona responsablemente el espacio y el ambiente",
    "1_sociales_c3": "Gestiona responsablemente los recursos económicos",
    
    # Desarrollo Personal, Ciudadanía y Cívica
    "1_desarrollo_c1": "Construye su identidad",
    "1_desarrollo_c2": "Convive y participa democráticamente en la búsqueda del bien común",
    "1_Desarrollo personal, ciudadanía y cívica _c1": "Construye su identidad",
    "1_Desarrollo personal, ciudadanía y cívica _c2": "Convive y participa democráticamente en la búsqueda del bien común",
    
    # Educación Física
    "1_ef_c1": "Se desenvuelve de manera autónoma a través de su motricidad",
    "1_ef_c2": "Asume una vida saludable",
    "1_ef_c3": "Interactúa a través de sus habilidades sociomotrices",
    
    # Educación Religiosa
    "1_religion_c1": "Construye su identidad como persona humana, amada por Dios, digna, libre y trascendente",
    "1_religion_c2": "Asume la experiencia del encuentro personal y comunitario con Dios",
    
    # Ciencia y Tecnología
    "1_ciencia_c1": "Indaga mediante métodos científicos para construir conocimientos",
    "1_ciencia_c2": "Explica el mundo físico basándose en conocimientos científicos",
    "1_ciencia_c3": "Diseña y construye soluciones tecnológicas para resolver problemas",
    
    # Educación para el Trabajo
    "1_trabajo_c1": "Gestiona proyectos de emprendimiento económico o social",
    
    # Quechua
    "1_quechua_c1": "Se comunica oralmente en quechua como segunda lengua",
    "1_quechua_c2": "Lee diversos tipos de textos escritos en quechua como segunda lengua",
    "1_quechua_c3": "Escribe diversos tipos de textos en quechua como segunda lengua",
    
    # Códigos adicionales encontrados
    "1_tj": "Competencia de trabajo y juventud",
    "1_tj_c1": "Competencia de trabajo y juventud",
    "1_tj_c2": "Competencia de trabajo y juventud",
    
    # Códigos con espacios (limpiar)
    "1_Desarrollo personal, ciudadanía y cívica _c1": "Construye su identidad",
    "1_Desarrollo personal, ciudadanía y cívica _c2": "Convive y participa democráticamente en la búsqueda del bien común",
}

def limpiar_codigo_competencia(codigo):
    """Limpiar código de competencia eliminando espacios extra"""
    if codigo:
        # Eliminar espacios al inicio y final
        codigo_limpio = codigo.strip()
        # Reemplazar múltiples espacios por uno solo
        codigo_limpio = " ".join(codigo_limpio.split())
        return codigo_limpio
    return codigo

def actualizar_descripciones_competencias():
    """Actualizar las descripciones de competencias en la base de datos"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'bdalumnas.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Obtener todas las competencias
        cursor.execute("""
            SELECT CompetenciaPlantilla_ID, Codigo_Competencia, Descripcion
            FROM CompetenciaPlantilla
            ORDER BY Codigo_Competencia
        """)
        competencias = cursor.fetchall()
        
        logger.info(f"Total de competencias a procesar: {len(competencias)}")
        
        actualizadas = 0
        sin_cambios = 0
        
        for comp_id, codigo, descripcion_actual in competencias:
            codigo_limpio = limpiar_codigo_competencia(codigo)
            
            # Buscar descripción en el mapeo
            nueva_descripcion = COMPETENCIAS_DESC_COMPLETO.get(codigo_limpio)
            
            if nueva_descripcion:
                # Si la descripción actual está vacía o es diferente, actualizar
                if not descripcion_actual or descripcion_actual.strip() == "" or descripcion_actual != nueva_descripcion:
                    cursor.execute("""
                        UPDATE CompetenciaPlantilla 
                        SET Descripcion = ? 
                        WHERE CompetenciaPlantilla_ID = ?
                    """, (nueva_descripcion, comp_id))
                    
                    logger.info(f"Actualizada competencia {comp_id}: {codigo_limpio} -> {nueva_descripcion}")
                    actualizadas += 1
                else:
                    logger.info(f"Sin cambios en competencia {comp_id}: {codigo_limpio}")
                    sin_cambios += 1
            else:
                # Generar descripción genérica
                descripcion_generica = generar_descripcion_generica(codigo_limpio)
                cursor.execute("""
                    UPDATE CompetenciaPlantilla 
                    SET Descripcion = ? 
                    WHERE CompetenciaPlantilla_ID = ?
                """, (descripcion_generica, comp_id))
                
                logger.warning(f"Descripción genérica para competencia {comp_id}: {codigo_limpio} -> {descripcion_generica}")
                actualizadas += 1
        
        # Confirmar cambios
        conn.commit()
        
        logger.info(f"Proceso completado:")
        logger.info(f"  - Competencias actualizadas: {actualizadas}")
        logger.info(f"  - Sin cambios: {sin_cambios}")
        
        # Verificar resultado
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN Descripcion IS NULL OR Descripcion = '' THEN 1 ELSE 0 END) as sin_descripcion
            FROM CompetenciaPlantilla
        """)
        total, sin_desc = cursor.fetchone()
        
        logger.info(f"Estado final:")
        logger.info(f"  - Total competencias: {total}")
        logger.info(f"  - Sin descripción: {sin_desc}")
        
        return {
            "actualizadas": actualizadas,
            "sin_cambios": sin_cambios,
            "total": total,
            "sin_descripcion": sin_desc
        }
        
    except Exception as e:
        logger.error(f"Error durante la actualización: {str(e)}")
        conn.rollback()
        raise e
    finally:
        conn.close()

def generar_descripcion_generica(codigo):
    """Generar una descripción genérica basada en el código"""
    partes = codigo.split("_")
    if len(partes) >= 3:
        grado = partes[0]
        materia = partes[1]
        competencia = partes[2]
        
        # Mapeo de materias a nombres más legibles
        materias = {
            "matematicas": "Matemáticas",
            "comunicacion": "Comunicación",
            "ingles": "Inglés",
            "arte": "Arte",
            "sociales": "Ciencias Sociales",
            "desarrollo": "Desarrollo Personal",
            "ef": "Educación Física",
            "religion": "Educación Religiosa",
            "ciencia": "Ciencia y Tecnología",
            "trabajo": "Educación para el Trabajo",
            "quechua": "Quechua",
            "tj": "Trabajo y Juventud"
        }
        
        materia_nombre = materias.get(materia.lower(), materia.title())
        
        return f"Competencia {competencia} de {materia_nombre}"
    
    return f"Descripción para {codigo}"

def generar_mapeo_actualizado():
    """Generar el mapeo actualizado para excel_processor.py"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'bdalumnas.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Obtener todas las competencias con sus descripciones
        cursor.execute("""
            SELECT Codigo_Competencia, Descripcion
            FROM CompetenciaPlantilla
            WHERE Descripcion IS NOT NULL AND Descripcion != ''
            ORDER BY Codigo_Competencia
        """)
        competencias = cursor.fetchall()
        
        logger.info("Mapeo actualizado para excel_processor.py:")
        print("\n# Mapeo completo de competencias para excel_processor.py")
        print("COMPETENCIAS_DESC = {")
        
        for codigo, descripcion in competencias:
            print(f'    "{codigo}": "{descripcion}",')
        
        print("}")
        
        return competencias
        
    except Exception as e:
        logger.error(f"Error generando mapeo: {str(e)}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== Actualizando Descripciones de Competencias ===")
    resultado = actualizar_descripciones_competencias()
    
    print("\n=== Generando Mapeo Actualizado ===")
    generar_mapeo_actualizado() 