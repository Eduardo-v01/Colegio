#!/usr/bin/env python3
"""
Script para migrar la base de datos y añadir la nueva tabla de conversaciones de IA.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import engine
from app.database import models

def migrate_database():
    """Migrar la base de datos para añadir la nueva tabla de conversaciones"""
    try:
        print("🔄 Iniciando migración de base de datos...")
        
        # Crear todas las tablas (incluyendo la nueva ConversacionesIA)
        models.Base.metadata.create_all(bind=engine)
        
        print("✅ Migración completada exitosamente!")
        print("📋 Tablas creadas/actualizadas:")
        print("   - Alumnos")
        print("   - Profesores") 
        print("   - Cursos")
        print("   - ProfesorCurso")
        print("   - CompetenciaPlantilla")
        print("   - AlumnoCompetencia")
        print("   - Inteligencias")
        print("   - CI")
        print("   - ConversacionesIA (NUEVA)")
        
        print("\n🎉 La base de datos está lista para el chat personal de IA!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
    
    return True

if __name__ == "__main__":
    migrate_database() 