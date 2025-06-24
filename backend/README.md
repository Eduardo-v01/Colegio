# Sistema de Gestión Educativa - Backend

## Descripción
Backend para el Sistema de Gestión Educativa con API REST y frontend integrado.

## Instalación y Configuración

### 1. Instalar dependencias
```bash
cd backend
pip install -r requirements.txt
```

### 2. Ejecutar el servidor
```bash
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

### 🧠 Sistema de Clustering Inteligente
El sistema implementa **análisis de clustering** para agrupar automáticamente a los alumnos según sus características académicas y cognitivas.

#### **¿Qué es el Clustering?**
El clustering es una técnica de **Machine Learning** que agrupa automáticamente a los alumnos en grupos similares basándose en sus características comunes, como:
- **Coeficiente Intelectual (CI)**
- **Inteligencias Múltiples** (puntajes en diferentes tipos de inteligencia)
- **Calificaciones académicas** (promedios y rendimiento por competencias)

#### **Algoritmos Utilizados**

##### **1. K-Means Clustering**
- **Propósito**: Agrupa alumnos en un número fijo de clusters (por defecto 3)
- **Funcionamiento**: 
  - Identifica 3 grupos principales: **Alto**, **Medio** y **Bajo rendimiento**
  - Cada alumno se asigna al cluster más cercano según sus características
  - Los clusters se optimizan iterativamente para minimizar la distancia entre miembros

##### **2. DBSCAN Clustering**
- **Propósito**: Identifica clusters basados en **densidad** de datos
- **Funcionamiento**:
  - Detecta grupos naturales sin especificar el número de clusters
  - Identifica posibles **outliers** (alumnos con características únicas)
  - Agrupa alumnos que están "cerca" entre sí en el espacio de características

#### **Proceso de Clustering por Alumno**

Para cada alumno, el sistema:

1. **Recopila datos**:
   ```
   - CI (Coeficiente Intelectual)
   - Inteligencias múltiples (8 tipos diferentes)
   - Calificaciones por competencias (A, B, C, D)
   - Promedio general de calificaciones
   ```

2. **Prepara características**:
   ```
   - CI normalizado
   - Promedio de inteligencias múltiples
   - Máximo puntaje de inteligencia
   - Desviación estándar de inteligencias
   - Promedio de calificaciones (convertidas a números)
   - Mejor calificación obtenida
   - Cantidad de competencias evaluadas
   ```

3. **Aplica algoritmos**:
   - **K-Means**: Asigna cluster 0, 1, o 2
   - **DBSCAN**: Asigna cluster basado en densidad

4. **Almacena resultados**:
   - Guarda `Cluster_KMeans` y `Cluster_DBSCAN` en la base de datos
   - Genera análisis y recomendaciones automáticas

#### **Interpretación de Resultados**

##### **K-Means (3 clusters típicos)**:
- **Cluster 0**: Alumnos con rendimiento **promedio-bajo**
- **Cluster 1**: Alumnos con rendimiento **alto**
- **Cluster 2**: Alumnos con rendimiento **medio**

##### **DBSCAN (clusters por densidad)**:
- **Cluster 0**: Grupo principal de alumnos similares
- **Otros clusters**: Grupos más pequeños con características únicas

#### **Recomendaciones Automáticas**

El sistema genera recomendaciones basadas en los clusters:

- **Alumnos con alto CI**: "Alumnos con alto potencial intelectual"
- **Alumnos con bajo rendimiento**: "Alumnos que requieren apoyo adicional"
- **Fortalezas en inteligencias**: "Fortalezas en inteligencias múltiples"
- **Buen rendimiento académico**: "Buen rendimiento académico"

#### **Cómo Usar el Clustering**

1. **Acceder a la pestaña "Clustering"** en el frontend
2. **Hacer clic en "Procesar Clustering"** para ejecutar el análisis
3. **Ver resultados**:
   - Estadísticas de cada cluster
   - Distribución de alumnos
   - Análisis detallado
   - Recomendaciones pedagógicas

4. **Consultar alumnos individuales** para ver sus clusters asignados

#### **Ventajas del Sistema**

- **Personalización**: Cada alumno recibe un análisis individualizado
- **Objetividad**: Los algoritmos eliminan sesgos subjetivos
- **Escalabilidad**: Funciona con cualquier número de alumnos
- **Actualización**: Se puede reprocesar cuando se agregan nuevos datos
- **Insights pedagógicos**: Proporciona recomendaciones específicas por grupo

#### **Casos de Uso**

- **Agrupación para clases**: Formar grupos homogéneos o heterogéneos
- **Identificación de necesidades**: Detectar alumnos que requieren apoyo especial
- **Planificación pedagógica**: Adaptar estrategias según el perfil del grupo
- **Seguimiento de progreso**: Monitorear cambios en los clusters a lo largo del tiempo

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
│   │   ├── clustering.py    # Endpoints para clustering
│   │   ├── inteligencias.py # Endpoints para inteligencias
│   │   ├── ci.py           # Endpoints para coeficiente intelectual
│   │   ├── ai_assistant.py # Endpoints para asistente IA
│   │   ├── profesores.py   # Endpoints para profesores
│   │   ├── personal_chat.py # Endpoints para chat personal
│   │   └── upload.py        # Endpoint para subir archivos
│   ├── schemas/
│   │   ├── alumno.py        # Schemas Pydantic para alumnos
│   │   ├── competencia.py   # Schemas Pydantic para competencias
│   │   ├── profesor.py      # Schemas Pydantic para profesores
│   │   └── conversacion.py  # Schemas Pydantic para conversaciones
│   ├── services/
│   │   ├── excel_processor.py # Procesamiento de archivos Excel
│   │   ├── clustering_service.py # Servicio de clustering ML
│   │   ├── ai_assistant.py  # Servicio de asistente IA
│   │   ├── personal_ai_chat.py # Servicio de chat personal
│   │   └── auth.py          # Servicio de autenticación
│   └── main.py              # Aplicación principal
├── scripts/
│   ├── __init__.py                    # Hace de scripts un paquete Python
│   ├── README.md                      # Documentación de scripts
│   ├── create_test_data.py            # Generador de datos de prueba
│   ├── create_test_profesores.py      # Generador de profesores de prueba
│   ├── diagnose_database.py           # Diagnóstico de la base de datos
│   ├── fix_calificaciones.py          # Corrector de calificaciones (números a letras)
│   ├── migrate_conversations.py       # Migración de conversaciones
│   ├── test_auth_and_chat.py          # Pruebas de autenticación y chat
│   ├── test_chat_functionality.py     # Pruebas de funcionalidad de chat
│   ├── test_clustering.py             # Script de prueba para clustering
│   ├── test_personal_chat.py          # Pruebas de chat personal
│   ├── test_profesores.py             # Pruebas completas de endpoints de profesores
│   ├── test_public_chat.py            # Pruebas de chat público
│   ├── test_welcome_endpoint.py       # Pruebas del endpoint de bienvenida
│   ├── test_yae_miko_personality.py   # Pruebas de personalidad de Yae Miko
│   ├── verificar_competencias.py      # Verificación de competencias
│   ├── verificar_conversaciones.py    # Verificación de conversaciones
│   ├── verificar_hojas_excel.py       # Verificación de estructura de Excel
│   └── verificar_inteligencias.py     # Verificación de inteligencias
├── static/
│   ├── index.html           # Frontend principal
│   ├── styles.css           # Estilos CSS
│   └── script.js            # JavaScript del frontend
├── bdalumnas.db             # Base de datos SQLite
└── requirements.txt         # Dependencias Python
```

