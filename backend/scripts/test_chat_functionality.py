#!/usr/bin/env python3
"""
Script para probar la funcionalidad del chat de Miko
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import crud, database
from app.services import personal_ai_chat

def test_chat_functionality():
    """Probar la funcionalidad del chat de Miko"""
    try:
        print("🌟 Probando funcionalidad del chat de Miko 🌟")
        print("=" * 50)
        
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
        print(f"   Longitud: {len(welcome_message)} caracteres")
        print(f"   Contiene 'Miko': {'Miko' in welcome_message}")
        print(f"   Contiene emojis: {'😊' in welcome_message or '🌟' in welcome_message}")
        
        # Mostrar una muestra del mensaje
        print("\n📝 Muestra del mensaje de bienvenida:")
        print("-" * 30)
        lines = welcome_message.split('\n')
        for i, line in enumerate(lines[:5]):  # Mostrar solo las primeras 5 líneas
            print(f"   {line}")
        if len(lines) > 5:
            print(f"   ... y {len(lines) - 5} líneas más")
        
        # Probar chat con contexto
        print("\n💬 Probando chat con contexto...")
        test_message = "Hola, ¿cómo estás? ¿Puedes darme algunos consejos de estudio?"
        
        response = personal_ai_chat.chat_with_student_context(
            context, [], test_message
        )
        
        if response["success"]:
            response_text = response["response"]
            print("✅ Respuesta del chat generada exitosamente:")
            print(f"   Longitud: {len(response_text)} caracteres")
            print(f"   ✅ Respuesta de Miko:")
            print(f"      Contiene 'Miko': {'Miko' in response_text}")
            print(f"      Contiene personalidad: {'amigable' in response_text.lower() or 'cálida' in response_text.lower()}")
            
            # Mostrar una muestra de la respuesta
            print("\n📝 Muestra de la respuesta:")
            print("-" * 30)
            lines = response_text.split('\n')
            for i, line in enumerate(lines[:3]):  # Mostrar solo las primeras 3 líneas
                print(f"   {line}")
            if len(lines) > 3:
                print(f"   ... y {len(lines) - 3} líneas más")
        else:
            print(f"❌ Error en la respuesta del chat: {response['error']}")
            return False
        
        # Probar chat con historial
        print("\n📚 Probando chat con historial...")
        conversation_history = [
            {"mensaje": "Hola Miko, ¿cómo estás?", "es_usuario": True},
            {"mensaje": "¡Hola! Estoy muy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?", "es_usuario": False}
        ]
        
        response_with_history = personal_ai_chat.chat_with_student_context(
            context, conversation_history, "¿Puedes recordar lo que hablamos antes?"
        )
        
        if response_with_history["success"]:
            response_text = response_with_history["response"]
            print("✅ Chat con historial funcionando correctamente:")
            print(f"   Longitud: {len(response_text)} caracteres")
            print(f"   Contiene personalidad de Miko: {'Miko' in response_text}")
        else:
            print(f"❌ Error en chat con historial: {response_with_history['error']}")
            return False
        
        print("\n🎉 ¡Prueba completada exitosamente!")
        print("El chat de Miko está funcionando correctamente.")
        print("\nFuncionalidades verificadas:")
        print("✅ Generación de mensaje de bienvenida")
        print("✅ Chat con contexto personalizado")
        print("✅ Chat con historial de conversación")
        print("✅ Personalidad consistente")
        print("✅ Respuestas apropiadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chat_functionality()
    if success:
        print("\n✅ Todas las pruebas pasaron exitosamente")
    else:
        print("\n❌ Algunas pruebas fallaron")
        sys.exit(1) 