#!/usr/bin/env python3
"""
Script para verificar que la tabla de conversaciones existe y funciona correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.database.database import engine
from app.database import models

def verificar_tabla_conversaciones():
    """Verifica que la tabla de conversaciones existe y funciona"""
    
    print("🔍 Verificando tabla de conversaciones...")
    print("=" * 50)
    
    try:
        # Crear conexión
        with engine.connect() as conn:
            
            # Verificar si la tabla existe
            result = conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='ConversacionesIA'
            """))
            
            table_exists = result.fetchone()
            
            if table_exists:
                print("✅ Tabla 'ConversacionesIA' existe")
                
                # Verificar estructura de la tabla
                result = conn.execute(text("PRAGMA table_info(ConversacionesIA)"))
                columns = result.fetchall()
                
                print(f"📋 Estructura de la tabla:")
                for col in columns:
                    print(f"   - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}")
                
                # Verificar si hay datos
                result = conn.execute(text("SELECT COUNT(*) FROM ConversacionesIA"))
                count = result.fetchone()[0]
                print(f"📊 Registros en la tabla: {count}")
                
                # Verificar claves foráneas
                result = conn.execute(text("PRAGMA foreign_key_list(ConversacionesIA)"))
                foreign_keys = result.fetchall()
                
                if foreign_keys:
                    print("🔗 Claves foráneas configuradas:")
                    for fk in foreign_keys:
                        print(f"   - {fk[3]} -> {fk[4]}.{fk[5]}")
                else:
                    print("⚠️ No se encontraron claves foráneas configuradas")
                
                # Verificar índices
                result = conn.execute(text("PRAGMA index_list(ConversacionesIA)"))
                indexes = result.fetchall()
                
                if indexes:
                    print("📈 Índices encontrados:")
                    for idx in indexes:
                        print(f"   - {idx[1]} ({'UNIQUE' if idx[2] else 'NORMAL'})")
                else:
                    print("ℹ️ No se encontraron índices específicos")
                
                # Probar inserción de un registro de prueba
                print("\n🧪 Probando inserción de registro de prueba...")
                
                # Verificar que existe al menos un alumno y profesor
                result = conn.execute(text("SELECT COUNT(*) FROM Alumnos"))
                alumnos_count = result.fetchone()[0]
                
                result = conn.execute(text("SELECT COUNT(*) FROM Profesores"))
                profesores_count = result.fetchone()[0]
                
                if alumnos_count > 0 and profesores_count > 0:
                    # Obtener primer alumno y profesor
                    result = conn.execute(text("SELECT Alumno_ID FROM Alumnos LIMIT 1"))
                    alumno_id = result.fetchone()[0]
                    
                    result = conn.execute(text("SELECT Profesor_ID FROM Profesores LIMIT 1"))
                    profesor_id = result.fetchone()[0]
                    
                    # Insertar registro de prueba
                    test_message = "Mensaje de prueba de Yae Miko"
                    conn.execute(text("""
                        INSERT INTO ConversacionesIA 
                        (Alumno_ID, Profesor_ID, Mensaje, Es_Usuario, Fecha_Creacion, Contexto_Alumno)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """), (alumno_id, profesor_id, test_message, 0, "2024-01-01T00:00:00", "{}"))
                    
                    conn.commit()
                    print("✅ Inserción de prueba exitosa")
                    
                    # Verificar que se insertó
                    result = conn.execute(text("SELECT COUNT(*) FROM ConversacionesIA"))
                    new_count = result.fetchone()[0]
                    print(f"📊 Nuevo total de registros: {new_count}")
                    
                    # Limpiar registro de prueba
                    conn.execute(text("DELETE FROM ConversacionesIA WHERE Mensaje = ?"), (test_message,))
                    conn.commit()
                    print("🧹 Registro de prueba eliminado")
                    
                else:
                    print("⚠️ No se pueden hacer pruebas de inserción - faltan alumnos o profesores")
                    if alumnos_count == 0:
                        print("   - No hay alumnos en la base de datos")
                    if profesores_count == 0:
                        print("   - No hay profesores en la base de datos")
                
            else:
                print("❌ Tabla 'ConversacionesIA' NO existe")
                print("💡 Creando tabla...")
                
                # Crear la tabla
                models.Base.metadata.create_all(bind=engine)
                print("✅ Tabla creada exitosamente")
                
                # Verificar nuevamente
                result = conn.execute(text("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='ConversacionesIA'
                """))
                
                if result.fetchone():
                    print("✅ Verificación: Tabla creada correctamente")
                else:
                    print("❌ Error: No se pudo crear la tabla")
    
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()

def verificar_endpoints():
    """Verifica que los endpoints están configurados correctamente"""
    
    print("\n🌐 Verificando configuración de endpoints...")
    print("=" * 50)
    
    try:
        # Verificar que el router está importado
        from app.routers import personal_chat
        print("✅ Router personal_chat importado correctamente")
        
        # Verificar que las funciones CRUD existen
        from app.database import crud
        
        functions_to_check = [
            'create_conversacion_message',
            'get_conversacion_history', 
            'clear_conversacion_alumno',
            'get_alumno_conversacion_context'
        ]
        
        for func_name in functions_to_check:
            if hasattr(crud, func_name):
                print(f"✅ Función {func_name} existe")
            else:
                print(f"❌ Función {func_name} NO existe")
        
        # Verificar que el servicio de IA existe
        from app.services import personal_ai_chat
        print("✅ Servicio personal_ai_chat importado correctamente")
        
        # Verificar que el modelo existe
        if hasattr(models, 'ConversacionIA'):
            print("✅ Modelo ConversacionIA existe")
        else:
            print("❌ Modelo ConversacionIA NO existe")
            
    except Exception as e:
        print(f"❌ Error verificando endpoints: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Diagnóstico completo del sistema de conversaciones")
    print("=" * 60)
    
    verificar_tabla_conversaciones()
    verificar_endpoints()
    
    print("\n🎉 Diagnóstico completado")
    print("Si todo está ✅, el sistema de conversaciones debería funcionar correctamente.") 