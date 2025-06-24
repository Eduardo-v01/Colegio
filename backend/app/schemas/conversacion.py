from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ConversacionCreate(BaseModel):
    alumno_id: int
    mensaje: str
    es_usuario: bool = True  # True = Profesor, False = IA

class ConversacionResponse(BaseModel):
    conversacion_id: int
    alumno_id: int
    profesor_id: int
    mensaje: str
    es_usuario: bool
    fecha_creacion: str
    contexto_alumno: Optional[str] = None

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    mensaje: str
    es_usuario: bool
    fecha: str

class ChatHistory(BaseModel):
    alumno_id: int
    alumno_nombre: str
    mensajes: List[ChatMessage]
    total_mensajes: int

class ChatRequest(BaseModel):
    mensaje: str
    alumno_id: int 