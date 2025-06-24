#!/usr/bin/env python3
"""
Script para probar el chat público sin autenticación.
"""

import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_public_chat():
    """Probar chat público sin autenticación"""
    print("🧪 Probando chat público sin autenticación...")
    print()
    
    # 1. Probar bienvenida
    print("1️⃣ Probando bienvenida sin autenticación...")
    try:
        response = requests.get(f"{BASE_URL}/personal-chat/welcome/1")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Bienvenida exitosa")
            print(f"   Mensaje: {data.get('welcome_message', 'N/A')[:100]}...")
            print(f"   Estructura completa: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 2. Probar envío de mensaje
    print("2️⃣ Probando envío de mensaje público...")
    try:
        chat_data = {
            "mensaje": "¿Qué puedo hacer para mejorar mis notas?",
            "alumno_id": 1
        }
        
        response = requests.post(
            f"{BASE_URL}/personal-chat/send-message-public",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Mensaje enviado exitosamente")
            print(f"   Estructura de respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
            print(f"   Campo 'mensaje': {data.get('mensaje', 'NO EXISTE')}")
            print(f"   Campo 'Mensaje': {data.get('Mensaje', 'NO EXISTE')}")
            print(f"   Todos los campos: {list(data.keys())}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 3. Probar con otro alumno
    print("3️⃣ Probando con otro alumno...")
    try:
        chat_data = {
            "mensaje": "Hola, ¿cómo estás?",
            "alumno_id": 2
        }
        
        response = requests.post(
            f"{BASE_URL}/personal-chat/send-message-public",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Mensaje enviado exitosamente para alumno 2")
            print(f"   Campo 'mensaje': {data.get('mensaje', 'NO EXISTE')}")
            print(f"   Campo 'Mensaje': {data.get('Mensaje', 'NO EXISTE')}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("🎉 ¡Pruebas completadas!")

if __name__ == "__main__":
    test_public_chat() 