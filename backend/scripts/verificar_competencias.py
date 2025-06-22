import sqlite3
import logging
import os
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verificar_competencias():
    """Verificar el estado de las competencias en la base de datos"""
    
    # Conectar a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), '..', 'bdalumnas.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Obtener todas las competencias
        cursor.execute("""
            SELECT cp.CompetenciaPlantilla_ID, cp.Codigo_Competencia, cp.Descripcion, c.Nombre as Curso
            FROM CompetenciaPlantilla cp
            LEFT JOIN Cursos c ON cp.Curso_ID = c.Curso_ID
            ORDER BY cp.Codigo_Competencia
        """)
        competencias = cursor.fetchall()
        
        logger.info(f"Total de competencias en la base de datos: {len(competencias)}")
        
        # Analizar competencias sin descripción
        sin_descripcion = []
        con_descripcion = []
        
        for comp_id, codigo, descripcion, curso in competencias:
            if not descripcion or descripcion.strip() == "":
                sin_descripcion.append((comp_id, codigo, curso))
            else:
                con_descripcion.append((comp_id, codigo, descripcion, curso))
        
        logger.info(f"Competencias CON descripción: {len(con_descripcion)}")
        logger.info(f"Competencias SIN descripción: {len(sin_descripcion)}")
        
        if sin_descripcion:
            logger.warning("Competencias que necesitan descripción:")
            for comp_id, codigo, curso in sin_descripcion:
                logger.warning(f"  - ID {comp_id}: {codigo} (Curso: {curso})")
        
        # Mostrar algunas competencias con descripción como ejemplo
        if con_descripcion:
            logger.info("Ejemplos de competencias con descripción:")
            for comp_id, codigo, descripcion, curso in con_descripcion[:5]:
                logger.info(f"  - {codigo}: {descripcion}")
        
        # Agrupar por curso
        cursor.execute("""
            SELECT c.Nombre as Curso, COUNT(cp.CompetenciaPlantilla_ID) as Total,
                   SUM(CASE WHEN cp.Descripcion IS NULL OR cp.Descripcion = '' THEN 1 ELSE 0 END) as SinDescripcion
            FROM Cursos c
            LEFT JOIN CompetenciaPlantilla cp ON c.Curso_ID = cp.Curso_ID
            GROUP BY c.Curso_ID, c.Nombre
            ORDER BY c.Nombre
        """)
        cursos_stats = cursor.fetchall()
        
        logger.info("\nEstadísticas por curso:")
        for curso, total, sin_desc in cursos_stats:
            logger.info(f"  - {curso}: {total} competencias ({sin_desc} sin descripción)")
        
        return {
            "total_competencias": len(competencias),
            "con_descripcion": len(con_descripcion),
            "sin_descripcion": len(sin_descripcion),
            "competencias_sin_desc": sin_descripcion,
            "cursos_stats": cursos_stats
        }
        
    except Exception as e:
        logger.error(f"Error durante la verificación: {str(e)}")
        raise e
    finally:
        conn.close()

def generar_mapeo_actualizado():
    """Generar un mapeo actualizado de competencias basado en la base de datos"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'bdalumnas.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Obtener competencias sin descripción
        cursor.execute("""
            SELECT cp.Codigo_Competencia, c.Nombre as Curso
            FROM CompetenciaPlantilla cp
            LEFT JOIN Cursos c ON cp.Curso_ID = c.Curso_ID
            WHERE cp.Descripcion IS NULL OR cp.Descripcion = ''
            ORDER BY cp.Codigo_Competencia
        """)
        competencias_sin_desc = cursor.fetchall()
        
        logger.info("Generando mapeo para competencias sin descripción:")
        
        mapeo_actualizado = {}
        
        for codigo, curso in competencias_sin_desc:
            # Generar descripción basada en el código
            descripcion = generar_descripcion_por_codigo(codigo, curso)
            mapeo_actualizado[codigo] = descripcion
            logger.info(f"  '{codigo}': '{descripcion}',")
        
        return mapeo_actualizado
        
    except Exception as e:
        logger.error(f"Error generando mapeo: {str(e)}")
        raise e
    finally:
        conn.close()

def generar_descripcion_por_codigo(codigo, curso):
    """Generar una descripción basada en el código de competencia"""
    
    # Mapeo de códigos a descripciones
    mapeo_base = {
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
        "1_quechua_c3": "Escribe diversos tipos de textos en quechua como segunda lengua"
    }
    
    # Si existe en el mapeo base, usarlo
    if codigo in mapeo_base:
        return mapeo_base[codigo]
    
    # Si no, generar una descripción genérica basada en el código
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
            "quechua": "Quechua"
        }
        
        materia_nombre = materias.get(materia, materia.title())
        
        return f"Competencia {competencia} de {materia_nombre}"
    
    return f"Descripción para {codigo}"

if __name__ == "__main__":
    print("=== Verificación de Competencias ===")
    stats = verificar_competencias()
    
    print("\n=== Generando Mapeo Actualizado ===")
    mapeo = generar_mapeo_actualizado()
    
    if mapeo:
        print("\nMapeo actualizado para agregar a excel_processor.py:")
        print("COMPETENCIAS_DESC = {")
        for codigo, descripcion in mapeo.items():
            print(f'    "{codigo}": "{descripcion}",')
        print("}")
    else:
        print("Todas las competencias ya tienen descripción.") 