## Endpoints de la API

### 🔐 Autenticación y Profesores
- `POST /profesores/register` - Registrar nuevo profesor
- `POST /profesores/login` - Iniciar sesión de profesor
- `GET /profesores/me` - Obtener información del profesor actual (requiere autenticación)
- `GET /profesores/` - Obtener lista de todos los profesores
- `GET /profesores/{profesor_id}` - Obtener profesor específico
- `PUT /profesores/{profesor_id}` - Actualizar información de profesor
- `DELETE /profesores/{profesor_id}` - Eliminar profesor

#### Gestión de Cursos por Profesor
- `GET /profesores/{profesor_id}/cursos` - Obtener cursos asignados a un profesor
- `POST /profesores/{profesor_id}/cursos/{curso_id}` - Asignar curso a profesor
- `DELETE /profesores/{profesor_id}/cursos/{curso_id}` - Desasignar curso de profesor
- `GET /profesores/cursos/disponibles` - Obtener todos los cursos disponibles
- `GET /profesores/{profesor_id}/estadisticas` - Obtener estadísticas del profesor

### 👥 Alumnos
- `GET /alumnos/` - Obtener lista de alumnos
- `GET /alumnos/{id}` - Obtener alumno específico
- `POST /alumnos/` - Crear nuevo alumno
- `PUT /alumnos/{id}` - Actualizar alumno
- `DELETE /alumnos/{id}` - Eliminar alumno

### 📚 Cursos
- `GET /cursos/` - Obtener lista de cursos
- `GET /cursos/{id}` - Obtener curso específico
- `POST /cursos/` - Crear nuevo curso
- `PUT /cursos/{id}` - Actualizar curso
- `DELETE /cursos/{id}` - Eliminar curso

