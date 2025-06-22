# Scripts de Utilidad

Esta carpeta contiene scripts de utilidad para el mantenimiento y administración del sistema de gestión educativa.

## Scripts Disponibles

### 📊 `create_test_excel.py`
**Propósito**: Crear archivos Excel de prueba con la estructura correcta para probar la funcionalidad de upload.

**Uso**:
```bash
cd backend/scripts
python create_test_excel.py
```

**Resultado**: Crea un archivo `datos_prueba.xlsx` en el directorio `backend/` con:
- Hoja "notas" con competencias y calificaciones
- Hoja "inteligencia" con puntajes de inteligencias múltiples
- Hoja "ci" con coeficientes intelectuales

### 🔧 `fix_calificaciones.py`
**Propósito**: Corregir calificaciones que están almacenadas como números en lugar de letras (A, B, C, D).

**Uso**:
```bash
cd backend/scripts
python fix_calificaciones.py
```

**Funcionalidades**:
- Verifica el estado actual de las calificaciones
- Convierte números (1, 2, 3, 4) a letras (D, C, B, A)
- Muestra estadísticas del proceso
- Verifica el resultado final

**Mapeo de conversión**:
- 1 → D
- 2 → C
- 3 → B
- 4 → A

### 📋 `verificar_competencias.py`
**Propósito**: Verificar el estado de las competencias en la base de datos y generar mapeos actualizados.

**Uso**:
```bash
cd backend/scripts
python verificar_competencias.py
```

**Funcionalidades**:
- Analiza todas las competencias en la base de datos
- Identifica competencias sin descripción
- Genera estadísticas por curso
- Produce mapeo actualizado para `excel_processor.py`

### 🔄 `actualizar_competencias_desc.py`
**Propósito**: Actualizar automáticamente las descripciones de competencias en la base de datos.

**Uso**:
```bash
cd backend/scripts
python actualizar_competencias_desc.py
```

**Funcionalidades**:
- Actualiza descripciones vacías o faltantes
- Limpia códigos de competencia con espacios extra
- Genera descripciones genéricas para códigos no mapeados
- Produce mapeo completo para `excel_processor.py`
- Muestra estadísticas del proceso de actualización

### 4. `verificar_inteligencias.py`
**Propósito**: Verificar y mostrar información sobre las inteligencias en la base de datos.

**Uso**:
```bash
# Verificar todas las inteligencias
python scripts/verificar_inteligencias.py

# Buscar inteligencias de un alumno específico
python scripts/verificar_inteligencias.py --alumno "Nombre del Alumno"
```

**Funcionalidad**:
- Muestra estadísticas generales de las inteligencias
- Lista todos los tipos de inteligencia encontrados
- Muestra estadísticas por tipo de inteligencia (promedio, mínimo, máximo)
- Identifica alumnos con más inteligencias registradas
- Verifica la consistencia de datos (alumnos sin inteligencias)
- Permite buscar inteligencias de un alumno específico

## Estructura de Archivos

```
backend/
├── scripts/
│   ├── __init__.py              # Hace de scripts un paquete Python
│   ├── README.md                # Este archivo
│   ├── create_test_excel.py     # Generador de archivos de prueba
│   ├── fix_calificaciones.py    # Corrector de calificaciones
│   ├── verificar_competencias.py # Verificador de competencias
│   └── actualizar_competencias_desc.py # Actualizador de descripciones
├── app/                         # Aplicación principal
├── static/                      # Archivos estáticos del frontend
├── bdalumnas.db                 # Base de datos
└── requirements.txt             # Dependencias
```

## Notas Importantes

1. **Ejecutar desde scripts/**: Todos los scripts deben ejecutarse desde la carpeta `scripts/`
2. **Rutas relativas**: Los scripts usan rutas relativas para acceder a la base de datos y otros archivos
3. **Backup**: Siempre haz un backup de la base de datos antes de ejecutar scripts de corrección
4. **Logging**: Los scripts incluyen logging detallado para debugging

## Agregar Nuevos Scripts

Para agregar un nuevo script de utilidad:

1. Crear el archivo en `backend/scripts/`
2. Usar rutas relativas para acceder a recursos del proyecto
3. Incluir logging apropiado
4. Documentar el propósito y uso en este README
5. Agregar manejo de errores robusto

## Ejemplos de Uso

### Crear archivo de prueba y corregir calificaciones
```bash
cd backend/scripts

# Crear archivo de prueba
python create_test_excel.py

# Corregir calificaciones existentes
python fix_calificaciones.py
```

### Solo verificar estado de calificaciones
```bash
cd backend/scripts
python -c "from fix_calificaciones import verificar_calificaciones; verificar_calificaciones()"
``` 