#!/usr/bin/env python3
"""
Script para probar el chat personal de IA.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import crud, database
from app.services import personal_ai_chat

def test_personal_chat():
    """Probar el chat personal de IA"""
    try:
        print("🧪 Iniciando pruebas del chat personal...")
        
        # Obtener sesión de base de datos
        db = next(database.get_db())
        
        # Obtener un alumno de prueba
        alumnos = crud.get_alumnos(db, limit=1)
        if not alumnos:
            print("❌ No hay alumnos en la base de datos para probar")
            return False
        
        alumno = alumnos[0]
        print(f"📚 Probando con alumno: {alumno.Nombre} (ID: {alumno.Alumno_ID})")
        
        # Probar obtención de contexto
        print("🔍 Obteniendo contexto del alumno...")
        context = crud.get_alumno_conversacion_context(db, alumno.Alumno_ID)
        
        if not context:
            print("❌ Error: No se pudo obtener el contexto del alumno")
            return False
        
        print("✅ Contexto obtenido exitosamente:")
        print(f"   - Nombre: {context['nombre']}")
        print(f"   - CI: {context['ci']} ({context['categoria_ci']})")
        print(f"   - Inteligencias: {len(context['inteligencias'])}")
        print(f"   - Calificaciones: {len(context['calificaciones'])}")
        
        # Probar generación de mensaje de bienvenida
        print("\n🤖 Generando mensaje de bienvenida...")
        welcome_message = personal_ai_chat.generate_welcome_message(context)
        
        if not welcome_message:
            print("❌ Error: No se pudo generar el mensaje de bienvenida")
            return False
        
        print("✅ Mensaje de bienvenida generado:")
        print(f"   {welcome_message[:100]}...")
        
        # Probar chat con contexto
        print("\n💬 Probando chat con contexto...")
        test_message = "¿Qué puedo hacer para mejorar mis notas?"
        chat_response = personal_ai_chat.chat_with_student_context(
            context, [], test_message
        )
        
        if not chat_response.get("success"):
            print(f"❌ Error en chat: {chat_response.get('error')}")
            return False
        
        print("✅ Chat funcionando correctamente:")
        print(f"   Respuesta: {chat_response['response'][:100]}...")
        
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_personal_chat() 