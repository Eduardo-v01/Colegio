#!/usr/bin/env python3
"""
Script para diagnosticar problemas en la base de datos.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import crud, database
from app.database import models

def diagnose_database():
    """Diagnosticar problemas en la base de datos"""
    try:
        print("🔍 Iniciando diagnóstico de la base de datos...")
        
        # Obtener sesión de base de datos
        db = next(database.get_db())
        
        # 1. Verificar tablas
        print("\n📋 Verificando tablas...")
        try:
            # Verificar si las tablas existen
            from sqlalchemy import inspect
            inspector = inspect(db.bind)
            tables = inspector.get_table_names()
            print(f"✅ Tablas encontradas: {tables}")
        except Exception as e:
            print(f"❌ Error verificando tablas: {e}")
        
        # 2. Verificar alumnos
        print("\n👥 Verificando alumnos...")
        try:
            alumnos = crud.get_alumnos(db, limit=10)
            print(f"✅ Alumnos encontrados: {len(alumnos)}")
            for alumno in alumnos[:3]:  # Mostrar solo los primeros 3
                print(f"   - {alumno.Nombre} (ID: {alumno.Alumno_ID}, CI: {alumno.CI})")
        except Exception as e:
            print(f"❌ Error verificando alumnos: {e}")
        
        # 3. Verificar inteligencias
        print("\n🧠 Verificando inteligencias...")
        try:
            inteligencias = db.query(models.Inteligencia).limit(10).all()
            print(f"✅ Inteligencias encontradas: {len(inteligencias)}")
            if inteligencias:
                print(f"   - Ejemplo: {inteligencias[0].Tipo_Inteligencia} (Puntaje: {inteligencias[0].Puntaje})")
        except Exception as e:
            print(f"❌ Error verificando inteligencias: {e}")
        
        # 4. Verificar calificaciones
        print("\n📊 Verificando calificaciones...")
        try:
            calificaciones = db.query(models.AlumnoCompetencia).limit(10).all()
            print(f"✅ Calificaciones encontradas: {len(calificaciones)}")
            if calificaciones:
                print(f"   - Ejemplo: Calificación {calificaciones[0].Calificacion}")
        except Exception as e:
            print(f"❌ Error verificando calificaciones: {e}")
        
        # 5. Verificar competencias
        print("\n🎯 Verificando competencias...")
        try:
            competencias = crud.get_competencias(db, limit=10)
            print(f"✅ Competencias encontradas: {len(competencias)}")
            for comp in competencias[:3]:
                print(f"   - {comp.Codigo_Competencia}: {comp.Descripcion}")
        except Exception as e:
            print(f"❌ Error verificando competencias: {e}")
        
        # 6. Probar función de contexto específica
        print("\n🔍 Probando función get_alumno_conversacion_context...")
        try:
            alumnos = crud.get_alumnos(db, limit=1)
            if alumnos:
                alumno = alumnos[0]
                print(f"Probando con alumno: {alumno.Nombre} (ID: {alumno.Alumno_ID})")
                
                context = crud.get_alumno_conversacion_context(db, alumno.Alumno_ID)
                if context:
                    print("✅ Contexto obtenido exitosamente:")
                    print(f"   - Nombre: {context['nombre']}")
                    print(f"   - CI: {context['ci']}")
                    print(f"   - Inteligencias: {len(context['inteligencias'])}")
                    print(f"   - Calificaciones: {len(context['calificaciones'])}")
                else:
                    print("❌ No se pudo obtener el contexto")
            else:
                print("❌ No hay alumnos para probar")
        except Exception as e:
            print(f"❌ Error probando contexto: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n🎉 Diagnóstico completado!")
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_database() 