### 🏆 Competencias
- `GET /competencias/` - Obtener lista de competencias
- `GET /competencias/{id}` - Obtener competencia específica
- `POST /competencias/` - Crear nueva competencia
- `PUT /competencias/{id}` - Actualizar competencia
- `DELETE /competencias/{id}` - Eliminar competencia

### 🧠 Inteligencias Múltiples
- `GET /inteligencias/` - Obtener lista de inteligencias
- `POST /inteligencias/` - Crear nueva inteligencia
- `GET /inteligencias/alumno/{alumno_id}` - Obtener inteligencias de un alumno
- `PUT /inteligencias/{id}` - Actualizar inteligencia
- `DELETE /inteligencias/{id}` - Eliminar inteligencia

### 🧮 Coeficiente Intelectual (CI)
- `GET /ci/` - Obtener lista de CIs
- `POST /ci/` - Crear/actualizar CI
- `GET /ci/alumno/{alumno_id}` - Obtener CI de un alumno
- `GET /ci/estadisticas` - Obtener estadísticas de CI
- `PUT /ci/{id}` - Actualizar CI
- `DELETE /ci/{id}` - Eliminar CI

### 🤖 Asistente IA (Yae Miko)
- `POST /ai-assistant/recommendations` - Generar recomendaciones para un alumno
- `POST /ai-assistant/chat` - Chat público con Yae Miko
- `POST /personal-chat/` - Chat personal con historial (requiere autenticación)
- `GET /personal-chat/history/{alumno_id}` - Obtener historial de chat personal (requiere autenticación)
- `GET /personal-chat/recommendations/{alumno_id}` - Obtener recomendaciones sin historial

### 📊 Clustering Inteligente
- `POST /clustering/process` - Procesar clustering de todos los alumnos
- `GET /clustering/statistics` - Obtener estadísticas de clusters
- `GET /clustering/alumnos` - Obtener alumnos con información de clusters
- `GET /clustering/alumnos/{id}` - Obtener clusters de un alumno específico
- `GET /clustering/analysis` - Obtener análisis completo de clustering

### 📁 Upload y Procesamiento
- `POST /upload` - Subir y procesar archivo Excel
- `POST /upload/update` - Subir archivo Excel en modo actualización (evita duplicados)

### 📈 Estadísticas y Reportes
- `GET /estadisticas/generales` - Obtener estadísticas generales del sistema
- `GET /estadisticas/alumnos` - Obtener estadísticas de alumnos
- `GET /estadisticas/cursos` - Obtener estadísticas de cursos
- `GET /estadisticas/competencias` - Obtener estadísticas de competencias

### 🔍 Búsqueda y Filtros
- `GET /alumnos/search?q={query}` - Buscar alumnos por nombre
- `GET /cursos/search?q={query}` - Buscar cursos por nombre
- `GET /competencias/search?q={query}` - Buscar competencias por código o descripción
- `GET /profesores/search?q={query}` - Buscar profesores por nombre o DNI

### 📋 Endpoints de Utilidad
- `GET /` - Información de bienvenida y estado del sistema
- `GET /health` - Verificar estado de salud del sistema
- `GET /docs` - Documentación interactiva de la API (Swagger UI)
- `GET /redoc` - Documentación alternativa de la API (ReDoc)

## Endpoints Pendientes de Implementar

### 🔄 Gestión de Calificaciones
- `GET /calificaciones/` - Obtener todas las calificaciones
- `GET /calificaciones/alumno/{alumno_id}` - Obtener calificaciones de un alumno
- `GET /calificaciones/competencia/{competencia_id}` - Obtener calificaciones por competencia
- `POST /calificaciones/` - Crear nueva calificación
- `PUT /calificaciones/{id}` - Actualizar calificación
- `DELETE /calificaciones/{id}` - Eliminar calificación
- `GET /calificaciones/promedio/alumno/{alumno_id}` - Obtener promedio de calificaciones de un alumno

### 📚 Gestión de Materias/Cursos
- `GET /materias/` - Obtener lista de materias
- `POST /materias/` - Crear nueva materia
- `PUT /materias/{id}` - Actualizar materia
- `DELETE /materias/{id}` - Eliminar materia
- `GET /materias/{id}/competencias` - Obtener competencias de una materia
- `POST /materias/{id}/competencias` - Asignar competencia a materia

### 👨‍🏫 Gestión de Asignaciones
- `GET /asignaciones/` - Obtener todas las asignaciones profesor-curso
- `GET /asignaciones/profesor/{profesor_id}` - Obtener asignaciones de un profesor
- `GET /asignaciones/curso/{curso_id}` - Obtener profesores asignados a un curso
- `POST /asignaciones/multiple` - Asignar múltiples cursos a un profesor
- `DELETE /asignaciones/multiple` - Desasignar múltiples cursos de un profesor

