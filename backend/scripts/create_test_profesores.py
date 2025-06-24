#!/usr/bin/env python3
"""
Script para crear profesores de prueba en la base de datos.
Permite probar la funcionalidad de login con DNI y nombre.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import SessionLocal
from app.database import crud, models
from app.schemas.profesor import ProfesorCreate

def create_test_profesores():
    """Crear profesores de prueba en la base de datos"""
    db = SessionLocal()
    
    try:
        # Lista de profesores de prueba
        profesores_prueba = [
            {
                "Nombre": "María González López",
                "DNI": "12345678",
                "Contrasena": "password123"
            },
            {
                "Nombre": "Juan Carlos Rodríguez",
                "DNI": "87654321",
                "Contrasena": "password456"
            },
            {
                "Nombre": "Ana Sofía Martínez",
                "DNI": "11223344",
                "Contrasena": "password789"
            },
            {
                "Nombre": "Carlos Eduardo Pérez",
                "DNI": "44332211",
                "Contrasena": "password101"
            }
        ]
        
        print("Creando profesores de prueba...")
        
        for i, profesor_data in enumerate(profesores_prueba, 1):
            # Verificar si el profesor ya existe
            existing_profesor = crud.get_profesor_by_dni(db, dni=profesor_data["DNI"])
            
            if existing_profesor:
                print(f"Profesor {i}: {profesor_data['Nombre']} (DNI: {profesor_data['DNI']}) - YA EXISTE")
                continue
            
            # Crear el profesor
            profesor_create = ProfesorCreate(**profesor_data)
            nuevo_profesor = crud.create_profesor(db=db, profesor=profesor_create)
            
            print(f"Profesor {i}: {nuevo_profesor.Nombre} (DNI: {nuevo_profesor.DNI}) - CREADO")
        
        print("\n✅ Profesores de prueba creados exitosamente!")
        print("\n📋 Información para pruebas:")
        print("=" * 50)
        
        for profesor in profesores_prueba:
            print(f"Nombre: {profesor['Nombre']}")
            print(f"DNI: {profesor['DNI']}")
            print(f"Contraseña: {profesor['Contrasena']}")
            print("-" * 30)
        
        print("\n💡 Puedes iniciar sesión usando:")
        print("   - El DNI completo")
        print("   - El nombre completo")
        print("   - Parte del nombre (ej: 'María', 'Carlos')")
        
    except Exception as e:
        print(f"❌ Error al crear profesores: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_profesores() 