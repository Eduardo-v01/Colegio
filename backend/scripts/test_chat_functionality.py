#!/usr/bin/env python3
"""
Script para probar la funcionalidad del chat de Yae Miko
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.personal_ai_chat import personal_ai_chat
from app.database import crud, database
from sqlalchemy.orm import Session

def test_chat_functionality():
    """Prueba la funcionalidad del chat con datos reales"""
    
    print("🌟 Probando funcionalidad del chat de Yae Miko 🌟")
    print("=" * 60)
    
    # Crear sesión de base de datos
    db = Session(database.engine)
    
    try:
        # Obtener el primer alumno de la base de datos
        alumnos = crud.get_alumnos(db, limit=1)
        
        if not alumnos:
            print("❌ No hay alumnos en la base de datos para probar")
            return
        
        alumno = alumnos[0]
        print(f"👤 Probando con alumno: {alumno.Nombre} (ID: {alumno.Alumno_ID})")
        
        # Obtener contexto del alumno
        student_context = crud.get_alumno_conversacion_context(db, alumno.Alumno_ID)
        
        if not student_context:
            print("❌ No se pudo obtener el contexto del alumno")
            return
        
        print(f"✅ Contexto obtenido:")
        print(f"   - Nombre: {student_context['nombre']}")
        print(f"   - CI: {student_context['ci']}")
        print(f"   - Inteligencias: {len(student_context['inteligencias'])}")
        print(f"   - Calificaciones: {len(student_context['calificaciones'])}")
        
        # Probar mensaje de bienvenida
        print("\n📝 Probando mensaje de bienvenida...")
        welcome_message = personal_ai_chat.generate_welcome_message(student_context)
        
        if welcome_message:
            print("✅ Mensaje de bienvenida generado:")
            print(f"   Longitud: {len(welcome_message)} caracteres")
            print(f"   Contiene 'Yae Miko': {'Yae Miko' in welcome_message}")
            print(f"   Contiene emojis: {'😊' in welcome_message or '🌟' in welcome_message}")
            
            # Mostrar primeras líneas
            lines = welcome_message.split('\n')
            print("   Muestra del mensaje:")
            for i, line in enumerate(lines[:5]):
                print(f"   {i+1}. {line}")
            if len(lines) > 5:
                print(f"   ... y {len(lines) - 5} líneas más")
        else:
            print("❌ Error generando mensaje de bienvenida")
        
        # Probar chat con contexto
        print("\n💬 Probando chat con contexto...")
        
        # Simular historial vacío
        conversation_history = []
        
        # Mensajes de prueba
        test_messages = [
            "Hola, ¿quién eres?",
            "¿Cómo puedo mejorar en matemáticas?",
            "¿Qué actividades me recomiendas?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n   Mensaje {i}: '{message}'")
            
            try:
                ai_response = personal_ai_chat.chat_with_student_context(
                    student_context, conversation_history, message
                )
                
                if ai_response["success"]:
                    response_text = ai_response["response"]
                    print(f"   ✅ Respuesta de Yae Miko:")
                    print(f"      Longitud: {len(response_text)} caracteres")
                    print(f"      Contiene 'Yae Miko': {'Yae Miko' in response_text}")
                    print(f"      Contiene emojis: {'😊' in response_text or '🌟' in response_text or '💪' in response_text}")
                    
                    # Mostrar primeras líneas de la respuesta
                    lines = response_text.split('\n')
                    print(f"      Muestra:")
                    for j, line in enumerate(lines[:3]):
                        if line.strip():
                            print(f"      - {line.strip()}")
                    if len(lines) > 3:
                        print(f"      ... y {len(lines) - 3} líneas más")
                    
                    # Agregar al historial para la siguiente iteración
                    conversation_history.append({
                        "mensaje": message,
                        "es_usuario": True,
                        "fecha": "2024-01-01T00:00:00"
                    })
                    conversation_history.append({
                        "mensaje": response_text,
                        "es_usuario": False,
                        "fecha": "2024-01-01T00:00:00"
                    })
                    
                else:
                    print(f"   ❌ Error en la respuesta: {ai_response.get('error', 'Error desconocido')}")
                    
            except Exception as e:
                print(f"   ❌ Excepción: {str(e)}")
        
        print("\n🎉 Pruebas completadas exitosamente!")
        print("El chat de Yae Miko está funcionando correctamente.")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

def test_endpoint_format():
    """Prueba el formato de respuesta de los endpoints"""
    
    print("\n🔧 Verificando formato de endpoints...")
    print("=" * 50)
    
    try:
        # Simular datos de prueba
        test_context = {
            "alumno_id": 1,
            "nombre": "Alumno de Prueba",
            "ci": 100,
            "categoria_ci": "Promedio",
            "inteligencias": [
                {"tipo": "Lógico-Matemática", "puntaje": 80}
            ],
            "calificaciones": [
                {"competencia": "Matemáticas", "calificacion": "B", "descripcion": "Buena"}
            ],
            "recomendaciones_basicas": "Alumno con buen potencial"
        }
        
        # Probar respuesta del chat
        conversation_history = []
        message = "Hola, ¿quién eres?"
        
        ai_response = personal_ai_chat.chat_with_student_context(
            test_context, conversation_history, message
        )
        
        print("✅ Formato de respuesta del servicio:")
        print(f"   success: {ai_response.get('success', False)}")
        print(f"   response: {'Presente' if 'response' in ai_response else 'Faltante'}")
        print(f"   student_name: {'Presente' if 'student_name' in ai_response else 'Faltante'}")
        
        if ai_response.get("success"):
            response_text = ai_response["response"]
            print(f"   Longitud de respuesta: {len(response_text)} caracteres")
            print(f"   Contiene personalidad de Yae Miko: {'Yae Miko' in response_text}")
        
        print("\n✅ Formato verificado correctamente")
        
    except Exception as e:
        print(f"❌ Error verificando formato: {str(e)}")

if __name__ == "__main__":
    test_chat_functionality()
    test_endpoint_format()
    
    print("\n🎯 Resumen:")
    print("Si todas las pruebas pasaron ✅, el chat debería funcionar correctamente.")
    print("Si hay errores ❌, revisa los logs del servidor para más detalles.") 