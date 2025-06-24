#!/usr/bin/env python3
"""
Script para verificar y mostrar información sobre las inteligencias en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import SessionLocal
from app.database import models
from sqlalchemy import func

def verificar_inteligencias():
    """Verificar el estado de las inteligencias en la base de datos"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("VERIFICACIÓN DE INTELIGENCIAS EN LA BASE DE DATOS")
        print("=" * 60)
        
        # 1. Contar total de inteligencias
        total_inteligencias = db.query(models.Inteligencia).count()
        print(f"\n1. Total de inteligencias registradas: {total_inteligencias}")
        
        if total_inteligencias == 0:
            print("   ⚠️  No hay inteligencias registradas en la base de datos")
            return
        
        # 2. Contar alumnos con inteligencias
        alumnos_con_inteligencias = db.query(func.count(func.distinct(models.Inteligencia.Alumno_ID))).scalar()
        print(f"\n2. Alumnos con inteligencias registradas: {alumnos_con_inteligencias}")
        
        # 3. Tipos de inteligencia únicos
        tipos_inteligencia = db.query(models.Inteligencia.Tipo_Inteligencia).distinct().all()
        tipos_list = [tipo[0] for tipo in tipos_inteligencia]
        print(f"\n3. Tipos de inteligencia encontrados ({len(tipos_list)}):")
        for i, tipo in enumerate(tipos_list, 1):
            print(f"   {i}. {tipo}")
        
        # 4. Estadísticas por tipo de inteligencia
        print(f"\n4. Estadísticas por tipo de inteligencia:")
        stats = db.query(
            models.Inteligencia.Tipo_Inteligencia,
            func.count(models.Inteligencia.Inteligencia_ID).label('cantidad'),
            func.avg(models.Inteligencia.Puntaje).label('promedio'),
            func.min(models.Inteligencia.Puntaje).label('minimo'),
            func.max(models.Inteligencia.Puntaje).label('maximo')
        ).group_by(models.Inteligencia.Tipo_Inteligencia).all()
        
        for stat in stats:
            print(f"   • {stat.Tipo_Inteligencia}:")
            print(f"     - Cantidad: {stat.cantidad}")
            print(f"     - Promedio: {float(stat.promedio):.2f}")
            print(f"     - Rango: {float(stat.minimo)} - {float(stat.maximo)}")
        
        # 5. Alumnos con más inteligencias registradas
        print(f"\n5. Alumnos con más inteligencias registradas:")
        alumnos_inteligencias = db.query(
            models.Alumno.Nombre,
            func.count(models.Inteligencia.Inteligencia_ID).label('cantidad_inteligencias')
        ).join(models.Inteligencia).group_by(models.Alumno.Alumno_ID, models.Alumno.Nombre).order_by(
            func.count(models.Inteligencia.Inteligencia_ID).desc()
        ).limit(10).all()
        
        for alumno in alumnos_inteligencias:
            print(f"   • {alumno.Nombre}: {alumno.cantidad_inteligencias} inteligencias")
        
        # 6. Verificar consistencia de datos
        print(f"\n6. Verificación de consistencia:")
        
        # Alumnos sin inteligencias
        total_alumnos = db.query(models.Alumno).count()
        alumnos_sin_inteligencias = total_alumnos - alumnos_con_inteligencias
        print(f"   • Alumnos totales: {total_alumnos}")
        print(f"   • Alumnos con inteligencias: {alumnos_con_inteligencias}")
        print(f"   • Alumnos sin inteligencias: {alumnos_sin_inteligencias}")
        
        if alumnos_sin_inteligencias > 0:
            print(f"   ⚠️  Hay {alumnos_sin_inteligencias} alumnos sin inteligencias registradas")
        
        # 7. Muestra de datos
        print(f"\n7. Muestra de datos de inteligencias (primeras 5):")
        inteligencias_muestra = db.query(models.Inteligencia).limit(5).all()
        
        for intel in inteligencias_muestra:
            alumno = db.query(models.Alumno).filter(models.Alumno.Alumno_ID == intel.Alumno_ID).first()
            print(f"   • {alumno.Nombre if alumno else 'Alumno no encontrado'} - {intel.Tipo_Inteligencia}: {intel.Puntaje}")
        
        print("\n" + "=" * 60)
        print("VERIFICACIÓN COMPLETADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error durante la verificación: {str(e)}")
    finally:
        db.close()

def mostrar_inteligencias_alumno(nombre_alumno):
    """Mostrar las inteligencias de un alumno específico"""
    db = SessionLocal()
    
    try:
        print(f"\nBuscando inteligencias para: {nombre_alumno}")
        
        alumno = db.query(models.Alumno).filter(models.Alumno.Nombre.like(f"%{nombre_alumno}%")).first()
        
        if not alumno:
            print(f"❌ No se encontró ningún alumno con el nombre '{nombre_alumno}'")
            return
        
        print(f"✅ Alumno encontrado: {alumno.Nombre} (ID: {alumno.Alumno_ID})")
        
        inteligencias = db.query(models.Inteligencia).filter(
            models.Inteligencia.Alumno_ID == alumno.Alumno_ID
        ).all()
        
        if not inteligencias:
            print(f"⚠️  El alumno {alumno.Nombre} no tiene inteligencias registradas")
            return
        
        print(f"\nInteligencias de {alumno.Nombre}:")
        print("-" * 40)
        
        for intel in inteligencias:
            print(f"• {intel.Tipo_Inteligencia}: {intel.Puntaje}")
        
        # Calcular promedio
        puntajes = [intel.Puntaje for intel in inteligencias]
        promedio = sum(puntajes) / len(puntajes)
        print(f"\nPromedio de inteligencias: {promedio:.2f}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Verificar inteligencias en la base de datos")
    parser.add_argument("--alumno", "-a", help="Buscar inteligencias de un alumno específico")
    
    args = parser.parse_args()
    
    if args.alumno:
        mostrar_inteligencias_alumno(args.alumno)
    else:
        verificar_inteligencias() 