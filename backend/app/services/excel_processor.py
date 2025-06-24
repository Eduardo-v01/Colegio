import pandas as pd
from sqlalchemy.orm import Session
from app.database import models
from collections import defaultdict
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapeo de códigos de competencia a descripciones
COMPETENCIAS_DESC = {
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
    "1_arte_c1": "Aprecia de manera crítica manifestaciones artísticas",
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
    "1_Ciencia y tecnología_c1": "Competencia c1 de Ciencia Y Tecnología",
    "1_Ciencia y tecnología_c2": "Competencia c2 de Ciencia Y Tecnología",
    "1_Ciencia y tecnología_c3": "Competencia c3 de Ciencia Y Tecnología",
    
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
}

def procesar_excel(db: Session, file_path: str, modo_actualizacion: bool = True):
    """
    Procesa un archivo Excel que contiene notas, inteligencias y CI de alumnos,
    y actualiza la base de datos.
    """
    try:
        logger.info(f"Iniciando procesamiento del archivo: {file_path}. Modo actualización: {modo_actualizacion}")

        # --- 1. LECTURA DE HOJAS EXCEL ---
        try:
            notas_df = pd.read_excel(file_path, sheet_name="notas")
            logger.info(f"Hoja 'notas' cargada con {len(notas_df)} filas.")
        except Exception as e:
            raise ValueError(f"Error al leer la hoja 'notas': {e}")

        # Detectar automáticamente la hoja de inteligencias
        try:
            excel_file = pd.ExcelFile(file_path)
            hojas_disponibles = excel_file.sheet_names
            logger.info(f"Hojas disponibles en el archivo: {hojas_disponibles}")
            
            # Buscar hoja de inteligencias por nombre similar
            hoja_inteligencia = None
            palabras_clave = ['inteligencia', 'inteligencias', 'intel', 'multiple', 'múltiple', 'brain', 'cerebro']
            
            for hoja in hojas_disponibles:
                hoja_lower = hoja.lower()
                for palabra in palabras_clave:
                    if palabra in hoja_lower:
                        hoja_inteligencia = hoja
                        logger.info(f"Hoja de inteligencias detectada: '{hoja}'")
                        break
                if hoja_inteligencia:
                    break
            
            if hoja_inteligencia:
                intel_df = pd.read_excel(file_path, sheet_name=hoja_inteligencia)
                logger.info(f"Hoja '{hoja_inteligencia}' cargada con {len(intel_df)} filas.")
            else:
                logger.warning(f"No se encontró hoja de inteligencias. Hojas disponibles: {hojas_disponibles}")
                intel_df = pd.DataFrame()
                
        except Exception as e:
            logger.warning(f"No se pudo leer la hoja de inteligencias. Se continuará sin procesar inteligencias. Error: {e}")
            intel_df = pd.DataFrame()

        # Detectar automáticamente la hoja de CI
        try:
            # Buscar hoja de CI por nombre similar
            hoja_ci = None
            palabras_clave_ci = ['ci', 'coeficiente', 'intelectual', 'iq', 'intelligence', 'quotient']
            
            for hoja in hojas_disponibles:
                hoja_lower = hoja.lower()
                for palabra in palabras_clave_ci:
                    if palabra in hoja_lower:
                        hoja_ci = hoja
                        logger.info(f"Hoja de CI detectada: '{hoja}'")
                        break
                if hoja_ci:
                    break
            
            if hoja_ci:
                ci_df = pd.read_excel(file_path, sheet_name=hoja_ci)
                logger.info(f"Hoja '{hoja_ci}' cargada con {len(ci_df)} filas.")
            else:
                logger.warning(f"No se encontró hoja de CI. Hojas disponibles: {hojas_disponibles}")
                ci_df = pd.DataFrame()
                
        except Exception as e:
            logger.warning(f"No se pudo leer la hoja de CI. Se continuará sin procesar CI. Error: {e}")
            ci_df = pd.DataFrame()

        # --- 2. TRANSFORMACIÓN DE DATOS DE INTELIGENCIA ---
        intel_melted_df = pd.DataFrame()
        inteligencias_info = {
            "hoja_encontrada": False,
            "hoja_detectada": None,
            "hojas_disponibles": [],
            "columnas_requeridas": False,
            "tipos_encontrados": [],
            "registros_validos": 0,
            "alumnos_con_inteligencias": 0,
            "error_mensaje": None
        }
        
        # Información de CI
        ci_info = {
            "hoja_encontrada": False,
            "hoja_detectada": None,
            "columnas_requeridas": False,
            "registros_validos": 0,
            "alumnos_con_ci": 0,
            "error_mensaje": None
        }
        
        # Guardar información de hojas disponibles
        try:
            excel_file = pd.ExcelFile(file_path)
            inteligencias_info["hojas_disponibles"] = excel_file.sheet_names
        except:
            pass
        
        if not intel_df.empty:
            inteligencias_info["hoja_encontrada"] = True
            # Obtener el nombre de la hoja detectada
            try:
                excel_file = pd.ExcelFile(file_path)
                palabras_clave = ['inteligencia', 'inteligencias', 'intel', 'multiple', 'múltiple', 'brain', 'cerebro']
                for hoja in excel_file.sheet_names:
                    hoja_lower = hoja.lower()
                    for palabra in palabras_clave:
                        if palabra in hoja_lower:
                            inteligencias_info["hoja_detectada"] = hoja
                            break
                    if inteligencias_info["hoja_detectada"]:
                        break
            except:
                pass
            
            logger.info(f"Hoja de inteligencia encontrada: '{inteligencias_info['hoja_detectada']}' con {len(intel_df)} filas y columnas: {list(intel_df.columns)}")
            
            # Verificar columnas requeridas
            if "nom" in intel_df.columns and "grado_seccion" in intel_df.columns:
                inteligencias_info["columnas_requeridas"] = True
                intel_df['nom'] = intel_df['nom'].astype(str).str.strip()
                
                # Identificar columnas de tipos de inteligencia
                id_vars = ['grado_seccion', 'nom']
                value_vars = [col for col in intel_df.columns if col not in id_vars and not col.startswith("Unnamed")]
                inteligencias_info["tipos_encontrados"] = value_vars
                
                logger.info(f"Tipos de inteligencia encontrados: {value_vars}")
                
                if value_vars:
                    try:
                        intel_melted_df = intel_df.melt(
                            id_vars=id_vars,
                            value_vars=value_vars,
                            var_name='Tipo_Inteligencia',
                            value_name='Puntaje'
                        )
                        
                        # Limpiar y validar datos
                        registros_originales = len(intel_melted_df)
                        intel_melted_df.dropna(subset=['Puntaje'], inplace=True)
                        intel_melted_df = intel_melted_df[pd.to_numeric(intel_melted_df['Puntaje'], errors='coerce').notnull()]
                        intel_melted_df['Puntaje'] = intel_melted_df['Puntaje'].astype(float)
                        
                        inteligencias_info["registros_validos"] = len(intel_melted_df)
                        inteligencias_info["alumnos_con_inteligencias"] = len(intel_melted_df['nom'].unique())
                        
                        logger.info(f"Transformación exitosa: {registros_originales} registros originales, {len(intel_melted_df)} registros válidos")
                        logger.info(f"Alumnos con datos de inteligencia: {inteligencias_info['alumnos_con_inteligencias']}")
                        
                    except Exception as e:
                        inteligencias_info["error_mensaje"] = f"Error en transformación: {str(e)}"
                        logger.error(f"Error al transformar datos de inteligencia: {e}")
                else:
                    inteligencias_info["error_mensaje"] = "No se encontraron columnas de tipos de inteligencia válidas"
                    logger.warning("No se encontraron columnas de tipos de inteligencia en la hoja de inteligencia")
            else:
                inteligencias_info["error_mensaje"] = f"La hoja '{inteligencias_info['hoja_detectada']}' no contiene las columnas requeridas 'nom' y 'grado_seccion'"
                logger.error(f"La hoja de inteligencia debe contener 'nom' y 'grado_seccion'. No se procesará.")
        else:
            inteligencias_info["error_mensaje"] = f"No se pudo leer la hoja de inteligencias. Hojas disponibles: {inteligencias_info['hojas_disponibles']}"
            logger.warning(f"No se pudo leer la hoja de inteligencias. Hojas disponibles: {inteligencias_info['hojas_disponibles']}")

        # --- 3. TRANSFORMACIÓN DE DATOS DE CI ---
        if not ci_df.empty:
            ci_info["hoja_encontrada"] = True
            ci_info["hoja_detectada"] = hoja_ci
            
            logger.info(f"Hoja de CI encontrada: '{ci_info['hoja_detectada']}' con {len(ci_df)} filas y columnas: {list(ci_df.columns)}")
            
            # Verificar columnas requeridas para CI
            if "nom" in ci_df.columns and "ci" in ci_df.columns:
                ci_info["columnas_requeridas"] = True
                ci_df['nom'] = ci_df['nom'].astype(str).str.strip()
                
                try:
                    # Limpiar y validar datos de CI
                    ci_df_clean = ci_df[['nom', 'ci']].copy()
                    ci_df_clean = ci_df_clean.dropna(subset=['ci'])
                    ci_df_clean['ci'] = pd.to_numeric(ci_df_clean['ci'], errors='coerce')
                    ci_df_clean = ci_df_clean.dropna(subset=['ci'])
                    
                    # Convertir CI a entero
                    ci_df_clean['ci'] = ci_df_clean['ci'].astype(int)
                    
                    ci_info["registros_validos"] = len(ci_df_clean)
                    ci_info["alumnos_con_ci"] = len(ci_df_clean['nom'].unique())
                    
                    logger.info(f"CI procesados: {len(ci_df_clean)} registros válidos")
                    logger.info(f"Alumnos con CI: {ci_info['alumnos_con_ci']}")
                    
                except Exception as e:
                    ci_info["error_mensaje"] = f"Error en procesamiento de CI: {str(e)}"
                    logger.error(f"Error al procesar datos de CI: {e}")
            else:
                ci_info["error_mensaje"] = f"La hoja '{ci_info['hoja_detectada']}' no contiene las columnas requeridas 'nom' y 'ci'"
                logger.error(f"La hoja de CI debe contener 'nom' y 'ci'. No se procesará.")
        else:
            ci_info["error_mensaje"] = f"No se pudo leer la hoja de CI. Hojas disponibles: {inteligencias_info['hojas_disponibles']}"
            logger.warning(f"No se pudo leer la hoja de CI. Hojas disponibles: {inteligencias_info['hojas_disponibles']}")

        # --- 4. PROCESAR CURSOS Y COMPETENCIAS ---
        cursos_db = {c.Nombre: c.Curso_ID for c in db.query(models.Curso).all()}
        competencias_db = {c.Codigo_Competencia: c.CompetenciaPlantilla_ID for c in db.query(models.CompetenciaPlantilla).all()}
        
        competencia_cols = [col for col in notas_df.columns if col not in ["grado_seccion", "nom", "1_apreciacion_tutor"] and "_conclusion" not in col and not col.startswith("Unnamed")]
        
        for codigo_competencia in competencia_cols:
            partes = codigo_competencia.split("_")
            if len(partes) < 2: continue
            
            nombre_curso = partes[1]
            if nombre_curso not in cursos_db:
                curso_obj = models.Curso(Nombre=nombre_curso)
                db.add(curso_obj)
                db.flush()
                cursos_db[nombre_curso] = curso_obj.Curso_ID
                logger.info(f"Curso creado: {nombre_curso}")

            if codigo_competencia not in competencias_db:
                comp_obj = models.CompetenciaPlantilla(
                    Curso_ID=cursos_db[nombre_curso],
                    Codigo_Competencia=codigo_competencia,
                    Descripcion=COMPETENCIAS_DESC.get(codigo_competencia, "")
                )
                db.add(comp_obj)
                db.flush()
                competencias_db[codigo_competencia] = comp_obj.CompetenciaPlantilla_ID
                logger.info(f"Competencia creada: {codigo_competencia}")

        # --- 5. PROCESAR ALUMNOS Y CALIFICACIONES ---
        alumnos_procesados, alumnos_creados, alumnos_actualizados = 0, 0, 0
        nombre_a_id = {}
        
        for _, row in notas_df.iterrows():
            nombre = row.get("nom")
            if pd.isna(nombre) or str(nombre).strip() == "": continue
            
            nombre_limpio = str(nombre).strip()
            alumno_existente = db.query(models.Alumno).filter(models.Alumno.Nombre == nombre_limpio).first()
            
            alumno_obj = None
            if alumno_existente:
                if modo_actualizacion:
                    alumno_obj = alumno_existente
                    alumnos_actualizados += 1
                else:
                    nombre_a_id[nombre_limpio] = alumno_existente.Alumno_ID
                    continue 
            else:
                alumno_obj = models.Alumno(Nombre=nombre_limpio)
                db.add(alumno_obj)
                db.flush()
                alumnos_creados += 1
            
            nombre_a_id[nombre_limpio] = alumno_obj.Alumno_ID

            # Actualizar CI y Recomendaciones
            if not ci_df.empty and "nom" in ci_df.columns and "ci" in ci_df.columns:
                ci_row = ci_df[ci_df["nom"] == nombre]
                if not ci_row.empty:
                    try:
                        ci_valor = ci_row["ci"].values[0]
                        if pd.notna(ci_valor):
                            alumno_obj.CI = int(ci_valor)
                    except (ValueError, TypeError): 
                        pass
            
            alumno_obj.Recomendaciones_Basicas = str(row.get("1_apreciacion_tutor", "")).strip()

            # Actualizar Calificaciones
            if modo_actualizacion and alumno_existente:
                db.query(models.AlumnoCompetencia).filter(models.AlumnoCompetencia.Alumno_ID == alumno_obj.Alumno_ID).delete()

            for codigo_competencia in competencia_cols:
                if codigo_competencia in row and pd.notna(row[codigo_competencia]):
                    calif_str = str(row[codigo_competencia]).strip().upper()
                    mapeo_num = {'1': 'D', '2': 'C', '3': 'B', '4': 'A'}
                    calif_str = mapeo_num.get(calif_str.replace('.0', ''), calif_str)

                    if calif_str in ['A', 'B', 'C', 'D']:
                        db.add(models.AlumnoCompetencia(
                            Alumno_ID=alumno_obj.Alumno_ID,
                            CompetenciaPlantilla_ID=competencias_db[codigo_competencia],
                            Calificacion=calif_str
                        ))
            alumnos_procesados += 1

        # --- 6. PROCESAR INTELIGENCIAS MÚLTIPLES ---
        inteligencias_procesadas = 0
        if not intel_melted_df.empty:
            logger.info("Iniciando procesamiento de inteligencias múltiples.")
            
            # Contar inteligencias existentes antes de eliminar
            inteligencias_existentes = db.query(models.Inteligencia).filter(
                models.Inteligencia.Alumno_ID.in_(list(nombre_a_id.values()))
            ).count()
            
            ids_a_actualizar = [id for nombre, id in nombre_a_id.items() if nombre in intel_melted_df['nom'].unique()]
            if ids_a_actualizar:
                eliminadas = db.query(models.Inteligencia).filter(models.Inteligencia.Alumno_ID.in_(ids_a_actualizar)).delete(synchronize_session=False)
                logger.info(f"Eliminadas {eliminadas} inteligencias existentes para {len(ids_a_actualizar)} alumnos")

            for _, row in intel_melted_df.iterrows():
                alumno_id = nombre_a_id.get(row['nom'])
                if alumno_id:
                    try:
                        db.add(models.Inteligencia(
                            Alumno_ID=alumno_id,
                            Tipo_Inteligencia=row['Tipo_Inteligencia'],
                            Puntaje=row['Puntaje']
                        ))
                        inteligencias_procesadas += 1
                    except Exception as e:
                        logger.error(f"Error al crear inteligencia para alumno {row['nom']}: {e}")
                else:
                    logger.warning(f"No se encontró el alumno '{row['nom']}' para asignarle inteligencia.")
            
            logger.info(f"Procesamiento de inteligencias completado: {inteligencias_procesadas} inteligencias creadas")
        else:
            logger.info("No hay datos de inteligencias válidos para procesar")
        
            db.commit()
        logger.info("Commit final exitoso.")

        return {
            "mensaje": "Archivo Excel procesado exitosamente",
            "alumnos_procesados": alumnos_procesados,
            "alumnos_creados": alumnos_creados,
            "alumnos_actualizados": alumnos_actualizados,
            "competencias_procesadas": len(competencia_cols),
            "cursos_procesados": len(cursos_db),
            "inteligencias": {
                "procesadas": inteligencias_procesadas,
                "hoja_encontrada": inteligencias_info["hoja_encontrada"],
                "hoja_detectada": inteligencias_info["hoja_detectada"],
                "hojas_disponibles": inteligencias_info["hojas_disponibles"],
                "columnas_requeridas": inteligencias_info["columnas_requeridas"],
                "tipos_encontrados": inteligencias_info["tipos_encontrados"],
                "registros_validos": inteligencias_info["registros_validos"],
                "alumnos_con_inteligencias": inteligencias_info["alumnos_con_inteligencias"],
                "error_mensaje": inteligencias_info["error_mensaje"]
            },
            "ci": {
                "hoja_encontrada": ci_info["hoja_encontrada"],
                "hoja_detectada": ci_info["hoja_detectada"],
                "columnas_requeridas": ci_info["columnas_requeridas"],
                "registros_validos": ci_info["registros_validos"],
                "alumnos_con_ci": ci_info["alumnos_con_ci"],
                "error_mensaje": ci_info["error_mensaje"]
            }
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error fatal durante el procesamiento del Excel: {e}", exc_info=True)
        raise e