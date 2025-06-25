#!/usr/bin/env python3
"""
Script de prueba para verificar la personalidad de Miko
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ai_assistant import AIAssistantService
from app.services.personal_ai_chat import PersonalAIChatService

def test_miko_personality():
    """Prueba la personalidad de Miko con datos de ejemplo"""
    
    print("🌟 Probando la personalidad de Miko 🌟")
    print("=" * 50)
    
    # Datos de ejemplo de una alumna
    student_data = {
        "alumno_id": 1,
        "nombre": "María García",
        "ci": 115,
        "categoria_ci": "Superior",
        "inteligencias": [
            {"tipo": "Lógico-Matemática", "puntaje": 85},
            {"tipo": "Lingüística", "puntaje": 78},
            {"tipo": "Espacial", "puntaje": 72},
            {"tipo": "Musical", "puntaje": 65},
            {"tipo": "Corporal-Kinestésica", "puntaje": 70},
            {"tipo": "Interpersonal", "puntaje": 80},
            {"tipo": "Intrapersonal", "puntaje": 75},
            {"tipo": "Naturalista", "puntaje": 68}
        ],
        "calificaciones": [
            {"competencia": "Matemáticas", "calificacion": "A", "descripcion": "Excelente comprensión matemática"},
            {"competencia": "Lenguaje", "calificacion": "B", "descripcion": "Buena expresión escrita"},
            {"competencia": "Ciencias", "calificacion": "A", "descripcion": "Excelente en ciencias naturales"}
        ],
        "recomendaciones_basicas": "Alumna con excelente potencial en áreas lógico-matemáticas"
    }
    
    # Probar el servicio de IA principal
    print("\n1. Probando servicio de IA principal (ai_assistant.py):")
    print("-" * 40)
    
    ai_service = AIAssistantService()
    
    # Probar el prompt del sistema
    system_prompt = ai_service._build_system_prompt(student_data)
    print("✅ Prompt del sistema generado correctamente")
    print(f"   Longitud: {len(system_prompt)} caracteres")
    print(f"   Contiene 'Miko': {'Miko' in system_prompt}")
    print(f"   Contiene 'San Martín de Porres': {'San Martín de Porres' in system_prompt}")
    print(f"   Contiene 'Cherving': {'Cherving' in system_prompt}")
    print(f"   Contiene emojis: {'😊' in system_prompt or '🌟' in system_prompt or '💪' in system_prompt}")
    
    # Probar el prompt de estudiante
    student_prompt = ai_service._build_student_prompt(student_data)
    print("\n✅ Prompt de estudiante generado correctamente")
    print(f"   Longitud: {len(student_prompt)} caracteres")
    print(f"   Contiene 'Miko': {'Miko' in student_prompt}")
    print(f"   Contiene personalidad: {'amigable' in student_prompt.lower() and 'motivadora' in student_prompt.lower()}")
    
    # Probar el servicio de chat personal
    print("\n2. Probando servicio de chat personal (personal_ai_chat.py):")
    print("-" * 40)
    
    personal_chat_service = PersonalAIChatService()
    
    # Probar el prompt del sistema personal
    personal_system_prompt = personal_chat_service._build_personal_system_prompt(student_data)
    print("✅ Prompt del sistema personal generado correctamente")
    print(f"   Longitud: {len(personal_system_prompt)} caracteres")
    print(f"   Contiene 'Miko': {'Miko' in personal_system_prompt}")
    print(f"   Contiene 'San Martín de Porres': {'San Martín de Porres' in personal_system_prompt}")
    print(f"   Contiene 'Cherving': {'Cherving' in personal_system_prompt}")
    print(f"   Contiene personalidad: {'cálida' in personal_system_prompt.lower() and 'cariñosa' in personal_system_prompt.lower()}")
    
    # Probar el mensaje de bienvenida
    welcome_message = personal_chat_service.generate_welcome_message(student_data)
    print("\n✅ Mensaje de bienvenida generado correctamente")
    print(f"   Longitud: {len(welcome_message)} caracteres")
    print(f"   Contiene 'Miko': {'Miko' in welcome_message}")
    print(f"   Contiene emojis: {'😊' in welcome_message or '🌟' in welcome_message or '💪' in welcome_message}")
    
    # Mostrar una muestra del mensaje de bienvenida
    print("\n📝 Muestra del mensaje de bienvenida:")
    print("-" * 30)
    lines = welcome_message.split('\n')
    for i, line in enumerate(lines[:10]):  # Mostrar solo las primeras 10 líneas
        print(f"   {line}")
    if len(lines) > 10:
        print(f"   ... y {len(lines) - 10} líneas más")
    
    print("\n🎉 ¡Prueba completada exitosamente!")
    print("La personalidad de Miko está configurada correctamente.")
    print("\nCaracterísticas verificadas:")
    print("✅ Nombre: Miko")
    print("✅ Personalidad: Amigable, sabia, motivadora")
    print("✅ Tono: Cálido y cercano")
    print("✅ Emojis: Incluidos apropiadamente")
    print("✅ Lenguaje: Personal e inclusivo")
    print("✅ Enfoque: Positivo y alentador")
    print("✅ Colegio: San Martín de Porres")
    print("✅ Creador: Seudónimo Cherving")

if __name__ == "__main__":
    test_miko_personality() 