### 📊 Reportes Avanzados
- `GET /reportes/rendimiento/general` - Reporte de rendimiento general
- `GET /reportes/rendimiento/curso/{curso_id}` - Reporte de rendimiento por curso
- `GET /reportes/rendimiento/profesor/{profesor_id}` - Reporte de rendimiento por profesor
- `GET /reportes/comparativo` - Reporte comparativo entre cursos/profesores
- `GET /reportes/evolucion/alumno/{alumno_id}` - Reporte de evolución de un alumno

### 🔐 Gestión de Usuarios y Permisos
- `GET /usuarios/` - Obtener lista de usuarios
- `POST /usuarios/` - Crear nuevo usuario
- `PUT /usuarios/{id}` - Actualizar usuario
- `DELETE /usuarios/{id}` - Eliminar usuario
- `GET /roles/` - Obtener roles disponibles
- `POST /roles/` - Crear nuevo rol
- `PUT /usuarios/{id}/roles` - Asignar roles a usuario

### 📧 Notificaciones
- `GET /notificaciones/` - Obtener notificaciones del usuario
- `POST /notificaciones/` - Crear nueva notificación
- `PUT /notificaciones/{id}/read` - Marcar notificación como leída
- `DELETE /notificaciones/{id}` - Eliminar notificación

### 🔄 Backup y Restauración
- `POST /backup/create` - Crear backup de la base de datos
- `GET /backup/list` - Listar backups disponibles
- `POST /backup/restore/{backup_id}` - Restaurar desde backup
- `DELETE /backup/{backup_id}` - Eliminar backup

### 📤 Exportación de Datos
- `GET /export/alumnos` - Exportar datos de alumnos (CSV/Excel)
- `GET /export/calificaciones` - Exportar calificaciones (CSV/Excel)
- `GET /export/reportes/{tipo}` - Exportar reportes específicos
- `POST /export/custom` - Exportación personalizada de datos

### 🔧 Configuración del Sistema
- `GET /config/` - Obtener configuración del sistema
- `PUT /config/` - Actualizar configuración del sistema
- `GET /config/clustering` - Obtener configuración de clustering
- `PUT /config/clustering` - Actualizar configuración de clustering

## Características del Frontend

### 🎨 Interfaz Moderna y Responsiva
- **Diseño responsive**: Adaptable a dispositivos móviles, tablets y desktop
- **Gradientes y animaciones**: Interfaz visualmente atractiva con transiciones suaves
- **Navegación por pestañas**: Organización clara y intuitiva de funcionalidades
- **Iconos Font Awesome**: Iconografía consistente y profesional

### 👥 Gestión Completa de Alumnos
- **CRUD completo**: Crear, leer, actualizar y eliminar alumnos
- **Formularios intuitivos**: Validación en tiempo real y feedback visual
- **Modal de edición**: Interfaz para modificar registros existentes
- **Mensajes de estado**: Feedback claro sobre operaciones exitosas y errores
- **Búsqueda y filtros**: Encontrar alumnos rápidamente

### 📚 Gestión de Cursos
- **CRUD completo**: Gestión integral de cursos
- **Validación de datos**: Asegura integridad de la información
- **Interfaz intuitiva**: Fácil navegación y operaciones

### 🏆 Gestión de Competencias
- **CRUD completo**: Administración de competencias educativas
- **Descripciones detalladas**: Información completa de cada competencia
- **Validación robusta**: Prevención de errores en la entrada de datos

### 🧠 Sistema de Inteligencias Múltiples
- **Visualización de inteligencias**: Gráficos y estadísticas de los 8 tipos de inteligencia
- **Análisis por alumno**: Perfiles individuales de inteligencias múltiples
- **Comparativas**: Análisis comparativo entre alumnos

### 🧮 Coeficiente Intelectual (CI)
- **Gestión de CI**: Registro y seguimiento del coeficiente intelectual
- **Estadísticas**: Análisis estadístico de los valores de CI
- **Visualización**: Gráficos y reportes de distribución de CI

### 🤖 Asistente IA - Yae Miko
- **Personalidad única**: Asistente con personalidad cálida y motivadora
- **Chat público**: Conversaciones generales con el asistente
- **Chat personal**: Conversaciones privadas con historial por alumno
- **Recomendaciones automáticas**: Sugerencias pedagógicas personalizadas
- **Contexto inteligente**: Memoria de conversaciones anteriores
- **Emojis y expresiones**: Comunicación amigable y cercana

