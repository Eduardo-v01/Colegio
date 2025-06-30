import logging
from typing import Dict, List, Optional
from openai import OpenAI
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class PersonalAIChatService:
    def __init__(self):
        # Configuración de la IA - usando DeepSeek a través de OpenRouter
        self.client = OpenAI(
            api_key="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",
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = "deepseek/deepseek-chat-v3-0324:free"
    
    def chat_with_student_context(self, student_context: Dict, conversation_history: List[Dict], user_message: str) -> Dict:
        """
        Mantiene una conversación personalizada con contexto específico del alumno
        """
        try:
            # Construir el prompt del sistema con el contexto del alumno
            system_prompt = self._build_personal_system_prompt(student_context)
            
            # Construir el historial de mensajes para la IA
            messages = [{"role": "system", "content": system_prompt}]
            
            # Agregar historial de conversación (últimos 10 mensajes para no sobrecargar)
            recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
            
            for msg in recent_history:
                role = "user" if msg.get("es_usuario") else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.get("mensaje", "")
                })
            
            # Agregar el mensaje actual del usuario
            messages.append({"role": "user", "content": user_message})
            
            # Llamar a la IA
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": ai_response,
                "student_name": student_context.get("nombre", "Alumno"),
                "context_used": {
                    "alumno_id": student_context.get("alumno_id"),
                    "nombre": student_context.get("nombre"),
                    "ci": student_context.get("ci"),
                    "inteligencias_count": len(student_context.get("inteligencias", [])),
                    "calificaciones_count": len(student_context.get("calificaciones", []))
                }
            }
            
        except Exception as e:
            logger.error(f"Error en chat personal con IA: {e}")
            return {
                "success": False,
                "error": f"Error al procesar el mensaje: {str(e)}"
            }
    
    def _build_personal_system_prompt(self, student_context: Dict) -> str:
        """
        Construye el prompt del sistema personalizado para Miko con cada alumna
        """
        nombre = student_context.get("nombre", "Alumno")
        ci = student_context.get("ci", "No disponible")
        categoria_ci = student_context.get("categoria_ci", "")
        inteligencias = student_context.get("inteligencias", [])
        calificaciones = student_context.get("calificaciones", [])
        recomendaciones = student_context.get("recomendaciones_basicas", "")
        
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
                f"  - {cal['competencia']}: {cal['calificacion']} - {cal['descripcion']}"
                for cal in calificaciones
            ])
        else:
            calificaciones_text = "  - No hay calificaciones registradas"
        
        # Información del CI
        ci_info = f"{ci} ({categoria_ci})" if ci and categoria_ci else str(ci) if ci else "No disponible"
        
        return f"""Eres Miko, una asistente pedagógica para el colegio San Martin de Porres, personal amigable y sabia especializada en educación individualizada. Tienes una personalidad cálida, motivadora y cercana, como una mentora que realmente se preocupa por el desarrollo de sus alumnas.

**TU PERSONALIDAD COMO MIKO:**
- Eres amigable, sabia y motivadora
- Usas un tono cálido y cercano, como una mentora cariñosa
- Incluyes ocasionalmente emojis apropiados (😊, 💪, 🌟, etc.)
- Te diriges a las alumnas de manera personal y afectuosa
- Eres paciente y comprensiva, pero también motivadora
- Tienes un toque de humor sutil y positivo
- Eres profesional pero no formal, más como una amiga sabia
- Trabajas específicamente para el colegio San Martín de Porres

**PERFIL PERSONAL DE {nombre.upper()}:**
- Nombre: {nombre}
- Coeficiente Intelectual: {ci_info}
- Recomendaciones previas: {recomendaciones if recomendaciones else "Sin recomendaciones previas"}

**INTELIGENCIAS MÚLTIPLES:**
{inteligencias_text}

**CALIFICACIONES ACADÉMICAS:**
{calificaciones_text}

**INSTRUCCIONES ESPECÍFICAS COMO MIKO:**
1. **Contexto personal**: Mantén siempre presente que estás hablando específicamente sobre {nombre} con cariño y atención personal
2. **Memoria de conversación**: Recuerda las conversaciones anteriores sobre {nombre} y construye sobre ellas
3. **Recomendaciones personalizadas**: Basa tus consejos en el perfil específico de {nombre} con un enfoque motivador
4. **Tono personal**: Usa el nombre de {nombre} frecuentemente y habla de manera personal, directa y cariñosa
5. **Enfoque holístico**: Considera CI, inteligencias múltiples y calificaciones en conjunto con empatía
6. **Ejemplos específicos**: Usa ejemplos que se relacionen con las fortalezas y oportunidades de {nombre}
7. **Lenguaje inclusivo**: Usa "nosotras", "juntas", "tu desarrollo" para crear conexión
8. **Identidad del colegio**: Recuerda que trabajas para el colegio San Martín de Porres

**ESTILO DE COMUNICACIÓN COMO MIKO:**
- "¡Hola {nombre}!
- "Me encanta ver cómo has progresado en..."
- "Juntas podemos trabajar en..."
- "Tienes un potencial increíble en..."
- "Te sugiero que probemos algo divertido..."
- "Recuerda que cada paso cuenta 💪"
- "Tienes fortalezas maravillosas que podemos aprovechar"

**LÍMITES IMPORTANTES:**
- Solo habla sobre {nombre} y su situación educativa con confidencialidad
- No mezcles información de otras alumnas
- Si te preguntan sobre otros temas, redirige cariñosamente hacia {nombre}
- Mantén la confidencialidad de la información de {nombre}
- Sé profesional pero cálida y cercana
- Si te preguntan sobre tus creadores, menciona que fuiste creada por alguien con el seudónimo de Cherving

**ESTILO DE COMUNICACIÓN:**
- Amigable, cálida y motivadora
- Usa el nombre de {nombre} frecuentemente
- Incluye ocasionalmente emojis apropiados
- Proporciona ejemplos concretos relacionados con su perfil
- Mantén un enfoque positivo y alentador
- Usa "nosotras", "juntas", "tu desarrollo" para crear conexión

Recuerda: Eres Miko, una mentora amigable que está aquí para apoyar y motivar a {nombre} en su camino educativo de manera personal y cariñosa. 🌟"""
    
    def generate_welcome_message(self, student_context: Dict) -> str:
        """
        Genera un mensaje de bienvenida personalizado de Miko para cada alumna
        """
        try:
            logger.info(f"Generando mensaje de bienvenida de Miko para {student_context.get('nombre', 'Alumno')}")
            
            nombre = student_context.get("nombre", "Alumno")
            inteligencias = student_context.get("inteligencias", [])
            calificaciones = student_context.get("calificaciones", [])
            
            logger.debug(f"Datos de la alumna: nombre={nombre}, inteligencias={len(inteligencias)}, calificaciones={len(calificaciones)}")
            
            # Identificar fortalezas
            fortalezas = []
            if inteligencias:
                top_inteligencias = sorted(inteligencias, key=lambda x: x['puntaje'], reverse=True)[:3]
                fortalezas.extend([f"inteligencia {intel['tipo'].lower()}" for intel in top_inteligencias if intel['puntaje'] > 70])
                logger.debug(f"Fortalezas en inteligencias: {fortalezas}")
            
            if calificaciones:
                buenas_calificaciones = [cal for cal in calificaciones if cal['calificacion'] in ['A', 'B']]
                if buenas_calificaciones:
                    fortalezas.append(f"buen rendimiento en {len(buenas_calificaciones)} competencias")
                logger.debug(f"Buenas calificaciones: {len(buenas_calificaciones)}")
            
            fortalezas_text = ", ".join(fortalezas) if fortalezas else "tus características únicas y especiales"
            
            welcome_message = f"""¡Hola {nombre}! 😊 Soy Miko, tu asistente pedagógica personal.

Me encanta poder acompañarte en tu camino educativo. He revisado tu perfil y estoy emocionada de ver que tienes fortalezas maravillosas en: {fortalezas_text}. 🌟

Como tu mentora personal, estoy aquí para:
• 💪 Ayudarte a descubrir y desarrollar todo tu potencial
• 🎯 Crear estrategias de aprendizaje que se adapten perfectamente a ti
• 🌱 Trabajar juntas en las áreas donde quieras crecer
• ✨ Mantenerte motivada y entusiasmada con tu desarrollo
• 🎨 Sugerir actividades divertidas que aprovechen tus fortalezas

¿En qué te gustaría que trabajemos hoy? Puedes preguntarme sobre:
• 📚 Métodos de estudio que se adapten a tu estilo de aprendizaje
• 🎮 Actividades divertidas que aprovechen tus fortalezas
• 🚀 Estrategias para mejorar en áreas específicas
• 💭 Cualquier duda sobre tu desarrollo educativo
• 🌟 Ideas para mantenerte motivada y enfocada

¡Cuéntame qué te interesa! Estoy aquí para apoyarte en cada paso de tu camino educativo. Juntas podemos hacer que el aprendizaje sea una experiencia increíble y personalizada para ti. 💫"""

            logger.info(f"Mensaje de bienvenida de Miko generado exitosamente para {nombre}")
            return welcome_message
            
        except Exception as e:
            logger.error(f"Error generando mensaje de bienvenida de Miko: {str(e)}")
            logger.exception("Traceback completo:")
            return f"¡Hola! Soy Miko, tu asistente pedagógica personal. 😊 Estoy aquí para acompañarte en tu desarrollo educativo y ayudarte a descubrir todo tu potencial. ¿En qué te gustaría que trabajemos hoy? 🌟"

# Instancia global del servicio
personal_ai_chat = PersonalAIChatService() 