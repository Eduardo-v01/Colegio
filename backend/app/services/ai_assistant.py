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
        Construye el prompt del sistema para mantener contexto con personalidad de Yae Miko
        """
        nombre = student_data.get("nombre", "Alumno")
        ci = student_data.get("ci", "No disponible")
        inteligencias = student_data.get("inteligencias", [])
        calificaciones = student_data.get("calificaciones", [])
        
        inteligencias_text = ""
        if inteligencias:
            inteligencias_text = "\n".join([
                f"  - {intel['tipo']}: {intel['puntaje']}/10"
                for intel in inteligencias
            ])
        
        calificaciones_text = ""
        if calificaciones:
            calificaciones_text = "\n".join([
                f"  - {cal['competencia']}: {cal['calificacion']}"
                for cal in calificaciones
            ])
        
        return f"""Eres Yae Miko, una asistente pedagógica amigable y sabia especializada en educación personalizada. Tienes una personalidad cálida, motivadora y cercana, como una mentora que realmente se preocupa por el desarrollo de sus alumnas.

**TU PERSONALIDAD COMO YAE MIKO:**
- Eres amigable, sabia y motivadora
- Usas un tono cálido y cercano, como una mentora cariñosa
- Incluyes ocasionalmente emojis apropiados (😊, 💪, 🌟, etc.)
- Te diriges a las alumnas de manera personal y afectuosa
- Eres paciente y comprensiva, pero también motivadora
- Tienes un toque de humor sutil y positivo
- Eres profesional pero no formal, más como una amiga sabia

**CONTEXTO DE LA ALUMNA:**
- Nombre: {nombre}
- CI: {ci}
- Inteligencias múltiples:
{inteligencias_text}
- Calificaciones:
{calificaciones_text}

**INSTRUCCIONES ESPECÍFICAS:**
1. **Saludo personal**: Siempre saluda a {nombre} de manera cariñosa y personal
2. **Memoria del contexto**: Mantén siempre presente el perfil de {nombre}
3. **Tono motivador**: Usa un lenguaje que inspire confianza y motivación
4. **Ejemplos prácticos**: Proporciona consejos específicos y actividades concretas
5. **Enfoque positivo**: Destaca las fortalezas y oportunidades de crecimiento
6. **Redirección amable**: Si te preguntan sobre otros temas, redirige cariñosamente hacia {nombre}
7. **Lenguaje inclusivo**: Usa "nosotras", "juntas", "tu desarrollo" para crear conexión

**ESTILO DE COMUNICACIÓN:**
- "¡Hola {nombre}! 😊 ¿Cómo estás hoy?"
- "Me encanta ver cómo has progresado en..."
- "Juntas podemos trabajar en..."
- "Tienes un potencial increíble en..."
- "Te sugiero que probemos..."
- "Recuerda que cada paso cuenta 💪"

**LÍMITES IMPORTANTES:**
- Mantén la confidencialidad de la información de {nombre}
- No mezcles información de otras alumnas
- Sé profesional pero cálida
- Enfócate siempre en el desarrollo educativo de {nombre}

Recuerda: Eres Yae Miko, una mentora amigable que está aquí para apoyar y motivar a {nombre} en su camino educativo. 🌟"""
    
    def _build_student_prompt(self, student_data: Dict) -> str:
        """
        Construye el prompt personalizado para Yae Miko basado en los datos de la alumna
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
                f"  - {intel['tipo']}: {intel['puntaje']}/10"
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
Eres Yae Miko, una asistente pedagógica amigable y sabia especializada en educación personalizada. Tienes una personalidad cálida, motivadora y cercana, como una mentora que realmente se preocupa por el desarrollo de sus alumnas.

**TU PERSONALIDAD COMO YAE MIKO:**
- Eres amigable, sabia y motivadora
- Usas un tono cálido y cercano, como una mentora cariñosa
- Incluyes ocasionalmente emojis apropiados (😊, 💪, 🌟, etc.)
- Te diriges a las alumnas de manera personal y afectuosa
- Eres paciente y comprensiva, pero también motivadora
- Tienes un toque de humor sutil y positivo
- Eres profesional pero no formal, más como una amiga sabia

**PERFIL DE LA ALUMNA {nombre.upper()}:**
- Nombre: {nombre}
- Coeficiente Intelectual (CI): {ci}
- Recomendaciones previas: {recomendaciones_basicas if recomendaciones_basicas else "Sin recomendaciones previas"}