### 📊 Sistema de Clustering Inteligente
- **Procesamiento automático**: Análisis de clustering con algoritmos ML
- **Algoritmos K-Means y DBSCAN**: Agrupación inteligente de alumnos
- **Estadísticas detalladas**: Análisis completo de cada cluster
- **Visualización de resultados**: Gráficos y tablas de clusters
- **Recomendaciones por cluster**: Sugerencias específicas por grupo
- **Análisis individual**: Clusters asignados por alumno

### 📁 Carga y Procesamiento de Archivos
- **Subida de Excel**: Procesamiento de archivos .xlsx y .xls
- **Validación de formato**: Verificación de estructura de archivos
- **Modo actualización**: Evita duplicados al subir el mismo archivo
- **Feedback detallado**: Información sobre registros creados y actualizados
- **Manejo de errores**: Mensajes claros sobre problemas en el archivo

### 👨‍🏫 Gestión Completa de Profesores
- **Registro y autenticación**: Sistema de usuarios para profesores
- **CRUD de profesores**: Gestión completa de información de profesores
- **Asignación de cursos**: Relación N:M entre profesores y cursos
- **Estadísticas de profesor**: Métricas de rendimiento y asignaciones
- **Gestión de sesiones**: Login/logout con tokens JWT
- **Perfil de usuario**: Información personal del profesor autenticado

### 📈 Estadísticas y Reportes
- **Dashboard general**: Vista general del sistema
- **Estadísticas por entidad**: Métricas de alumnos, cursos, competencias
- **Gráficos interactivos**: Visualización de datos con Chart.js
- **Reportes personalizados**: Análisis específicos por criterios

### 🔍 Búsqueda y Filtros Avanzados
- **Búsqueda global**: Encontrar información rápidamente
- **Filtros por categoría**: Refinamiento de resultados
- **Ordenamiento**: Organización por diferentes criterios
- **Paginación**: Navegación eficiente en grandes conjuntos de datos

### 🔐 Sistema de Autenticación
- **Login seguro**: Autenticación con JWT tokens
- **Gestión de sesiones**: Control de acceso a funcionalidades
- **Protección de rutas**: Endpoints protegidos por autenticación
- **Logout seguro**: Cierre de sesión con invalidación de tokens

### 📱 Funcionalidades Avanzadas
- **Modales dinámicos**: Ventanas emergentes para edición
- **Validación en tiempo real**: Feedback inmediato en formularios
- **Carga asíncrona**: Operaciones sin recargar la página
- **Manejo de errores**: Interfaz robusta ante fallos
- **Responsive design**: Adaptación a diferentes tamaños de pantalla
- **Accesibilidad**: Navegación por teclado y lectores de pantalla

### 🎯 Características Específicas por Pestaña

#### Pestaña Alumnos
- Lista completa de alumnos con información detallada
- Formulario de creación con validación
- Modal de edición con datos precargados
- Botones de acción (editar, eliminar) por alumno

#### Pestaña Cursos
- Gestión de cursos con CRUD completo
- Validación de nombres únicos
- Interfaz limpia y organizada

#### Pestaña Competencias
- Administración de competencias educativas
- Códigos y descripciones detalladas
- Validación de datos obligatorios

#### Pestaña Inteligencias
- Visualización de inteligencias múltiples
- Gráficos de distribución
- Análisis por alumno

#### Pestaña CI
- Gestión de coeficiente intelectual
- Estadísticas y análisis
- Visualización de datos

#### Pestaña Profesores
- Sistema completo de autenticación
- Gestión de profesores y asignaciones
- Estadísticas y reportes de profesor
- Interfaz de login/registro

#### Pestaña Clustering
- Procesamiento de clustering ML
- Visualización de resultados
- Análisis detallado de clusters
- Recomendaciones automáticas

#### Pestaña AI Assistant
- Chat interactivo con Yae Miko
- Selección de alumnos para análisis
- Generación de recomendaciones
- Historial de conversaciones

#### Pestaña Upload
- Subida de archivos Excel
- Validación de formato
- Feedback de procesamiento
- Modo actualización para evitar duplicados

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI
- **scikit-learn**: Machine Learning para clustering (K-Means, DBSCAN)
- **NumPy**: Computación numérica para análisis de datos
- **Pandas**: Manipulación y análisis de datos
- **OpenAI**: API para asistente IA (Yae Miko)
- **Python-Jose**: Autenticación JWT
- **Passlib**: Hashing de contraseñas
- **OpenPyXL**: Procesamiento de archivos Excel

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con Flexbox y Grid
- **JavaScript ES6+**: Funcionalidad interactiva
- **Font Awesome**: Iconos
- **Fetch API**: Comunicación con el backend
- **Chart.js**: Visualización de datos y gráficos (para clustering)

## Scripts y Herramientas

### 🛠️ Scripts de Mantenimiento

