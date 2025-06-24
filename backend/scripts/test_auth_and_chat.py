#!/usr/bin/env python3
"""
Script para probar la autenticación y el chat personal.
"""

import requests
import json

def test_auth_and_chat():
    """Probar autenticación y chat personal"""
    base_url = "http://localhost:8001"
    
    print("🧪 Probando autenticación y chat personal...")
    
    # 1. Probar login
    print("\n1️⃣ Probando login...")
    try:
        login_data = {
            'username': '12345678',  # DNI del profesor
            'password': 'password123'
        }
        
        response = requests.post(
            f"{base_url}/api/profesores/token",
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            print(f"✅ Login exitoso - Token obtenido: {token[:20]}...")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False
    
    # 2. Probar endpoint de bienvenida
    print("\n2️⃣ Probando endpoint de bienvenida...")
    try:
        response = requests.get(
            f"{base_url}/api/personal-chat/welcome/1",
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bienvenida exitosa para: {data.get('student_name')}")
            print(f"   Mensaje: {data.get('welcome_message', '')[:50]}...")
        else:
            print(f"❌ Error en bienvenida: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en bienvenida: {e}")
        return False
    
    # 3. Probar envío de mensaje
    print("\n3️⃣ Probando envío de mensaje...")
    try:
        message_data = {
            'mensaje': '¿Qué puedo hacer para mejorar mis notas?',
            'alumno_id': 1
        }
        
        response = requests.post(
            f"{base_url}/api/personal-chat/send-message",
            json=message_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Mensaje enviado exitosamente")
            print(f"   Respuesta de IA: {data.get('Mensaje', '')[:100]}...")
        else:
            print(f"❌ Error enviando mensaje: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")
        return False
    
    # 4. Probar historial
    print("\n4️⃣ Probando historial...")
    try:
        response = requests.get(
            f"{base_url}/api/personal-chat/history/1",
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Historial obtenido: {data.get('total_mensajes', 0)} mensajes")
        else:
            print(f"❌ Error obteniendo historial: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error obteniendo historial: {e}")
        return False
    
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    return True

if __name__ == "__main__":
    test_auth_and_chat() 