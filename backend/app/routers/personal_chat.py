import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import crud, database
from app.schemas import conversacion as conversacion_schema
from app.services import personal_ai_chat
from app.routers.profesores import get_current_profesor

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/personal-chat",
    tags=["personal-chat"],
)

@router.post("/send-message")
async def send_personal_message(
    chat_request: conversacion_schema.ChatRequest,
    current_profesor = Depends(get_current_profesor),
    db: Session = Depends(database.get_db)
):
    """
    Envía un mensaje personal a la IA para un alumno específico
    """
    try:
        # Obtener el contexto actualizado del alumno
        student_context = crud.get_alumno_conversacion_context(db, chat_request.alumno_id)
        if not student_context:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Obtener historial de conversación
        conversation_history = crud.get_conversacion_history(db, chat_request.alumno_id, current_profesor.Profesor_ID)
        
        # Convertir historial a formato esperado por la IA
        history_for_ai = []
        for conv in conversation_history:
            history_for_ai.append({
                "mensaje": conv.Mensaje,
                "es_usuario": bool(conv.Es_Usuario),
                "fecha": conv.Fecha_Creacion
            })
        
        # Guardar mensaje del usuario
        user_message = conversacion_schema.ConversacionCreate(
            alumno_id=chat_request.alumno_id,
            mensaje=chat_request.mensaje,
            es_usuario=True
        )
        
        contexto_json = json.dumps(student_context, ensure_ascii=False)
        crud.create_conversacion_message(
            db, user_message, current_profesor.Profesor_ID, contexto_json
        )
        
        # Obtener respuesta de la IA
        ai_response = personal_ai_chat.chat_with_student_context(
            student_context, history_for_ai, chat_request.mensaje
        )
        
        if not ai_response["success"]:
            raise HTTPException(status_code=500, detail=ai_response["error"])
        
        # Guardar respuesta de la IA
        ai_message = conversacion_schema.ConversacionCreate(
            alumno_id=chat_request.alumno_id,
            mensaje=ai_response["response"],
            es_usuario=False
        )
        
        ai_conversacion = crud.create_conversacion_message(
            db, ai_message, current_profesor.Profesor_ID, contexto_json
        )
        
        # Devolver formato que espera el frontend
        return {
            "success": True,
            "response": ai_response["response"],
            "student_name": student_context["nombre"],
            "conversacion_id": ai_conversacion.Conversacion_ID
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/history/{alumno_id}", response_model=conversacion_schema.ChatHistory)
async def get_personal_chat_history(
    alumno_id: int,
    current_profesor = Depends(get_current_profesor),
    db: Session = Depends(database.get_db)
):
    """
    Obtiene el historial completo de conversación personal de un alumno
    """
    try:
        # Verificar que el alumno existe
        alumno = crud.get_alumno(db, alumno_id)
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Obtener historial de conversación
        conversation_history = crud.get_conversacion_history(db, alumno_id, current_profesor.Profesor_ID)
        
        # Convertir a formato de respuesta
        messages = []
        for conv in conversation_history:
            messages.append(conversacion_schema.ChatMessage(
                mensaje=conv.Mensaje,
                es_usuario=bool(conv.Es_Usuario),
                fecha=conv.Fecha_Creacion
            ))
        
        return conversacion_schema.ChatHistory(
            alumno_id=alumno_id,
            alumno_nombre=alumno.Nombre,
            mensajes=messages,
            total_mensajes=len(messages)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.delete("/clear/{alumno_id}")
async def clear_personal_chat_history(
    alumno_id: int,
    current_profesor = Depends(get_current_profesor),
    db: Session = Depends(database.get_db)
):
    """
    Limpia todo el historial de conversación personal de un alumno
    """
    try:
        # Verificar que el alumno existe
        alumno = crud.get_alumno(db, alumno_id)
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Limpiar conversación
        crud.clear_conversacion_alumno(db, alumno_id, current_profesor.Profesor_ID)
        
        return {"success": True, "message": f"Conversación de {alumno.Nombre} limpiada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/welcome/{alumno_id}")
async def get_personal_welcome_message(
    alumno_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Obtiene un mensaje de bienvenida personalizado para un alumno (sin autenticación)
    """
    try:
        logger.info(f"Iniciando welcome message para alumno_id: {alumno_id}")
        
        # Obtener contexto del alumno
        logger.info(f"Obteniendo contexto para alumno_id: {alumno_id}")
        student_context = crud.get_alumno_conversacion_context(db, alumno_id)
        
        if not student_context:
            logger.error(f"Alumno no encontrado: {alumno_id}")
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        logger.info(f"Contexto obtenido exitosamente para {student_context.get('nombre', 'Alumno')}")
        logger.debug(f"Contexto: {json.dumps(student_context, ensure_ascii=False, default=str)}")
        
        # Generar mensaje de bienvenida
        logger.info("Generando mensaje de bienvenida...")
        welcome_message = personal_ai_chat.generate_welcome_message(student_context)
        
        if not welcome_message:
            logger.error("No se pudo generar el mensaje de bienvenida")
            raise HTTPException(status_code=500, detail="Error al generar mensaje de bienvenida")
        
        logger.info("Mensaje de bienvenida generado exitosamente")
        
        response_data = {
            "success": True,
            "welcome_message": welcome_message,
            "student_name": student_context["nombre"],
            "context_summary": {
                "alumno_id": student_context["alumno_id"],
                "ci": student_context["ci"],
                "inteligencias_count": len(student_context["inteligencias"]),
                "calificaciones_count": len(student_context["calificaciones"])
            }
        }
        
        logger.info(f"Respuesta exitosa para alumno: {student_context['nombre']}")
        return response_data
        
    except HTTPException:
        logger.error(f"HTTPException en welcome message para alumno_id: {alumno_id}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado en welcome message para alumno_id {alumno_id}: {str(e)}")
        logger.exception("Traceback completo:")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/send-message-public")
async def send_public_message(
    chat_request: conversacion_schema.ChatRequest,
    db: Session = Depends(database.get_db)
):
    """
    Envía un mensaje público a la IA para un alumno específico (sin autenticación)
    """
    try:
        # Usar un profesor por defecto (ID 1) para las conversaciones públicas
        default_profesor_id = 1
        
        # Obtener el contexto actualizado del alumno
        student_context = crud.get_alumno_conversacion_context(db, chat_request.alumno_id)
        if not student_context:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Obtener historial de conversación
        conversation_history = crud.get_conversacion_history(db, chat_request.alumno_id, default_profesor_id)
        
        # Convertir historial a formato esperado por la IA
        history_for_ai = []
        for conv in conversation_history:
            history_for_ai.append({
                "mensaje": conv.Mensaje,
                "es_usuario": bool(conv.Es_Usuario),
                "fecha": conv.Fecha_Creacion
            })
        
        # Guardar mensaje del usuario
        user_message = conversacion_schema.ConversacionCreate(
            alumno_id=chat_request.alumno_id,
            mensaje=chat_request.mensaje,
            es_usuario=True
        )
        
        contexto_json = json.dumps(student_context, ensure_ascii=False)
        user_conversacion = crud.create_conversacion_message(
            db, user_message, default_profesor_id, contexto_json
        )
        
        # Obtener respuesta de la IA
        ai_response = personal_ai_chat.chat_with_student_context(
            student_context, history_for_ai, chat_request.mensaje
        )
        
        if not ai_response["success"]:
            raise HTTPException(status_code=500, detail=ai_response["error"])
        
        # Guardar respuesta de la IA
        ai_message = conversacion_schema.ConversacionCreate(
            alumno_id=chat_request.alumno_id,
            mensaje=ai_response["response"],
            es_usuario=False
        )
        
        ai_conversacion = crud.create_conversacion_message(
            db, ai_message, default_profesor_id, contexto_json
        )
        
        # Devolver formato que espera el frontend
        return {
            "success": True,
            "response": ai_response["response"],
            "student_name": student_context["nombre"],
            "conversacion_id": ai_conversacion.Conversacion_ID
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/recommendations/{alumno_id}")
async def get_recommendations_only(alumno_id: int, db: Session = Depends(database.get_db)):
    """
    Obtiene solo las recomendaciones de Miko para un alumno (sin historial, sin autenticación)
    """
    try:
        logger.info(f"Obteniendo recomendaciones para alumno_id: {alumno_id}")
        
        # Obtener contexto del alumno
        student_context = crud.get_alumno_conversacion_context(db, alumno_id)
        
        if not student_context:
            logger.error(f"Alumno no encontrado: {alumno_id}")
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        logger.info(f"Contexto obtenido exitosamente para {student_context.get('nombre', 'Alumno')}")
        
        # Generar recomendaciones usando el servicio de IA principal
        from app.services.ai_assistant import ai_assistant
        ai_response = ai_assistant.generate_pedagogical_recommendations(student_context)
        
        if not ai_response["success"]:
            logger.error(f"Error generando recomendaciones: {ai_response.get('error', 'Error desconocido')}")
            raise HTTPException(status_code=500, detail="Error al generar recomendaciones")
        
        logger.info("Recomendaciones generadas exitosamente")
        
        response_data = {
            "success": True,
            "recommendations": ai_response["recommendations"],
            "student_name": student_context["nombre"],
            "analysis_summary": ai_response.get("analysis_summary", {}),
            "context_summary": {
                "alumno_id": student_context["alumno_id"],
                "ci": student_context["ci"],
                "inteligencias_count": len(student_context["inteligencias"]),
                "calificaciones_count": len(student_context["calificaciones"])
            }
        }
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}") 