#### **Diagnóstico y Verificación**
- `diagnose_database.py` - Diagnóstico completo de la base de datos
- `verificar_competencias.py` - Verificar integridad de competencias
- `verificar_conversaciones.py` - Verificar conversaciones de IA
- `verificar_hojas_excel.py` - Verificar estructura de archivos Excel
- `verificar_inteligencias.py` - Verificar datos de inteligencias múltiples

#### **Corrección de Datos**
- `fix_calificaciones.py` - Convertir calificaciones numéricas a letras (A, B, C, D)
- `migrate_conversations.py` - Migrar conversaciones existentes

#### **Generación de Datos de Prueba**
- `create_test_data.py` - Generar datos de prueba completos
- `create_test_profesores.py` - Generar profesores de prueba

### 🧪 Scripts de Pruebas

#### **Pruebas de Funcionalidad**
- `test_clustering.py` - Pruebas completas del sistema de clustering
- `test_profesores.py` - Pruebas de endpoints de profesores
- `test_auth_and_chat.py` - Pruebas de autenticación y chat
- `test_chat_functionality.py` - Pruebas de funcionalidad de chat
- `test_personal_chat.py` - Pruebas de chat personal
- `test_public_chat.py` - Pruebas de chat público
- `test_welcome_endpoint.py` - Pruebas del endpoint de bienvenida
- `test_yae_miko_personality.py` - Pruebas de personalidad de Yae Miko

### 📋 Cómo Usar los Scripts

#### **Ejecutar Scripts de Prueba**
```bash
# Pruebas de clustering
python scripts/test_clustering.py

# Pruebas de profesores
python scripts/test_profesores.py

# Pruebas de chat
python scripts/test_chat_functionality.py
```

#### **Ejecutar Scripts de Mantenimiento**
```bash
# Diagnóstico de base de datos
python scripts/diagnose_database.py

# Corregir calificaciones
python scripts/fix_calificaciones.py

# Verificar competencias
python scripts/verificar_competencias.py
```

#### **Generar Datos de Prueba**
```bash
# Generar datos completos
python scripts/create_test_data.py

# Generar profesores de prueba
python scripts/create_test_profesores.py
```

### 🔍 Verificación del Sistema

#### **Verificar Estado de la Base de Datos**
```bash
python scripts/diagnose_database.py
```
Este script verifica:
- Existencia de todas las tablas
- Integridad de las relaciones
- Datos de ejemplo
- Configuración de la base de datos

#### **Verificar Datos de Competencias**
```bash
python scripts/verificar_competencias.py
```
Este script verifica:
- Competencias con descripciones
- Códigos de competencias válidos
- Relaciones con cursos

#### **Verificar Conversaciones de IA**
```bash
python scripts/verificar_conversaciones.py
```
Este script verifica:
- Tabla de conversaciones
- Mensajes de IA
- Relaciones con alumnos y profesores

### 🛠️ Herramientas de Corrección

#### **Corregir Calificaciones**
Si las calificaciones están almacenadas como números en lugar de letras:
```bash
python scripts/fix_calificaciones.py
```
Este script:
- Convierte 1 → A, 2 → B, 3 → C, 4 → D
- Actualiza la base de datos
- Genera reporte de cambios

#### **Migrar Conversaciones**
Para migrar conversaciones existentes:
```bash
python scripts/migrate_conversations.py
```

### 📊 Generación de Datos de Prueba

#### **Datos Completos**
```bash
python scripts/create_test_data.py
```
Genera:
- Alumnos de ejemplo
- Cursos y competencias
- Inteligencias múltiples
- Coeficientes intelectuales
- Calificaciones

#### **Profesores de Prueba**
```bash
python scripts/create_test_profesores.py
```
Genera:
- Profesores con credenciales válidas
- Asignaciones de cursos
- Datos de prueba para autenticación

### 🧪 Ejecutar Todas las Pruebas

Para verificar que todo el sistema funciona correctamente:

```bash
# 1. Verificar base de datos
python scripts/diagnose_database.py

# 2. Probar clustering
python scripts/test_clustering.py

# 3. Probar profesores
python scripts/test_profesores.py

# 4. Probar chat
python scripts/test_chat_functionality.py

# 5. Probar personalidad de Yae Miko
python scripts/test_yae_miko_personality.py
```

### 📝 Interpretación de Resultados

#### **Scripts de Verificación**
- ✅ **PASÓ**: Todo está correcto
- ❌ **FALLÓ**: Hay problemas que necesitan atención
- ⚠️ **ADVERTENCIA**: Problemas menores que no afectan funcionamiento

#### **Scripts de Prueba**
- ✅ **PASÓ**: La funcionalidad funciona correctamente
- ❌ **FALLÓ**: Error en la funcionalidad
- 🔧 **ERROR**: Problema de configuración o conexión

