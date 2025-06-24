#!/usr/bin/env python3
"""
Script para probar específicamente el endpoint de bienvenida.
"""

import requests
import json

def test_welcome_endpoint():
    """Probar el endpoint de bienvenida"""
    base_url = "http://localhost:8001"
    
    print("🧪 Probando endpoint de bienvenida...")
    
    # Probar con diferentes IDs de alumnos
    test_ids = [1, 2, 3, 4, 6, 7]
    
    for alumno_id in test_ids:
        print(f"\n📚 Probando alumno_id: {alumno_id}")
        
        try:
            url = f"{base_url}/api/personal-chat/welcome/{alumno_id}"
            print(f"URL: {url}")
            
            response = requests.get(url, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                print(f"   - Success: {data.get('success')}")
                print(f"   - Student Name: {data.get('student_name')}")
                print(f"   - Welcome Message: {data.get('welcome_message', '')[:100]}...")
            else:
                print(f"❌ Error {response.status_code}:")
                try:
                    error_data = response.json()
                    print(f"   - Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   - Response: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión: El servidor no está corriendo")
            break
        except requests.exceptions.Timeout:
            print("❌ Timeout: La petición tardó demasiado")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_welcome_endpoint() 