#!/usr/bin/env python3
"""
Script para crear datos de prueba completos para el sistema.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import crud, database
from app.database import models
from app.schemas import alumno, competencia

def create_test_data():
    """Crear datos de prueba completos"""
    try:
        print("🔄 Creando datos de prueba...")
        
        # Obtener sesión de base de datos
        db = next(database.get_db())
        
        # 1. Crear curso de prueba
        print("📚 Creando curso de prueba...")
        curso_test = models.Curso(Nombre="Matemáticas Básicas")
        db.add(curso_test)
        db.commit()
        db.refresh(curso_test)
        print(f"✅ Curso creado: {curso_test.Nombre}")
        
        # 2. Crear competencias de prueba
        print("🎯 Creando competencias de prueba...")
        competencias_data = [
            {"nombre": "Suma y Resta", "descripcion": "Operaciones básicas de suma y resta"},
            {"nombre": "Multiplicación", "descripcion": "Tablas de multiplicar"},
            {"nombre": "División", "descripcion": "Operaciones de división"},
            {"nombre": "Problemas", "descripcion": "Resolución de problemas matemáticos"}
        ]
        
        competencias_creadas = []
        for comp_data in competencias_data:
            competencia_obj = crud.create_competencia(db, competencia.CompetenciaCreate(**comp_data))
            competencias_creadas.append(competencia_obj)
            print(f"✅ Competencia creada: {competencia_obj.Codigo_Competencia}")
        
        # 3. Crear alumnos de prueba
        print("👥 Creando alumnos de prueba...")
        alumnos_data = [
            {"nombre": "Ana", "apellido": "García", "ci": 115},
            {"nombre": "Carlos", "apellido": "López", "ci": 95},
            {"nombre": "María", "apellido": "Rodríguez", "ci": 125},
            {"nombre": "Juan", "apellido": "Martínez", "ci": 85}
        ]
        
        alumnos_creados = []
        for alumno_data in alumnos_data:
            alumno_obj = crud.create_alumno(db, alumno.AlumnoCreate(**alumno_data))
            # Actualizar CI
            alumno_obj.CI = alumno_data["ci"]
            db.commit()
            alumnos_creados.append(alumno_obj)
            print(f"✅ Alumno creado: {alumno_obj.Nombre} (CI: {alumno_obj.CI})")
        
        # 4. Crear inteligencias de prueba
        print("🧠 Creando inteligencias de prueba...")
        tipos_inteligencias = ["Lógico-Matemática", "Lingüística", "Espacial", "Musical", "Corporal-Kinestésica"]
        
        for alumno_obj in alumnos_creados:
            for i, tipo in enumerate(tipos_inteligencias):
                puntaje = 60 + (i * 10) + (alumno_obj.CI % 20)  # Puntaje variado
                inteligencia = models.Inteligencia(
                    Alumno_ID=alumno_obj.Alumno_ID,
                    Tipo_Inteligencia=tipo,
                    Puntaje=puntaje
                )
                db.add(inteligencia)
            print(f"✅ Inteligencias creadas para {alumno_obj.Nombre}")
        
        # 5. Crear calificaciones de prueba
        print("📊 Creando calificaciones de prueba...")
        
        for alumno_obj in alumnos_creados:
            for comp in competencias_creadas:
                # Calificación basada en CI y competencia
                if "Suma" in comp.Codigo_Competencia:
                    cal = "A" if alumno_obj.CI > 100 else "B"
                elif "Multiplicación" in comp.Codigo_Competencia:
                    cal = "A" if alumno_obj.CI > 110 else "B"
                elif "División" in comp.Codigo_Competencia:
                    cal = "B" if alumno_obj.CI > 90 else "C"
                else:  # Problemas
                    cal = "B" if alumno_obj.CI > 105 else "C"
                
                calificacion = models.AlumnoCompetencia(
                    Alumno_ID=alumno_obj.Alumno_ID,
                    CompetenciaPlantilla_ID=comp.CompetenciaPlantilla_ID,
                    Calificacion=cal,
                    Conclusion_descriptiva=f"Alumno con buen desempeño en {comp.Codigo_Competencia}"
                )
                db.add(calificacion)
            print(f"✅ Calificaciones creadas para {alumno_obj.Nombre}")
        
        db.commit()
        
        print("\n🎉 ¡Datos de prueba creados exitosamente!")
        print(f"📋 Resumen:")
        print(f"   - 1 curso creado")
        print(f"   - {len(competencias_creadas)} competencias creadas")
        print(f"   - {len(alumnos_creados)} alumnos creados")
        print(f"   - {len(alumnos_creados) * len(tipos_inteligencias)} inteligencias creadas")
        print(f"   - {len(alumnos_creados) * len(competencias_creadas)} calificaciones creadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_test_data() 