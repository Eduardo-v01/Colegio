import logging
from typing import Dict, List, Optional
from openai import OpenAI
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class AIAssistantService:
    def __init__(self):
        # Configuración de la IA - usando DeepSeek a través de OpenRouter
        self.client = OpenAI(
            api_key="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",
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = "deepseek/deepseek-r1:free"
        # Almacenar conversaciones por alumno
        self.conversations = {}
    
    def generate_pedagogical_recommendations(self, student_data: Dict) -> Dict:
        """
        Genera recomendaciones pedagógicas personalizadas basadas en el perfil del alumno
        """
        try:
            # Construir el prompt con la información del alumno
            prompt = self._build_student_prompt(student_data)
            
            # Llamar a la IA
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,
                temperature=0.7,
            )
            
            ai_response = response.choices[0].message.content
            
            # Inicializar conversación para este alumno
            student_id = student_data.get("alumno_id")
            if student_id:
                self.conversations[student_id] = {
                    "student_data": student_data,
                    "messages": [
                        {"role": "system", "content": self._build_system_prompt(student_data)},
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": ai_response}
                    ],
                    "last_updated": datetime.now()
                }
            
            return {
                "success": True,
                "recommendations": ai_response,
                "student_name": student_data.get("nombre", "Alumno"),
                "analysis_summary": self._extract_summary(ai_response)
            }
            
        except Exception as e:
            logger.error(f"Error al generar recomendaciones de IA: {e}")
            return {
                "success": False,
                "error": f"Error al procesar la solicitud: {str(e)}",
                "recommendations": "No se pudieron generar recomendaciones en este momento."
            }
    
    def chat_with_ai(self, student_id: int, user_message: str) -> Dict:
        """
        Mantiene una conversación con la IA sobre un alumno específico
        """
        try:
            if student_id not in self.conversations:
                return {
                    "success": False,
                    "error": "No hay contexto de alumno. Primero genera recomendaciones para este alumno."
                }
            
            conversation = self.conversations[student_id]
            
            # Agregar mensaje del usuario
            conversation["messages"].append({"role": "user", "content": user_message})
            conversation["last_updated"] = datetime.now()
            
            # Llamar a la IA con el historial completo
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation["messages"],
                max_tokens=4096,
                temperature=0.7,
            )
            
            ai_response = response.choices[0].message.content
            
            # Agregar respuesta de la IA al historial
            conversation["messages"].append({"role": "assistant", "content": ai_response})
            
            return {
                "success": True,
                "response": ai_response,
                "student_name": conversation["student_data"].get("nombre", "Alumno"),
                "conversation_length": len(conversation["messages"])
            }
            
        except Exception as e:
            logger.error(f"Error en chat con IA: {e}")
            return {
                "success": False,
                "error": f"Error al procesar el mensaje: {str(e)}"
            }
    
    def get_conversation_history(self, student_id: int) -> Dict:
        """
        Obtiene el historial de conversación para un alumno
        """
        if student_id not in self.conversations:
            return {
                "success": False,
                "error": "No hay conversación para este alumno"
            }
        
        conversation = self.conversations[student_id]
        return {
            "success": True,
            "messages": conversation["messages"][3:],  # Excluir mensajes del sistema y recomendaciones iniciales
            "student_name": conversation["student_data"].get("nombre", "Alumno"),
            "last_updated": conversation["last_updated"].isoformat()
        }
    
    def _build_system_prompt(self, student_data: Dict) -> str:
        """
        Construye el prompt del sistema para mantener contexto
        """
        nombre = student_data.get("nombre", "Alumno")
        ci = student_data.get("ci", "No disponible")
        inteligencias = student_data.get("inteligencias", [])
        calificaciones = student_data.get("calificaciones", [])
        
        inteligencias_text = ""
        if inteligencias:
            inteligencias_text = "\n".join([
                f"  - {intel['tipo']}: {intel['puntaje']}/100"
                for intel in inteligencias
            ])
        
        calificaciones_text = ""
        if calificaciones:
            calificaciones_text = "\n".join([
                f"  - {cal['competencia']}: {cal['calificacion']}"
                for cal in calificaciones
            ])
        
        return f"""Eres una asistente pedagógica especializada en educación personalizada. Estás conversando sobre el alumno {nombre}.

CONTEXTO DEL ALUMNO:
- Nombre: {nombre}
- CI: {ci}
- Inteligencias múltiples:
{inteligencias_text}
- Calificaciones:
{calificaciones_text}

INSTRUCCIONES:
1. Mantén siempre el contexto del alumno en mente
2. Responde de manera amigable y profesional
3. Proporciona consejos prácticos y específicos
4. Si te preguntan sobre otros temas, redirige amablemente la conversación hacia el alumno
5. Usa ejemplos concretos relacionados con el perfil del alumno
6. Mantén un tono motivador y constructivo

Recuerda que estás aquí para ayudar al docente a entender mejor y trabajar más efectivamente con {nombre}."""
    
    def _build_student_prompt(self, student_data: Dict) -> str:
        """
        Construye el prompt personalizado para la IA basado en los datos del alumno
        """
        nombre = student_data.get("nombre", "Alumno")
        ci = student_data.get("ci", "No disponible")
        inteligencias = student_data.get("inteligencias", [])
        calificaciones = student_data.get("calificaciones", [])
        recomendaciones_basicas = student_data.get("recomendaciones_basicas", "")
        
        # Formatear inteligencias
        inteligencias_text = ""
        if inteligencias:
            inteligencias_text = "\n".join([
                f"  - {intel['tipo']}: {intel['puntaje']}/100"
                for intel in inteligencias
            ])
        else:
            inteligencias_text = "  - No hay datos de inteligencias múltiples"
        
        # Formatear calificaciones
        calificaciones_text = ""
        if calificaciones:
            calificaciones_text = "\n".join([
                f"  - {cal['competencia']}: {cal['calificacion']}"
                for cal in calificaciones
            ])
        else:
            calificaciones_text = "  - No hay calificaciones registradas"
        
        prompt = f"""
Eres una IA educativa especializada en análisis pedagógico y recomendaciones personalizadas. Tu objetivo es ayudar a los docentes a entender mejor a sus alumnos y sugerir estrategias de enseñanza efectivas.

**PERFIL DEL ALUMNO:**
- Nombre: {nombre}
- Coeficiente Intelectual (CI): {ci}
- Recomendaciones previas: {recomendaciones_basicas if recomendaciones_basicas else "Sin recomendaciones previas"}

**INTELIGENCIAS MÚLTIPLES:**
{inteligencias_text}

**CALIFICACIONES ACADÉMICAS:**
{calificaciones_text}

**TAREAS PARA TI:**
1. **Saludo personalizado**: Dirígete al alumno por su nombre y pregúntale qué le gustaría trabajar hoy.

2. **Análisis del perfil**: 
   - Interpreta los datos del alumno considerando CI, inteligencias múltiples y calificaciones
   - Identifica fortalezas y áreas de oportunidad
   - Detecta posibles causas de bajo rendimiento en ciertas áreas

3. **Recomendaciones pedagógicas** (mínimo 3):
   - Sugiere métodos de estudio específicos para sus inteligencias predominantes
   - Propón estrategias para mejorar en áreas débiles
   - Recomienda actividades que aprovechen sus fortalezas

4. **Estrategias de motivación**:
   - Sugiere formas de mantener al alumno motivado
   - Propón actividades que conecten con sus intereses

5. **Advertencias importantes**:
   - Advierte sobre posibles prejuicios al juzgar solo por CI o calificaciones
   - Enfatiza la importancia del enfoque holístico

**FORMATO DE RESPUESTA:**
- Usa un tono amigable y motivador
- Sé específico y práctico en las recomendaciones
- Incluye ejemplos concretos de actividades
- Mantén un lenguaje claro para docentes y padres

Genera una respuesta completa y estructurada que ayude al docente a trabajar mejor con este alumno.
"""
        
        return prompt
    
    def _extract_summary(self, ai_response: str) -> Dict:
        """
        Extrae un resumen estructurado de la respuesta de la IA
        """
        try:
            # Buscar secciones clave en la respuesta
            lines = ai_response.split('\n')
            summary = {
                "fortalezas": [],
                "areas_mejora": [],
                "recomendaciones_principales": [],
                "actividades_sugeridas": []
            }
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detectar secciones
                if "fortaleza" in line.lower() or "fortalezas" in line.lower():
                    current_section = "fortalezas"
                elif "mejora" in line.lower() or "oportunidad" in line.lower() or "débil" in line.lower():
                    current_section = "areas_mejora"
                elif "recomendación" in line.lower() or "sugerencia" in line.lower():
                    current_section = "recomendaciones_principales"
                elif "actividad" in line.lower() or "ejercicio" in line.lower():
                    current_section = "actividades_sugeridas"
                elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    if current_section and current_section in summary:
                        summary[current_section].append(line[1:].strip())
            
            return summary
            
        except Exception as e:
            logger.error(f"Error al extraer resumen: {e}")
            return {
                "fortalezas": ["Análisis en progreso"],
                "areas_mejora": ["Análisis en progreso"],
                "recomendaciones_principales": ["Ver respuesta completa"],
                "actividades_sugeridas": ["Ver respuesta completa"]
            }

# Instancia global del servicio
ai_assistant = AIAssistantService() 