### 🔧 Solución de Problemas con Scripts

#### **Error de Conexión**
Si un script falla por conexión:
1. Verificar que el servidor esté corriendo
2. Verificar la URL del servidor en el script
3. Verificar que no haya problemas de red

#### **Error de Base de Datos**
Si hay errores de base de datos:
1. Ejecutar `diagnose_database.py` para identificar problemas
2. Verificar que la base de datos existe y es accesible
3. Verificar permisos de escritura

#### **Error de Dependencias**
Si faltan dependencias:
1. Instalar requirements: `pip install -r requirements.txt`
2. Verificar que todas las librerías estén instaladas
3. Verificar versiones de Python y dependencias

## Notas Importantes

1. **CORS**: Configurado para permitir todas las origenes (solo para desarrollo)
2. **Base de datos**: SQLite para simplicidad, puede migrarse a PostgreSQL/MySQL
3. **Archivos estáticos**: Servidos desde el directorio `/static`
4. **Validación**: Implementada tanto en frontend como backend
5. **Error handling**: Manejo de errores en todas las operaciones
6. **Logging**: Sistema de logs para debugging

## Próximos Pasos

### ✅ Funcionalidades Implementadas
- [x] Sistema completo de autenticación y autorización
- [x] CRUD completo para todas las entidades (alumnos, cursos, competencias, profesores)
- [x] Sistema de clustering inteligente con K-Means y DBSCAN
- [x] Asistente IA con personalidad de Yae Miko
- [x] Chat personal y público con historial
- [x] Carga y procesamiento de archivos Excel
- [x] Gestión de inteligencias múltiples y CI
- [x] Asignación de cursos a profesores
- [x] Frontend completo con interfaz moderna
- [x] Scripts de prueba y mantenimiento
- [x] Sistema de validación robusto
- [x] Manejo de errores completo

### 🚧 Funcionalidades en Desarrollo
- [ ] Sistema de calificaciones individuales
- [ ] Reportes avanzados y exportación
- [ ] Dashboard con métricas en tiempo real
- [ ] Sistema de notificaciones
- [ ] Backup y restauración automática

### 🔮 Funcionalidades Futuras
- [ ] Sistema de roles y permisos avanzado
- [ ] API para aplicaciones móviles
- [ ] Integración con sistemas externos
- [ ] Análisis predictivo con ML
- [ ] Sistema de evaluación automática
- [ ] Gamificación y badges
- [ ] Integración con calendarios académicos
- [ ] Sistema de mensajería interna
- [ ] Auditoría y logs detallados
- [ ] Optimización de rendimiento avanzada

### 🛠️ Mejoras Técnicas Pendientes
- [ ] Migración a PostgreSQL/MySQL para producción
- [ ] Implementación de caché Redis
- [ ] Sistema de colas para tareas pesadas
- [ ] Tests unitarios y de integración
- [ ] CI/CD pipeline
- [ ] Dockerización completa
- [ ] Monitoreo y alertas
- [ ] Documentación de API con OpenAPI 3.0
- [ ] Internacionalización (i18n)
- [ ] Optimización de consultas de base de datos

### 📊 Mejoras de UX/UI
- [ ] Temas personalizables
- [ ] Modo oscuro
- [ ] Gráficos interactivos avanzados
- [ ] Filtros y búsqueda avanzada
- [ ] Paginación infinita
- [ ] Drag & drop para archivos
- [ ] Notificaciones push
- [ ] Accesibilidad mejorada
- [ ] Responsive design optimizado
- [ ] Animaciones y transiciones

### 🔐 Seguridad y Compliance
- [ ] Encriptación de datos sensibles
- [ ] Auditoría de seguridad
- [ ] Cumplimiento GDPR/LOPD
- [ ] Autenticación de dos factores
- [ ] Rate limiting
- [ ] Validación de entrada avanzada
- [ ] Sanitización de datos
- [ ] Logs de seguridad
- [ ] Backup encriptado
- [ ] Política de contraseñas

### 📈 Escalabilidad
- [ ] Arquitectura microservicios
- [ ] Load balancing
- [ ] Base de datos distribuida
- [ ] CDN para archivos estáticos
- [ ] Compresión de respuestas
- [ ] Optimización de imágenes
- [ ] Lazy loading
- [ ] Service workers
- [ ] Progressive Web App (PWA)
- [ ] API versioning

## Solución de Problemas

### 🚨 Errores Comunes y Soluciones