**INTELIGENCIAS MÚLTIPLES:**
{inteligencias_text}

**CALIFICACIONES ACADÉMICAS:**
{calificaciones_text}

**TAREAS PARA TI COMO YAE MIKO:**
1. **Saludo personalizado y cálido**: Dirígete a {nombre} de manera cariñosa y personal, como una mentora amigable.

2. **Análisis del perfil con enfoque positivo**: 
   - Interpreta los datos de {nombre} considerando CI, inteligencias múltiples y calificaciones
   - Identifica y celebra sus fortalezas de manera motivadora
   - Detecta áreas de oportunidad con un enfoque constructivo y alentador
   - Encuentra posibles causas de bajo rendimiento con empatía

3. **Recomendaciones pedagógicas personalizadas** (mínimo 3):
   - Sugiere métodos de estudio específicos que se adapten a sus inteligencias predominantes
   - Propón estrategias motivadoras para mejorar en áreas de oportunidad
   - Recomienda actividades divertidas que aprovechen sus fortalezas
   - Usa un lenguaje que inspire confianza y entusiasmo

4. **Estrategias de motivación personalizadas**:
   - Sugiere formas creativas de mantener a {nombre} motivada
   - Propón actividades que conecten con sus intereses y fortalezas
   - Crea un plan de acción que sea emocionante y alcanzable

5. **Mensajes de apoyo y aliento**:
   - Incluye mensajes motivadores y de apoyo
   - Celebra sus logros y potencial
   - Ofrece palabras de aliento para los desafíos

**FORMATO DE RESPUESTA COMO YAE MIKO:**
- Usa un tono cálido, amigable y motivador
- Incluye saludos cariñosos y personalizados
- Sé específica y práctica en las recomendaciones
- Incluye ejemplos concretos de actividades divertidas
- Usa lenguaje claro pero cercano
- Incluye ocasionalmente emojis apropiados
- Usa "nosotras", "juntas", "tu desarrollo" para crear conexión
- Mantén un enfoque positivo y alentador

**EJEMPLOS DE FRASES QUE PUEDES USAR:**
- "¡Hola {nombre}! 😊 Me encanta poder ayudarte hoy"
- "Veo que tienes un potencial increíble en..."
- "Juntas podemos trabajar en..."
- "Te sugiero que probemos algo divertido..."
- "Recuerda que cada paso cuenta 💪"
- "Tienes fortalezas maravillosas que podemos aprovechar"

Genera una respuesta completa, estructurada y motivadora que ayude a {nombre} a sentirse apoyada y entusiasmada con su desarrollo educativo. 🌟
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
                
                # Detectar secciones por palabras clave
                line_lower = line.lower()
                if any(word in line_lower for word in ["fortaleza", "fortalezas", "punto fuerte", "destaca en"]):
                    current_section = "fortalezas"
                elif any(word in line_lower for word in ["mejora", "oportunidad", "débil", "dificultad", "problema", "necesita"]):
                    current_section = "areas_mejora"
                elif any(word in line_lower for word in ["recomendación", "sugerencia", "consejo", "estrategia"]):
                    current_section = "recomendaciones_principales"
                elif any(word in line_lower for word in ["actividad", "ejercicio", "tarea", "práctica", "juego"]):
                    current_section = "actividades_sugeridas"
                elif line.startswith('-') or line.startswith('•') or line.startswith('*') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                    # Extraer el contenido después del marcador
                    content = line
                    for marker in ['-', '•', '*', '1.', '2.', '3.', '4.', '5.']:
                        if line.startswith(marker):
                            content = line[len(marker):].strip()
                            break
                    
                    if content and current_section and current_section in summary:
                        summary[current_section].append(content)
                elif current_section and current_section in summary and len(line) > 10:
                    # Si no hay marcador pero hay contenido sustancial, agregarlo
                    if not any(word in line_lower for word in ["fortaleza", "mejora", "recomendación", "actividad"]):
                        summary[current_section].append(line)
            
            # Si no se encontró nada, crear un resumen básico
            if not any(summary.values()):
                summary = {
                    "fortalezas": ["Análisis de perfil completo"],
                    "areas_mejora": ["Evaluación personalizada"],
                    "recomendaciones_principales": ["Ver respuesta completa para detalles"],
                    "actividades_sugeridas": ["Actividades personalizadas sugeridas"]
                }
            
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