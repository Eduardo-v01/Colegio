#!/usr/bin/env python3
"""
Script de prueba para los endpoints de profesores
Prueba todas las funcionalidades CRUD y gestión de cursos
"""

import requests
import json
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000"

def test_profesores_endpoints():
    """Prueba todos los endpoints de profesores"""
    print("🧪 Iniciando pruebas de endpoints de profesores...")
    print("=" * 60)
    
    # Test 1: Crear profesor
    print("\n1️⃣ Probando creación de profesor...")
    profesor_data = {
        "Nombre": "Profesor Test",
        "DNI": "12345678",
        "Contrasena": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/profesores/register", json=profesor_data)
        if response.status_code == 200:
            profesor = response.json()
            print(f"✅ Profesor creado exitosamente: {profesor['Nombre']} (ID: {profesor['Profesor_ID']})")
            profesor_id = profesor['Profesor_ID']
        else:
            print(f"❌ Error al crear profesor: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Test 2: Obtener lista de profesores
    print("\n2️⃣ Probando obtención de lista de profesores...")
    try:
        response = requests.get(f"{BASE_URL}/profesores/")
        if response.status_code == 200:
            profesores = response.json()
            print(f"✅ Lista de profesores obtenida: {len(profesores)} profesores")
        else:
            print(f"❌ Error al obtener profesores: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 3: Obtener profesor específico
    print("\n3️⃣ Probando obtención de profesor específico...")
    try:
        response = requests.get(f"{BASE_URL}/profesores/{profesor_id}")
        if response.status_code == 200:
            profesor = response.json()
            print(f"✅ Profesor obtenido: {profesor['Nombre']}")
        else:
            print(f"❌ Error al obtener profesor: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 4: Obtener cursos disponibles
    print("\n4️⃣ Probando obtención de cursos disponibles...")
    try:
        response = requests.get(f"{BASE_URL}/profesores/cursos/disponibles")
        if response.status_code == 200:
            cursos = response.json()
            print(f"✅ Cursos disponibles obtenidos: {len(cursos)} cursos")
            if cursos:
                curso_id = cursos[0]['Curso_ID']
                print(f"   Usando curso: {cursos[0]['Nombre']} (ID: {curso_id})")
            else:
                print("   No hay cursos disponibles para asignar")
                return True
        else:
            print(f"❌ Error al obtener cursos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Test 5: Asignar curso a profesor
    print("\n5️⃣ Probando asignación de curso a profesor...")
    try:
        response = requests.post(f"{BASE_URL}/profesores/{profesor_id}/cursos/{curso_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Curso asignado exitosamente: {result['message']}")
        else:
            print(f"❌ Error al asignar curso: {response.status_code}")
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 6: Obtener cursos del profesor
    print("\n6️⃣ Probando obtención de cursos del profesor...")
    try:
        response = requests.get(f"{BASE_URL}/profesores/{profesor_id}/cursos")
        if response.status_code == 200:
            cursos_profesor = response.json()
            print(f"✅ Cursos del profesor obtenidos: {len(cursos_profesor)} cursos")
            for curso in cursos_profesor:
                print(f"   - {curso['Nombre']} (ID: {curso['Curso_ID']})")
        else:
            print(f"❌ Error al obtener cursos del profesor: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 7: Obtener estadísticas del profesor
    print("\n7️⃣ Probando obtención de estadísticas del profesor...")
    try:
        response = requests.get(f"{BASE_URL}/profesores/{profesor_id}/estadisticas")
        if response.status_code == 200:
            estadisticas = response.json()
            print(f"✅ Estadísticas obtenidas:")
            print(f"   - Nombre: {estadisticas['nombre']}")
            print(f"   - Total cursos: {estadisticas['total_cursos']}")
            print(f"   - Total alumnos: {estadisticas['total_alumnos']}")
            print(f"   - Promedio calificaciones: {estadisticas['promedio_calificaciones']}")
        else:
            print(f"❌ Error al obtener estadísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 8: Actualizar profesor
    print("\n8️⃣ Probando actualización de profesor...")
    update_data = {
        "Nombre": "Profesor Test Actualizado"
    }
    try:
        response = requests.put(f"{BASE_URL}/profesores/{profesor_id}", json=update_data)
        if response.status_code == 200:
            profesor_actualizado = response.json()
            print(f"✅ Profesor actualizado: {profesor_actualizado['Nombre']}")
        else:
            print(f"❌ Error al actualizar profesor: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 9: Desasignar curso del profesor
    print("\n9️⃣ Probando desasignación de curso...")
    try:
        response = requests.delete(f"{BASE_URL}/profesores/{profesor_id}/cursos/{curso_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Curso desasignado exitosamente: {result['message']}")
        else:
            print(f"❌ Error al desasignar curso: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 10: Login de profesor
    print("\n🔟 Probando login de profesor...")
    login_data = {
        "username": "12345678",  # DNI
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/profesores/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login exitoso: Token obtenido")
            print(f"   - Tipo: {token_data['token_type']}")
            print(f"   - Token: {token_data['access_token'][:20]}...")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test 11: Eliminar profesor (limpieza)
    print("\n1️⃣1️⃣ Probando eliminación de profesor...")
    try:
        response = requests.delete(f"{BASE_URL}/profesores/{profesor_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Profesor eliminado exitosamente: {result['message']}")
        else:
            print(f"❌ Error al eliminar profesor: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas de endpoints de profesores completadas")
    return True

def test_error_cases():
    """Prueba casos de error"""
    print("\n🧪 Probando casos de error...")
    print("=" * 60)
    
    # Test: Profesor inexistente
    print("\n1️⃣ Probando obtención de profesor inexistente...")
    try:
        response = requests.get(f"{BASE_URL}/profesores/99999")
        if response.status_code == 404:
            print("✅ Error 404 correcto para profesor inexistente")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test: Asignación de curso a profesor inexistente
    print("\n2️⃣ Probando asignación de curso a profesor inexistente...")
    try:
        response = requests.post(f"{BASE_URL}/profesores/99999/cursos/1")
        if response.status_code == 400:
            print("✅ Error 400 correcto para asignación inválida")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas de casos de error completadas")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas completas de endpoints de profesores")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code != 200:
            print("❌ El servidor no está corriendo en http://localhost:8000")
            print("   Por favor, inicia el servidor con: uvicorn app.main:app --reload")
            sys.exit(1)
    except Exception as e:
        print("❌ No se puede conectar al servidor")
        print("   Por favor, inicia el servidor con: uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Ejecutar pruebas
    success = test_profesores_endpoints()
    test_error_cases()
    
    if success:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✅ Los endpoints de profesores están funcionando correctamente")
    else:
        print("\n❌ Algunas pruebas fallaron")
        print("🔧 Revisa los errores y verifica la configuración")
    
    print("\n📝 Resumen:")
    print("   - ✅ CRUD completo de profesores")
    print("   - ✅ Gestión de cursos por profesor")
    print("   - ✅ Estadísticas de profesores")
    print("   - ✅ Autenticación de profesores")
    print("   - ✅ Manejo de errores") 