#### **Error 500 al subir archivo Excel**

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
   python scripts/create_test_data.py
   ```

#### **Error 500 al listar competencias/alumnos**

Si recibes un error 500 al listar competencias o alumnos:
- Incompatibilidad entre los schemas Pydantic y los modelos de la base de datos
- Campos faltantes en la respuesta JSON

**Solución**: Los routers han sido actualizados para manejar manualmente la conversión de datos.

#### **Error 401 Unauthorized en chat personal**

Si recibes error 401 al acceder al chat personal:
- El endpoint requiere autenticación de profesor
- Verificar que el token JWT sea válido
- Usar el endpoint `/personal-chat/recommendations/{alumno_id}` para acceso sin autenticación

#### **Error en clustering**

Si el clustering falla:
- Verificar que hay alumnos con datos de CI, inteligencias y calificaciones
- Revisar que las dependencias de ML estén instaladas: `scikit-learn`, `numpy`, `pandas`
- Verificar logs del servidor para errores específicos

#### **Error de conexión al servidor**

Si no puedes conectar al servidor:
```bash
# Verificar que el puerto esté disponible
netstat -an | findstr :8000

# Usar puerto alternativo
uvicorn app.main:app --reload --port 8001
```

### 🔍 Verificación de Logs

Para ver información detallada sobre errores, revisa la consola donde ejecutaste el servidor. Los logs mostrarán:
- Información sobre el procesamiento de archivos
- Errores específicos con detalles
- Número de registros procesados
- Errores de autenticación y autorización

### 🛠️ Diagnóstico del Sistema

#### **Verificar Estado Completo**
```bash
# Diagnóstico de base de datos
python scripts/diagnose_database.py

# Verificar competencias
python scripts/verificar_competencias.py

# Verificar conversaciones
python scripts/verificar_conversaciones.py
```

#### **Probar Funcionalidades Críticas**
```bash
# Probar clustering
python scripts/test_clustering.py

# Probar profesores
python scripts/test_profesores.py

# Probar chat
python scripts/test_chat_functionality.py
```

### 🔧 Correcciones Automáticas

#### **Corregir Calificaciones**
Si las calificaciones están como números en lugar de letras:
```bash
python scripts/fix_calificaciones.py
```

#### **Migrar Datos**
Para migrar conversaciones existentes:
```bash
python scripts/migrate_conversations.py
```

### 📊 Verificación de Datos

#### **Verificar Base de Datos**
- Ejecutar `diagnose_database.py` para verificar integridad
- Verificar que todas las tablas existan
- Verificar relaciones entre tablas

#### **Verificar Archivos Excel**
- Usar `verificar_hojas_excel.py` para validar estructura
- Verificar nombres de hojas y columnas
- Verificar formato de datos

### 🚀 Optimización de Rendimiento

#### **Problemas de Rendimiento**
- Verificar que la base de datos no esté corrupta
- Limpiar datos innecesarios
- Optimizar consultas complejas

#### **Problemas de Memoria**
- Verificar que no haya fugas de memoria
- Optimizar procesamiento de archivos grandes
- Usar paginación en listas grandes

### 📱 Problemas del Frontend

#### **Errores de JavaScript**
- Verificar la consola del navegador (F12)
- Verificar que todos los archivos se carguen correctamente
- Verificar compatibilidad del navegador

#### **Problemas de CORS**
- Verificar configuración de CORS en el backend
- Verificar que las URLs sean correctas
- Verificar headers de las peticiones

### 🔐 Problemas de Autenticación

#### **Error de Login**
- Verificar credenciales del profesor
- Verificar que el profesor esté registrado
- Verificar formato de DNI y contraseña

#### **Token Expirado**
- Los tokens JWT expiran después de 30 minutos
- Hacer logout y login nuevamente
- Verificar configuración de expiración

### 📈 Problemas de Clustering

#### **Clustering No Funciona**
- Verificar que hay suficientes datos (mínimo 3 alumnos)
- Verificar que los datos sean numéricos válidos
- Verificar que las dependencias de ML estén instaladas

#### **Resultados Inesperados**
- Verificar calidad de los datos de entrada
- Ajustar parámetros de clustering si es necesario
- Verificar que los algoritmos se ejecuten correctamente

### 🤖 Problemas del Asistente IA

#### **Yae Miko No Responde**
- Verificar conexión a internet
- Verificar configuración de OpenAI
- Verificar que el prompt esté bien formateado

#### **Respuestas Inconsistentes**
- Verificar personalidad configurada
- Verificar contexto del alumno
- Verificar historial de conversaciones

### 📋 Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] El servidor está corriendo
- [ ] La base de datos es accesible
- [ ] Todas las dependencias están instaladas
- [ ] Los archivos de configuración son correctos
- [ ] Los logs no muestran errores críticos
- [ ] El frontend se carga correctamente
- [ ] Las credenciales son válidas (si aplica)
- [ ] Los datos de entrada son correctos 