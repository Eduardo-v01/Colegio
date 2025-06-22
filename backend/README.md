# Sistema de Gestión Educativa - Backend

## Descripción
Backend para el Sistema de Gestión Educativa con API REST y frontend integrado.

## Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el servidor
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8001
```

### 3. Acceder al frontend
Una vez que el servidor esté ejecutándose, puedes acceder al frontend en:
- **Frontend**: http://127.0.0.1:8001/frontend
- **API Docs**: http://127.0.0.1:8001/docs

## Funcionalidades del Frontend

### 📚 Gestión de Alumnos
- **Crear alumno**: Agregar nuevos alumnos con nombre, apellido, email y edad
- **Ver lista**: Mostrar todos los alumnos registrados
- **Editar**: Modificar información de alumnos existentes
- **Eliminar**: Remover alumnos del sistema

### 📖 Gestión de Cursos
- **Crear curso**: Agregar nuevos cursos
- **Ver lista**: Mostrar todos los cursos registrados
- **Editar**: Modificar información de cursos
- **Eliminar**: Remover cursos del sistema

### 🏆 Gestión de Competencias
- **Crear competencia**: Agregar nuevas competencias con descripción
- **Ver lista**: Mostrar todas las competencias registradas
- **Editar**: Modificar información de competencias
- **Eliminar**: Remover competencias del sistema

### 📊 Subir Archivo Excel
- **Procesar datos**: Subir archivos Excel (.xlsx, .xls) para procesar datos masivos
- **Formato requerido**: El archivo debe contener hojas llamadas "notas", "inteligencia" y "ci"
- **Resultado**: Los datos se procesan y se almacenan en la base de datos

## Estructura de Archivos

```
backend/
├── app/
│   ├── database/
│   │   ├── database.py      # Configuración de base de datos
│   │   ├── models.py        # Modelos SQLAlchemy
│   │   └── crud.py          # Operaciones CRUD
│   ├── routers/
│   │   ├── alumnos.py       # Endpoints para alumnos
│   │   ├── cursos.py        # Endpoints para cursos
│   │   ├── competencias.py  # Endpoints para competencias
│   │   └── upload.py        # Endpoint para subir archivos
│   ├── schemas/
│   │   ├── alumno.py        # Schemas Pydantic para alumnos
│   │   └── competencia.py   # Schemas Pydantic para competencias
│   ├── services/
│   │   └── excel_processor.py # Procesamiento de archivos Excel
│   └── main.py              # Aplicación principal
├── scripts/
│   ├── __init__.py          # Hace de scripts un paquete Python
│   ├── README.md            # Documentación de scripts
│   ├── create_test_excel.py # Generador de archivos Excel de prueba
│   └── fix_calificaciones.py # Corrector de calificaciones
├── static/
│   ├── index.html           # Frontend principal
│   ├── styles.css           # Estilos CSS
│   └── script.js            # JavaScript del frontend
├── bdalumnas.db             # Base de datos SQLite
└── requirements.txt         # Dependencias Python
```

## Endpoints de la API

### Alumnos
- `GET /api/alumnos/` - Obtener lista de alumnos
- `GET /api/alumnos/{id}` - Obtener alumno específico
- `POST /api/alumnos/` - Crear nuevo alumno
- `PUT /api/alumnos/{id}` - Actualizar alumno
- `DELETE /api/alumnos/{id}` - Eliminar alumno

### Cursos
- `GET /api/cursos/` - Obtener lista de cursos
- `GET /api/cursos/{id}` - Obtener curso específico
- `POST /api/cursos/` - Crear nuevo curso
- `PUT /api/cursos/{id}` - Actualizar curso
- `DELETE /api/cursos/{id}` - Eliminar curso

### Competencias
- `GET /api/competencias/` - Obtener lista de competencias
- `GET /api/competencias/{id}` - Obtener competencia específica
- `POST /api/competencias/` - Crear nueva competencia
- `PUT /api/competencias/{id}` - Actualizar competencia
- `DELETE /api/competencias/{id}` - Eliminar competencia

### Upload
- `POST /api/upload` - Subir y procesar archivo Excel

## Características del Frontend

- **Interfaz moderna**: Diseño responsive con gradientes y animaciones
- **Navegación por pestañas**: Organización clara de funcionalidades
- **Formularios intuitivos**: Validación y feedback visual
- **Operaciones CRUD**: Crear, leer, actualizar y eliminar registros
- **Mensajes de estado**: Feedback claro sobre operaciones
- **Modal de edición**: Interfaz para modificar registros existentes
- **Carga de archivos**: Subida y procesamiento de archivos Excel

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con Flexbox y Grid
- **JavaScript ES6+**: Funcionalidad interactiva
- **Font Awesome**: Iconos
- **Fetch API**: Comunicación con el backend

## Solución de Problemas

### Error 500 al subir archivo Excel

Si recibes un error 500 al subir un archivo Excel, verifica lo siguiente:

1. **Estructura del archivo Excel**:
   - Debe tener exactamente 3 hojas: `notas`, `inteligencia`, `ci`
   - Los nombres de las hojas deben estar en minúsculas
   - La hoja `notas` debe tener una columna llamada `nom` (nombre del alumno)

2. **Formato de datos**:
   - Las competencias deben seguir el formato: `1_materia_c1`, `1_materia_c2`, etc.
   - Las calificaciones deben ser: A, B, C, o D
   - Los valores de CI deben ser números enteros
   - Los valores de inteligencia deben ser números decimales

3. **Crear archivo de prueba**:
   ```bash
   cd backend
   python create_test_excel.py
   ```
   Esto creará un archivo `datos_prueba.xlsx` que puedes usar para probar el sistema.

### Error 500 al listar competencias/alumnos

Si recibes un error 500 al listar competencias o alumnos, el problema puede ser:
- Incompatibilidad entre los schemas Pydantic y los modelos de la base de datos
- Campos faltantes en la respuesta JSON

**Solución**: Los routers han sido actualizados para manejar manualmente la conversión de datos y evitar estos errores.

### Verificar logs del servidor

Para ver información detallada sobre errores, revisa la consola donde ejecutaste el servidor. Los logs mostrarán:
- Información sobre el procesamiento de archivos
- Errores específicos con detalles
- Número de registros procesados

## Notas Importantes

1. **CORS**: Configurado para permitir todas las origenes (solo para desarrollo)
2. **Base de datos**: SQLite para simplicidad, puede migrarse a PostgreSQL/MySQL
3. **Archivos estáticos**: Servidos desde el directorio `/static`
4. **Validación**: Implementada tanto en frontend como backend
5. **Error handling**: Manejo de errores en todas las operaciones
6. **Logging**: Sistema de logs para debugging

## Próximos Pasos

- [ ] Implementar autenticación y autorización
- [ ] Agregar más validaciones de datos
- [ ] Implementar paginación para listas grandes
- [ ] Agregar filtros y búsqueda
- [ ] Implementar exportación de datos
- [ ] Agregar gráficos y estadísticas
- [ ] Optimizar rendimiento de la base de datos 