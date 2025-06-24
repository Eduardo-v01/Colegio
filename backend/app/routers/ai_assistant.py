from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.database.database import get_db
from app.database import models
from app.services.ai_assistant import ai_assistant

router = APIRouter(prefix="/ai-assistant", tags=["Asistente Pedagógica IA"])

@router.get("/students")
def get_students_for_ai(db: Session = Depends(get_db)):
    """Obtener lista de alumnos con información básica para la IA"""
    try:
        alumnos = db.query(models.Alumno).all()
        
        students_list = []
        for alumno in alumnos:
            # Obtener CI
            ci_info = None
            if alumno.CI:
                ci_info = {
                    "valor": alumno.CI,
                    "categoria": _get_ci_category(alumno.CI)
                }
            
            # Obtener inteligencias
            inteligencias = db.query(models.Inteligencia).filter(
                models.Inteligencia.Alumno_ID == alumno.Alumno_ID
            ).all()
            
            inteligencias_list = [
                {
                    "tipo": intel.Tipo_Inteligencia,
                    "puntaje": intel.Puntaje
                } for intel in inteligencias
            ]
            
            # Obtener calificaciones
            calificaciones = db.query(models.AlumnoCompetencia).filter(
                models.AlumnoCompetencia.Alumno_ID == alumno.Alumno_ID
            ).all()
            
            calificaciones_list = []
            for cal in calificaciones:
                competencia = db.query(models.CompetenciaPlantilla).filter(
                    models.CompetenciaPlantilla.CompetenciaPlantilla_ID == cal.CompetenciaPlantilla_ID
                ).first()
                
                if competencia:
                    calificaciones_list.append({
                        "competencia": competencia.Codigo_Competencia,
                        "calificacion": cal.Calificacion,
                        "descripcion": competencia.Descripcion
                    })
            
            students_list.append({
                "alumno_id": alumno.Alumno_ID,
                "nombre": alumno.Nombre,
                "ci": ci_info,
                "inteligencias": inteligencias_list,
                "calificaciones": calificaciones_list,
                "promedio": alumno.Promedio_Calificaciones,
                "recomendaciones_basicas": alumno.Recomendaciones_Basicas,
                "cantidad_competencias": len(calificaciones_list)
            })
        
        return {
            "success": True,
            "students": students_list,
            "total": len(students_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de alumnos: {str(e)}")

@router.get("/student/{alumno_id}")
def get_student_profile(alumno_id: int, db: Session = Depends(get_db)):
    """Obtener perfil completo de un alumno específico"""
    try:
        # Obtener alumno
        alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Obtener CI
        ci_info = None
        if alumno.CI:
            ci_info = {
                "valor": alumno.CI,
                "categoria": _get_ci_category(alumno.CI)
            }
        
        # Obtener inteligencias
        inteligencias = db.query(models.Inteligencia).filter(
            models.Inteligencia.Alumno_ID == alumno.Alumno_ID
        ).order_by(models.Inteligencia.Puntaje.desc()).all()
        
        inteligencias_list = [
            {
                "tipo": intel.Tipo_Inteligencia,
                "puntaje": intel.Puntaje
            } for intel in inteligencias
        ]
        
        # Obtener calificaciones agrupadas por curso
        calificaciones = db.query(models.AlumnoCompetencia).filter(
            models.AlumnoCompetencia.Alumno_ID == alumno.Alumno_ID
        ).all()
        
        calificaciones_por_curso = {}
        for cal in calificaciones:
            competencia = db.query(models.CompetenciaPlantilla).filter(
                models.CompetenciaPlantilla.CompetenciaPlantilla_ID == cal.CompetenciaPlantilla_ID
            ).first()
            
            if competencia:
                curso = db.query(models.Curso).filter(
                    models.Curso.Curso_ID == competencia.Curso_ID
                ).first()
                
                if curso:
                    if curso.Nombre not in calificaciones_por_curso:
                        calificaciones_por_curso[curso.Nombre] = []
                    
                    calificaciones_por_curso[curso.Nombre].append({
                        "competencia": competencia.Codigo_Competencia,
                        "calificacion": cal.Calificacion,
                        "descripcion": competencia.Descripcion
                    })
        
        # Calcular estadísticas
        total_calificaciones = len(calificaciones)
        calificaciones_a = len([c for c in calificaciones if c.Calificacion == 'A'])
        calificaciones_b = len([c for c in calificaciones if c.Calificacion == 'B'])
        calificaciones_c = len([c for c in calificaciones if c.Calificacion == 'C'])
        calificaciones_d = len([c for c in calificaciones if c.Calificacion == 'D'])
        
        # Inteligencias predominantes
        inteligencias_predominantes = []
        if inteligencias_list:
            max_puntaje = max(intel['puntaje'] for intel in inteligencias_list)
            inteligencias_predominantes = [
                intel for intel in inteligencias_list 
                if intel['puntaje'] >= max_puntaje * 0.8  # 80% del máximo
            ]
        
        return {
            "success": True,
            "alumno": {
                "alumno_id": alumno.Alumno_ID,
                "nombre": alumno.Nombre,
                "ci": ci_info,
                "inteligencias": inteligencias_list,
                "inteligencias_predominantes": inteligencias_predominantes,
                "calificaciones_por_curso": calificaciones_por_curso,
                "promedio": alumno.Promedio_Calificaciones,
                "recomendaciones_basicas": alumno.Recomendaciones_Basicas,
                "estadisticas": {
                    "total_calificaciones": total_calificaciones,
                    "calificaciones_a": calificaciones_a,
                    "calificaciones_b": calificaciones_b,
                    "calificaciones_c": calificaciones_c,
                    "calificaciones_d": calificaciones_d,
                    "porcentaje_excelente": (calificaciones_a / total_calificaciones * 100) if total_calificaciones > 0 else 0,
                    "porcentaje_bueno": (calificaciones_b / total_calificaciones * 100) if total_calificaciones > 0 else 0,
                    "porcentaje_regular": (calificaciones_c / total_calificaciones * 100) if total_calificaciones > 0 else 0,
                    "porcentaje_deficiente": (calificaciones_d / total_calificaciones * 100) if total_calificaciones > 0 else 0
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener perfil del alumno: {str(e)}")

@router.post("/generate-recommendations/{alumno_id}")
def generate_ai_recommendations(alumno_id: int, db: Session = Depends(get_db)):
    """Generar recomendaciones pedagógicas personalizadas usando IA"""
    try:
        # Obtener perfil del alumno
        alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Obtener inteligencias
        inteligencias = db.query(models.Inteligencia).filter(
            models.Inteligencia.Alumno_ID == alumno.Alumno_ID
        ).all()
        
        inteligencias_list = [
            {
                "tipo": intel.Tipo_Inteligencia,
                "puntaje": intel.Puntaje
            } for intel in inteligencias
        ]
        
        # Obtener calificaciones
        calificaciones = db.query(models.AlumnoCompetencia).filter(
            models.AlumnoCompetencia.Alumno_ID == alumno.Alumno_ID
        ).all()
        
        calificaciones_list = []
        for cal in calificaciones:
            competencia = db.query(models.CompetenciaPlantilla).filter(
                models.CompetenciaPlantilla.CompetenciaPlantilla_ID == cal.CompetenciaPlantilla_ID
            ).first()
            
            if competencia:
                calificaciones_list.append({
                    "competencia": competencia.Codigo_Competencia,
                    "calificacion": cal.Calificacion,
                    "descripcion": competencia.Descripcion
                })
        
        # Preparar datos para la IA
        student_data = {
            "alumno_id": alumno.Alumno_ID,
            "nombre": alumno.Nombre,
            "ci": alumno.CI,
            "inteligencias": inteligencias_list,
            "calificaciones": calificaciones_list,
            "recomendaciones_basicas": alumno.Recomendaciones_Basicas
        }
        
        # Generar recomendaciones con IA
        ai_result = ai_assistant.generate_pedagogical_recommendations(student_data)
        
        return {
            "success": ai_result["success"],
            "student_name": alumno.Nombre,
            "recommendations": ai_result["recommendations"],
            "analysis_summary": ai_result.get("analysis_summary", {}),
            "error": ai_result.get("error")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")

@router.post("/chat/{alumno_id}")
def chat_with_ai(alumno_id: int, message: Dict, db: Session = Depends(get_db)):
    """Chat interactivo con la IA sobre un alumno específico"""
    try:
        user_message = message.get("message", "").strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
        
        # Verificar que el alumno existe
        alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Enviar mensaje a la IA
        chat_result = ai_assistant.chat_with_ai(alumno_id, user_message)
        
        return {
            "success": chat_result["success"],
            "response": chat_result.get("response", ""),
            "student_name": chat_result.get("student_name", alumno.Nombre),
            "conversation_length": chat_result.get("conversation_length", 0),
            "error": chat_result.get("error")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")

@router.get("/conversation-history/{alumno_id}")
def get_conversation_history(alumno_id: int, db: Session = Depends(get_db)):
    """Obtener historial de conversación para un alumno"""
    try:
        # Verificar que el alumno existe
        alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Obtener historial de conversación
        history_result = ai_assistant.get_conversation_history(alumno_id)
        
        return {
            "success": history_result["success"],
            "messages": history_result.get("messages", []),
            "student_name": history_result.get("student_name", alumno.Nombre),
            "last_updated": history_result.get("last_updated"),
            "error": history_result.get("error")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")

@router.delete("/conversation/{alumno_id}")
def clear_conversation(alumno_id: int, db: Session = Depends(get_db)):
    """Limpiar historial de conversación para un alumno"""
    try:
        # Verificar que el alumno existe
        alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == alumno_id).first()
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Limpiar conversación
        if alumno_id in ai_assistant.conversations:
            del ai_assistant.conversations[alumno_id]
        
        return {
            "success": True,
            "message": f"Conversación de {alumno.Nombre} limpiada exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al limpiar conversación: {str(e)}")

def _get_ci_category(ci_value: int) -> str:
    """Determinar categoría de CI"""
    if ci_value >= 130:
        return "Muy Superior"
    elif ci_value >= 120:
        return "Superior"
    elif ci_value >= 110:
        return "Promedio Alto"
    elif ci_value >= 90:
        return "Promedio"
    elif ci_value >= 80:
        return "Promedio Bajo"
    elif ci_value >= 70:
        return "Bajo"
    else:
        return "Muy Bajo" 