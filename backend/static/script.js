// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8001/api';

// Variables globales
let currentEditId = null;
let currentEditType = null;
let currentStudentProfile = null;

// Variables globales para autenticación
let currentToken = localStorage.getItem('authToken');
let currentUser = localStorage.getItem('currentUser');

// Variables globales para chat personal
let currentChatStudentId = null;
let currentChatStudentName = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeChat(); // Inicializar chat
    loadAlumnos(); // Cargar datos iniciales
    loadAlumnosForSelect(); // Cargar alumnos para el select de inteligencias
    loadTiposInteligencia(); // Cargar tipos de inteligencia para el select
    loadStudentsForAI(); // Cargar alumnos para la IA
    loadStudentsForPersonalChat(); // Cargar alumnos para el chat personal
    
    // Event listeners para profesores
    const profesorRegisterForm = document.getElementById('profesorRegisterForm');
    const profesorLoginForm = document.getElementById('profesorLoginForm');
    
    if (profesorRegisterForm) {
        profesorRegisterForm.addEventListener('submit', handleProfesorRegister);
    }
    
    if (profesorLoginForm) {
        profesorLoginForm.addEventListener('submit', handleProfesorLogin);
    }
    
    // Inicializar estado de autenticación
    initializeAuth();
});

// Event Listeners
function initializeEventListeners() {
    // Formularios
    document.getElementById('alumnoForm').addEventListener('submit', handleAlumnoSubmit);
    document.getElementById('cursoForm').addEventListener('submit', handleCursoSubmit);
    document.getElementById('competenciaForm').addEventListener('submit', handleCompetenciaSubmit);
    document.getElementById('inteligenciaForm').addEventListener('submit', handleInteligenciaSubmit);
    document.getElementById('ciForm').addEventListener('submit', handleCISubmit);
    document.getElementById('uploadForm').addEventListener('submit', handleUploadSubmit);
    
    // Chat personal
    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', handlePersonalChatSubmit);
    }
    
    // Modal
    document.querySelector('.close').addEventListener('click', closeModal);
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('editModal')) {
            closeModal();
        }
    });
}

// Funciones de navegación
function showTab(tabName) {
    // Ocultar todas las pestañas
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Desactivar todos los botones
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    // Mostrar la pestaña seleccionada
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    // Cargar datos según la pestaña
    switch(tabName) {
        case 'alumnos':
            loadAlumnos();
            break;
        case 'cursos':
            loadCursos();
            break;
        case 'competencias':
            loadCompetencias();
            break;
        case 'inteligencias':
            loadInteligencias();
            break;
        case 'ci':
            loadCIs();
            break;
        case 'profesores':
            loadProfesores();
            loadCursosDisponibles();
            break;
        case 'ai-assistant':
            loadStudentsForAI();
            loadStudentsForPersonalChat();
            break;
    }
}

// Funciones para Alumnos
async function loadAlumnos() {
    const container = document.getElementById('alumnosList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando alumnos...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/alumnos/`);
        if (!response.ok) throw new Error('Error al cargar alumnos');
        
        const alumnos = await response.json();
        displayAlumnos(alumnos);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayAlumnos(alumnos) {
    const container = document.getElementById('alumnosList');
    
    if (alumnos.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay alumnos registrados</div>';
        return;
    }
    
    container.innerHTML = alumnos.map(alumno => `
        <div class="item-card">
            <div class="item-header">
                <div class="item-title">${alumno.Nombre || 'Sin nombre'}</div>
                <div class="item-actions">
                    <button class="btn btn-success" onclick="editItem('alumno', ${alumno.Alumno_ID})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn btn-danger" onclick="deleteItem('alumno', ${alumno.Alumno_ID})">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </div>
            </div>
            <div class="item-details">
                <p><strong>ID:</strong> ${alumno.Alumno_ID}</p>
                <p><strong>Promedio:</strong> ${alumno.Promedio_Calificaciones || 'N/A'}</p>
                <p><strong>Competencias:</strong> ${alumno.Cantidad_Competencias || 0}</p>
                <p><strong>CI:</strong> ${alumno.CI || 'N/A'}</p>
                <p><strong>Recomendaciones:</strong> ${alumno.Recomendaciones_Basicas || 'Sin recomendaciones'}</p>
            </div>
        </div>
    `).join('');
}

async function handleAlumnoSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        nombre: formData.get('nombre'),
        apellido: formData.get('apellido'),
        email: formData.get('email'),
        edad: parseInt(formData.get('edad')) || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/alumnos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Error al crear alumno');
        
        showStatus('Alumno creado exitosamente', 'success');
        event.target.reset();
        loadAlumnos();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Funciones para Cursos
async function loadCursos() {
    const container = document.getElementById('cursosList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando cursos...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/cursos/`);
        if (!response.ok) throw new Error('Error al cargar cursos');
        
        const cursos = await response.json();
        displayCursos(cursos);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayCursos(cursos) {
    const container = document.getElementById('cursosList');
    
    if (cursos.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay cursos registrados</div>';
        return;
    }
    
    container.innerHTML = cursos.map(curso => `
        <div class="item-card">
            <div class="item-header">
                <div class="item-title">${curso.Nombre}</div>
                <div class="item-actions">
                    <button class="btn btn-success" onclick="editItem('curso', ${curso.Curso_ID})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn btn-danger" onclick="deleteItem('curso', ${curso.Curso_ID})">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </div>
            </div>
            <div class="item-details">
                <p><strong>ID:</strong> ${curso.Curso_ID}</p>
            </div>
        </div>
    `).join('');
}

async function handleCursoSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        Nombre: formData.get('nombre')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/cursos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Error al crear curso');
        
        showStatus('Curso creado exitosamente', 'success');
        event.target.reset();
        loadCursos();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Funciones para Competencias
async function loadCompetencias() {
    const container = document.getElementById('competenciasList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando competencias...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/competencias/`);
        if (!response.ok) throw new Error('Error al cargar competencias');
        
        const competencias = await response.json();
        displayCompetencias(competencias);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayCompetencias(competencias) {
    const container = document.getElementById('competenciasList');
    
    if (competencias.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay competencias registradas</div>';
        return;
    }
    
    container.innerHTML = competencias.map(comp => `
        <div class="item-card">
            <div class="item-header">
                <div class="item-title">${comp.Codigo_Competencia}</div>
                <div class="item-actions">
                    <button class="btn btn-success" onclick="editItem('competencia', ${comp.CompetenciaPlantilla_ID})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn btn-danger" onclick="deleteItem('competencia', ${comp.CompetenciaPlantilla_ID})">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </div>
            </div>
            <div class="item-details">
                <p><strong>ID:</strong> ${comp.CompetenciaPlantilla_ID}</p>
                <p><strong>Descripción:</strong> ${comp.Descripcion || 'Sin descripción'}</p>
                <p><strong>Curso ID:</strong> ${comp.Curso_ID}</p>
            </div>
        </div>
    `).join('');
}

async function handleCompetenciaSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        nombre: formData.get('nombre'),
        descripcion: formData.get('descripcion')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/competencias/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Error al crear competencia');
        
        showStatus('Competencia creada exitosamente', 'success');
        event.target.reset();
        loadCompetencias();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Funciones para Upload
async function handleUploadSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const file = formData.get('file');
    const actualizarExistentes = formData.get('actualizar_existentes') === 'on';
    
    if (!file) {
        showStatus('Por favor selecciona un archivo', 'error');
        return;
    }
    
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Procesando archivo...</div>';
    
    try {
        const uploadFormData = new FormData();
        uploadFormData.append('file', file);
        uploadFormData.append('actualizar_existentes', actualizarExistentes);
        
        const response = await fetch(`${API_BASE_URL}/upload/`, {
            method: 'POST',
            body: uploadFormData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al subir archivo');
        }
        
        const result = await response.json();
        
        // Crear mensaje detallado con información de inteligencias
        let statusMessage = `
            <div class="upload-result">
                <h4><i class="fas fa-check-circle"></i> ${result.mensaje}</h4>
                <div class="result-summary">
                    <p><strong>Alumnos:</strong> ${result.alumnos_procesados} procesados (${result.alumnos_creados} creados, ${result.alumnos_actualizados} actualizados)</p>
                    <p><strong>Competencias:</strong> ${result.competencias_procesadas} procesadas</p>
                    <p><strong>Cursos:</strong> ${result.cursos_procesados} procesados</p>
                </div>
        `;
        
        // Agregar información detallada de inteligencias
        if (result.inteligencias) {
            const intel = result.inteligencias;
            statusMessage += `
                <div class="inteligencias-summary">
                    <h5><i class="fas fa-brain"></i> Procesamiento de Inteligencias</h5>
                    <div class="inteligencias-details">
                        <p><strong>Estado:</strong> 
                            ${intel.hoja_encontrada ? 
                                (intel.columnas_requeridas ? 
                                    (intel.registros_validos > 0 ? 
                                        `<span class="status-success">✓ Exitoso</span>` : 
                                        `<span class="status-warning">⚠ Sin datos válidos</span>`) : 
                                    `<span class="status-error">✗ Columnas faltantes</span>`) : 
                                `<span class="status-error">✗ Hoja no encontrada</span>`}
                        </p>
                        ${intel.hoja_detectada ? `<p><strong>Hoja detectada:</strong> '${intel.hoja_detectada}'</p>` : ''}
                        ${intel.hojas_disponibles.length > 0 ? `<p><strong>Hojas disponibles:</strong> ${intel.hojas_disponibles.join(', ')}</p>` : ''}
                        ${intel.hoja_encontrada ? `
                            <p><strong>Tipos encontrados:</strong> ${intel.tipos_encontrados.length > 0 ? intel.tipos_encontrados.join(', ') : 'Ninguno'}</p>
                            <p><strong>Registros válidos:</strong> ${intel.registros_validos}</p>
                            <p><strong>Alumnos con inteligencias:</strong> ${intel.alumnos_con_inteligencias}</p>
                            <p><strong>Inteligencias procesadas:</strong> ${intel.procesadas}</p>
                        ` : ''}
                        ${intel.error_mensaje ? `<p><strong>Error:</strong> <span class="error-text">${intel.error_mensaje}</span></p>` : ''}
                    </div>
                </div>
            `;
        }
        
        // Agregar información detallada de CI
        if (result.ci) {
            const ci = result.ci;
            statusMessage += `
                <div class="inteligencias-summary" style="background: #fff3cd; border-left-color: #ffc107;">
                    <h5 style="color: #856404;"><i class="fas fa-chart-line"></i> Procesamiento de CI</h5>
                    <div class="inteligencias-details">
                        <p><strong>Estado:</strong> 
                            ${ci.hoja_encontrada ? 
                                (ci.columnas_requeridas ? 
                                    (ci.registros_validos > 0 ? 
                                        `<span class="status-success">✓ Exitoso</span>` : 
                                        `<span class="status-warning">⚠ Sin datos válidos</span>`) : 
                                    `<span class="status-error">✗ Columnas faltantes</span>`) : 
                                `<span class="status-error">✗ Hoja no encontrada</span>`}
                        </p>
                        ${ci.hoja_detectada ? `<p><strong>Hoja detectada:</strong> '${ci.hoja_detectada}'</p>` : ''}
                        ${ci.hoja_encontrada ? `
                            <p><strong>Registros válidos:</strong> ${ci.registros_validos}</p>
                            <p><strong>Alumnos con CI:</strong> ${ci.alumnos_con_ci}</p>
                        ` : ''}
                        ${ci.error_mensaje ? `<p><strong>Error:</strong> <span class="error-text">${ci.error_mensaje}</span></p>` : ''}
                    </div>
                </div>
            `;
        }
        
        statusMessage += '</div>';
        statusDiv.innerHTML = statusMessage;
        
        // Recargar datos si es necesario
        setTimeout(() => {
            loadAlumnos();
            loadInteligencias();
            loadCIs();
        }, 2000);
        
    } catch (error) {
        statusDiv.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

// Funciones de edición y eliminación
async function editItem(type, id) {
    currentEditType = type;
    currentEditId = id;
    
    try {
        let response;
        switch(type) {
            case 'alumno':
                response = await fetch(`${API_BASE_URL}/alumnos/${id}`);
                break;
            case 'curso':
                response = await fetch(`${API_BASE_URL}/cursos/${id}`);
                break;
            case 'competencia':
                response = await fetch(`${API_BASE_URL}/competencias/${id}`);
                break;
            case 'inteligencia':
                response = await fetch(`${API_BASE_URL}/inteligencias/${id}`);
                break;
            case 'ci':
                response = await fetch(`${API_BASE_URL}/ci/alumno/${id}`);
                break;
        }
        
        if (!response.ok) throw new Error('Error al cargar datos');
        
        const item = await response.json();
        showEditModal(type, item);
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function showEditModal(type, item) {
    const modal = document.getElementById('editModal');
    const title = document.getElementById('modalTitle');
    const fields = document.getElementById('modalFields');
    
    title.textContent = `Editar ${type.charAt(0).toUpperCase() + type.slice(1)}`;
    
    let fieldsHTML = '';
    switch(type) {
        case 'alumno':
            const nombres = (item.Nombre || '').split(' ');
            const nombre = nombres[0] || '';
            const apellido = nombres.slice(1).join(' ') || '';
            fieldsHTML = `
                <div class="form-group">
                    <label for="editNombre">Nombre:</label>
                    <input type="text" id="editNombre" name="nombre" value="${nombre}" required>
                </div>
                <div class="form-group">
                    <label for="editApellido">Apellido:</label>
                    <input type="text" id="editApellido" name="apellido" value="${apellido}" required>
                </div>
            `;
            break;
        case 'curso':
            fieldsHTML = `
                <div class="form-group">
                    <label for="editCursoNombre">Nombre:</label>
                    <input type="text" id="editCursoNombre" name="nombre" value="${item.Nombre}" required>
                </div>
            `;
            break;
        case 'competencia':
            fieldsHTML = `
                <div class="form-group">
                    <label for="editCompNombre">Nombre:</label>
                    <input type="text" id="editCompNombre" name="nombre" value="${item.Codigo_Competencia}" required>
                </div>
                <div class="form-group">
                    <label for="editCompDescripcion">Descripción:</label>
                    <textarea id="editCompDescripcion" name="descripcion" rows="3">${item.Descripcion || ''}</textarea>
                </div>
            `;
            break;
        case 'inteligencia':
            fieldsHTML = `
                <div class="form-group">
                    <label for="editIntelTipo">Tipo de Inteligencia:</label>
                    <input type="text" id="editIntelTipo" name="tipo_inteligencia" value="${item.Tipo_Inteligencia}" required>
                </div>
                <div class="form-group">
                    <label for="editIntelPuntaje">Puntaje:</label>
                    <input type="number" id="editIntelPuntaje" name="puntaje" step="0.1" min="0" max="100" value="${item.Puntaje}" required>
                </div>
            `;
            break;
        case 'ci':
            fieldsHTML = `
                <div class="form-group">
                    <label for="editCIValor">Valor de CI:</label>
                    <input type="number" id="editCIValor" name="valor_ci" min="0" max="200" value="${item.Valor_CI}" required>
                </div>
                <div class="form-group">
                    <label for="editCIFecha">Fecha del Test:</label>
                    <input type="date" id="editCIFecha" name="fecha_test" value="${item.Fecha_Test || ''}">
                </div>
                <div class="form-group">
                    <label for="editCITipo">Tipo de Test:</label>
                    <input type="text" id="editCITipo" name="tipo_test" value="${item.Tipo_Test || ''}" placeholder="Ej: WISC, Stanford-Binet, etc.">
                </div>
                <div class="form-group">
                    <label for="editCIObservaciones">Observaciones:</label>
                    <textarea id="editCIObservaciones" name="observaciones" rows="3" placeholder="Observaciones adicionales...">${item.Observaciones || ''}</textarea>
                </div>
            `;
            break;
    }
    
    fields.innerHTML = fieldsHTML;
    modal.style.display = 'block';
    
    // Configurar el formulario de edición
    const editForm = document.getElementById('editForm');
    editForm.onsubmit = handleEditSubmit;
}

async function handleEditSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    let data = {};
    
    switch(currentEditType) {
        case 'alumno':
            data = {
                nombre: formData.get('nombre'),
                apellido: formData.get('apellido')
            };
            break;
        case 'curso':
            data = {
                Nombre: formData.get('nombre')
            };
            break;
        case 'competencia':
            data = {
                nombre: formData.get('nombre'),
                descripcion: formData.get('descripcion')
            };
            break;
        case 'inteligencia':
            data = {
                Tipo_Inteligencia: formData.get('tipo_inteligencia'),
                Puntaje: parseFloat(formData.get('puntaje'))
            };
            break;
        case 'ci':
            data = {
                Alumno_ID: parseInt(formData.get('alumno_id')),
                Valor_CI: parseInt(formData.get('valor_ci')),
                Fecha_Test: formData.get('fecha_test') || null,
                Tipo_Test: formData.get('tipo_test') || null,
                Observaciones: formData.get('observaciones') || null
            };
            break;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/${currentEditType}s/${currentEditId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Error al actualizar');
        
        showStatus('Elemento actualizado exitosamente', 'success');
        closeModal();
        
        // Recargar datos
        switch(currentEditType) {
            case 'alumno':
                loadAlumnos();
                break;
            case 'curso':
                loadCursos();
                break;
            case 'competencia':
                loadCompetencias();
                break;
            case 'inteligencia':
                loadInteligencias();
                break;
            case 'ci':
                loadCIs();
                break;
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function deleteItem(type, id) {
    if (!confirm('¿Estás seguro de que quieres eliminar este elemento?')) {
        return;
    }
    
    try {
        let response;
        switch(type) {
            case 'alumno':
                response = await fetch(`${API_BASE_URL}/alumnos/${id}`, { method: 'DELETE' });
                break;
            case 'curso':
                response = await fetch(`${API_BASE_URL}/cursos/${id}`, { method: 'DELETE' });
                break;
            case 'competencia':
                response = await fetch(`${API_BASE_URL}/competencias/${id}`, { method: 'DELETE' });
                break;
            case 'inteligencia':
                response = await fetch(`${API_BASE_URL}/inteligencias/${id}`, { method: 'DELETE' });
                break;
            case 'ci':
                response = await fetch(`${API_BASE_URL}/ci/${id}`, { method: 'DELETE' });
                break;
        }
        
        if (!response.ok) throw new Error('Error al eliminar');
        
        showStatus('Elemento eliminado exitosamente', 'success');
        
        // Recargar datos según el tipo
        switch(type) {
            case 'alumno':
                loadAlumnos();
                break;
            case 'curso':
                loadCursos();
                break;
            case 'competencia':
                loadCompetencias();
                break;
            case 'inteligencia':
                loadInteligencias();
                break;
            case 'ci':
                loadCIs();
                break;
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Funciones auxiliares
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
    currentEditId = null;
    currentEditType = null;
}

function showStatus(message, type) {
    // Crear un elemento de estado temporal
    const statusDiv = document.createElement('div');
    statusDiv.className = `status-message ${type}`;
    statusDiv.textContent = message;
    
    // Insertar al principio del contenedor
    const container = document.querySelector('.container');
    container.insertBefore(statusDiv, container.firstChild);
    
    // Remover después de 5 segundos
    setTimeout(() => {
        statusDiv.remove();
    }, 5000);
}

// Funciones para Inteligencias
async function loadInteligencias() {
    const container = document.getElementById('inteligenciasList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando inteligencias...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/inteligencias/`);
        if (!response.ok) throw new Error('Error al cargar inteligencias');
        
        const inteligencias = await response.json();
        displayInteligencias(inteligencias);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayInteligencias(inteligencias) {
    const container = document.getElementById('inteligenciasList');
    
    if (inteligencias.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay inteligencias registradas</div>';
        return;
    }
    
    // Agrupar inteligencias por alumno
    const inteligenciasPorAlumno = {};
    inteligencias.forEach(intel => {
        if (!inteligenciasPorAlumno[intel.Alumno_ID]) {
            inteligenciasPorAlumno[intel.Alumno_ID] = [];
        }
        inteligenciasPorAlumno[intel.Alumno_ID].push(intel);
    });
    
    container.innerHTML = Object.entries(inteligenciasPorAlumno).map(([alumnoId, intels]) => {
        const puntajes = intels.map(i => i.Puntaje);
        const maxPuntaje = Math.max(...puntajes);
        const promedio = puntajes.reduce((a, b) => a + b, 0) / puntajes.length;
        
        return `
            <div class="item-card">
                <div class="item-header">
                    <div class="item-title">Alumno ID: ${alumnoId}</div>
                    <div class="item-actions">
                        <button class="btn btn-info" onclick="verEstadisticasAlumno(${alumnoId})">
                            <i class="fas fa-chart-bar"></i> Estadísticas
                        </button>
                        <button class="btn btn-danger" onclick="deleteInteligenciasAlumno(${alumnoId})">
                            <i class="fas fa-trash"></i> Eliminar Todas
                        </button>
                    </div>
                </div>
                <div class="item-details">
                    <p><strong>Total Inteligencias:</strong> ${intels.length}</p>
                    <p><strong>Puntaje Máximo:</strong> ${maxPuntaje}</p>
                    <p><strong>Promedio:</strong> ${promedio.toFixed(2)}</p>
                    <div class="inteligencias-grid">
                        ${intels.map(intel => `
                            <div class="inteligencia-item">
                                <span class="inteligencia-tipo">${intel.Tipo_Inteligencia}</span>
                                <span class="inteligencia-puntaje">${intel.Puntaje}</span>
                                <div class="inteligencia-actions">
                                    <button class="btn btn-sm btn-success" onclick="editItem('inteligencia', ${intel.Inteligencia_ID})">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="btn btn-sm btn-danger" onclick="deleteItem('inteligencia', ${intel.Inteligencia_ID})">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

async function verEstadisticasAlumno(alumnoId) {
    try {
        const response = await fetch(`${API_BASE_URL}/inteligencias/estadisticas/alumno/${alumnoId}`);
        if (!response.ok) throw new Error('Error al cargar estadísticas');
        
        const stats = await response.json();
        
        if (stats.message) {
            showStatus(stats.message, 'info');
            return;
        }
        
        // Mostrar estadísticas en un modal o en la lista
        const container = document.getElementById('inteligenciasList');
        container.innerHTML = `
            <div class="stats-card">
                <div class="stats-header">
                    <h3>Estadísticas de Inteligencias - ${stats.nombre_alumno}</h3>
                    <button class="btn btn-secondary" onclick="loadInteligencias()">
                        <i class="fas fa-arrow-left"></i> Volver
                    </button>
                </div>
                <div class="stats-content">
                    <div class="stats-summary">
                        <div class="stat-item">
                            <span class="stat-label">Total Inteligencias:</span>
                            <span class="stat-value">${stats.total_inteligencias}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Puntaje Máximo:</span>
                            <span class="stat-value">${stats.puntaje_maximo}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Inteligencia Más Alta:</span>
                            <span class="stat-value">${stats.inteligencia_maxima}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Puntaje Mínimo:</span>
                            <span class="stat-value">${stats.puntaje_minimo}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Promedio:</span>
                            <span class="stat-value">${stats.promedio}</span>
                        </div>
                    </div>
                    <div class="inteligencias-detalle">
                        <h4>Detalle por Tipo de Inteligencia</h4>
                        ${stats.inteligencias.map(intel => `
                            <div class="inteligencia-stat">
                                <span class="inteligencia-nombre">${intel.tipo}</span>
                                <span class="inteligencia-valor">${intel.puntaje}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function deleteInteligenciasAlumno(alumnoId) {
    if (!confirm('¿Estás seguro de que quieres eliminar todas las inteligencias de este alumno?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/inteligencias/alumno/${alumnoId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Error al eliminar inteligencias');
        
        const result = await response.json();
        showStatus(result.message, 'success');
        loadInteligencias();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function loadTiposInteligencia() {
    try {
        const response = await fetch(`${API_BASE_URL}/inteligencias/tipos/lista`);
        if (!response.ok) throw new Error('Error al cargar tipos de inteligencia');
        
        const data = await response.json();
        const select = document.getElementById('intelTipo');
        
        // Limpiar opciones existentes
        select.innerHTML = '<option value="">Seleccionar tipo...</option>';
        
        // Agregar opciones de tipos de inteligencia
        data.tipos_inteligencia.forEach(tipo => {
            const option = document.createElement('option');
            option.value = tipo;
            option.textContent = tipo;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error al cargar tipos de inteligencia:', error);
    }
}

async function handleInteligenciaSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        Alumno_ID: parseInt(formData.get('alumno_id')),
        Tipo_Inteligencia: formData.get('tipo_inteligencia'),
        Puntaje: parseFloat(formData.get('puntaje'))
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/inteligencias/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Error al crear inteligencia');
        
        showStatus('Inteligencia creada exitosamente', 'success');
        event.target.reset();
        loadInteligencias();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function loadAlumnosForSelect() {
    try {
        const response = await fetch(`${API_BASE_URL}/alumnos/`);
        if (!response.ok) throw new Error('Error al cargar alumnos');
        
        const alumnos = await response.json();
        const select = document.getElementById('intelAlumno');
        
        // Limpiar opciones existentes excepto la primera
        select.innerHTML = '<option value="">Seleccionar alumno...</option>';
        
        // Agregar opciones de alumnos
        alumnos.forEach(alumno => {
            const option = document.createElement('option');
            option.value = alumno.Alumno_ID;
            option.textContent = alumno.Nombre;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error al cargar alumnos para select:', error);
    }
}

// Funciones para CI
async function loadCIs() {
    const container = document.getElementById('cisList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando CIs...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/ci/`);
        if (!response.ok) throw new Error('Error al cargar CIs');
        
        const cis = await response.json();
        displayCIs(cis);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayCIs(cis) {
    const container = document.getElementById('cisList');
    
    if (cis.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay CIs registrados</div>';
        return;
    }
    
    container.innerHTML = cis.map(ci => `
        <div class="item-card">
            <div class="item-header">
                <div class="item-title">CI: ${ci.Valor_CI}</div>
                <div class="item-actions">
                    <button class="btn btn-info" onclick="verResumenCI(${ci.Alumno_ID})">
                        <i class="fas fa-chart-line"></i> Resumen
                    </button>
                    <button class="btn btn-success" onclick="editItem('ci', ${ci.Alumno_ID})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn btn-danger" onclick="deleteItem('ci', ${ci.Alumno_ID})">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </div>
            </div>
            <div class="item-details">
                <p><strong>Alumno ID:</strong> ${ci.Alumno_ID}</p>
                <p><strong>Valor CI:</strong> ${ci.Valor_CI}</p>
                <p><strong>Fecha Test:</strong> ${ci.Fecha_Test || 'N/A'}</p>
                <p><strong>Tipo Test:</strong> ${ci.Tipo_Test || 'N/A'}</p>
                <p><strong>Observaciones:</strong> ${ci.Observaciones || 'Sin observaciones'}</p>
            </div>
        </div>
    `).join('');
}

async function handleCISubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        Alumno_ID: parseInt(formData.get('alumno_id')),
        Valor_CI: parseInt(formData.get('valor_ci')),
        Fecha_Test: formData.get('fecha_test') || null,
        Tipo_Test: formData.get('tipo_test') || null,
        Observaciones: formData.get('observaciones') || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/ci/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Error al guardar CI');
        
        showStatus('CI guardado exitosamente', 'success');
        event.target.reset();
        loadCIs();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function loadEstadisticasCI() {
    const container = document.getElementById('cisList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando estadísticas...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/ci/estadisticas/general`);
        if (!response.ok) throw new Error('Error al cargar estadísticas');
        
        const stats = await response.json();
        displayEstadisticasCI(stats);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayEstadisticasCI(stats) {
    const container = document.getElementById('cisList');
    
    if (stats.message) {
        container.innerHTML = `<div class="status-message info">${stats.message}</div>`;
        return;
    }
    
    const categoriasHTML = Object.entries(stats.alumnos_por_rango).map(([categoria, info]) => `
        <div class="stat-item">
            <span class="stat-label">${categoria}:</span>
            <span class="stat-value">${info.count} alumnos</span>
        </div>
    `).join('');
    
    container.innerHTML = `
        <div class="stats-container">
            <h3>Estadísticas Generales de CI</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-title">Total Alumnos</div>
                    <div class="stat-number">${stats.total_alumnos}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">Promedio CI</div>
                    <div class="stat-number">${stats.promedio_ci}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">CI Máximo</div>
                    <div class="stat-number">${stats.ci_maximo}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">CI Mínimo</div>
                    <div class="stat-number">${stats.ci_minimo}</div>
                </div>
            </div>
            <div class="categorias-section">
                <h4>Distribución por Categorías</h4>
                <div class="categorias-grid">
                    ${categoriasHTML}
                </div>
            </div>
        </div>
    `;
}

async function verResumenCI(alumnoId) {
    try {
        const response = await fetch(`${API_BASE_URL}/ci/resumen/alumno/${alumnoId}`);
        if (!response.ok) throw new Error('Error al cargar resumen');
        
        const resumen = await response.json();
        
        if (resumen.message) {
            showStatus(resumen.message, 'info');
            return;
        }
        
        const categoriaColor = getCategoriaColor(resumen.categoria);
        
        const modal = document.getElementById('editModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalFields = document.getElementById('modalFields');
        
        modalTitle.textContent = `Resumen CI - ${resumen.nombre_alumno}`;
        modalFields.innerHTML = `
            <div class="resumen-ci">
                <div class="resumen-item">
                    <label>Valor CI:</label>
                    <span class="ci-valor">${resumen.valor_ci}</span>
                </div>
                <div class="resumen-item">
                    <label>Categoría:</label>
                    <span class="categoria-ci ${categoriaColor}">${resumen.categoria}</span>
                </div>
                <div class="resumen-item">
                    <label>Percentil:</label>
                    <span>${resumen.percentil ? resumen.percentil + '%' : 'N/A'}</span>
                </div>
            </div>
        `;
        
        modal.style.display = 'block';
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function getCategoriaColor(categoria) {
    const colores = {
        'Muy Superior': 'ci-muy-superior',
        'Superior': 'ci-superior',
        'Promedio Alto': 'ci-promedio-alto',
        'Promedio': 'ci-promedio',
        'Promedio Bajo': 'ci-promedio-bajo',
        'Bajo': 'ci-bajo',
        'Muy Bajo': 'ci-muy-bajo'
    };
    return colores[categoria] || 'ci-default';
}

// Funciones para Asistente IA
async function loadStudentsForAI() {
    const select = document.getElementById('aiStudentSelect');
    select.innerHTML = '<option value="">Cargando alumnos...</option>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/ai-assistant/students`);
        if (!response.ok) throw new Error('Error al cargar alumnos');
        
        const data = await response.json();
        
        select.innerHTML = '<option value="">Seleccionar alumno...</option>';
        data.students.forEach(student => {
            const option = document.createElement('option');
            option.value = student.alumno_id;
            option.textContent = `${student.nombre} (${student.cantidad_competencias} competencias)`;
            select.appendChild(option);
        });
        
    } catch (error) {
        select.innerHTML = '<option value="">Error al cargar alumnos</option>';
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function loadStudentProfile() {
    const select = document.getElementById('aiStudentSelect');
    const alumnoId = select.value;
    
    if (!alumnoId) {
        showStatus('Por favor selecciona un alumno', 'warning');
        return;
    }
    
    const profileSection = document.getElementById('studentProfileSection');
    const profileContainer = document.getElementById('studentProfile');
    const recommendationsSection = document.getElementById('aiRecommendationsSection');
    
    profileSection.style.display = 'none';
    recommendationsSection.style.display = 'none';
    
    profileContainer.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Cargando perfil...</div>';
    profileSection.style.display = 'block';
    
    try {
        const response = await fetch(`${API_BASE_URL}/ai-assistant/student/${alumnoId}`);
        if (!response.ok) throw new Error('Error al cargar perfil');
        
        const data = await response.json();
        currentStudentProfile = data.alumno;
        
        displayStudentProfile(data.alumno);
        recommendationsSection.style.display = 'block';
        
        // Inicializar automáticamente el chat personal
        await initializePersonalChatForStudent(alumnoId, data.alumno.nombre);
        
        // 🚀 GENERAR RECOMENDACIONES AUTOMÁTICAMENTE
        showStatus('Generando recomendaciones automáticamente...', 'info');
        await generateAIRecommendations();
        
    } catch (error) {
        profileContainer.innerHTML = `<div class="ai-error">Error: ${error.message}</div>`;
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function displayStudentProfile(alumno) {
    const container = document.getElementById('studentProfile');
    
    // Generar iniciales para el avatar
    const nombres = alumno.nombre.split(' ');
    const iniciales = nombres.map(n => n[0]).join('').toUpperCase();
    
    // Formatear inteligencias
    const inteligenciasHTML = alumno.inteligencias.map(intel => {
        // Nueva escala: el puntaje se multiplica por 10 para que la escala sea sobre 10.
        // Un puntaje de 10 será el 100% de la barra.
        const porcentaje = (intel.puntaje || 0) * 10;
        
        return `
            <div class="inteligencia-bar">
                <div class="inteligencia-label">${intel.tipo}</div>
                <div class="inteligencia-progress">
                    <div class="inteligencia-fill" style="width: ${porcentaje}%"></div>
                    <div class="inteligencia-value">${intel.puntaje}</div>
                </div>
            </div>
        `;
    }).join('');
    
    // Formatear calificaciones por curso
    const calificacionesHTML = Object.entries(alumno.calificaciones_por_curso).map(([curso, calificaciones]) => `
        <div class="profile-section">
            <h5>${curso}</h5>
            <div class="calificaciones-grid">
                ${calificaciones.map(cal => `
                    <div class="calificacion-item calificacion-${cal.calificacion.toLowerCase()}">
                        <div class="calificacion-competencia">${cal.competencia}</div>
                        <div class="calificacion-valor">${cal.calificacion}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
    
    // Estadísticas
    const stats = alumno.estadisticas;
    const estadisticasHTML = `
        <div class="profile-section">
            <h5>Estadísticas Generales</h5>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">Total Calificaciones:</span>
                    <span class="stat-value">${stats.total_calificaciones}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Promedio:</span>
                    <span class="stat-value">${alumno.promedio ? alumno.promedio.toFixed(2) : 'N/A'}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Excelente (A):</span>
                    <span class="stat-value">${stats.calificaciones_a} (${stats.porcentaje_excelente.toFixed(1)}%)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Bueno (B):</span>
                    <span class="stat-value">${stats.calificaciones_b} (${stats.porcentaje_bueno.toFixed(1)}%)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Regular (C):</span>
                    <span class="stat-value">${stats.calificaciones_c} (${stats.porcentaje_regular.toFixed(1)}%)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Deficiente (D):</span>
                    <span class="stat-value">${stats.calificaciones_d} (${stats.porcentaje_deficiente.toFixed(1)}%)</span>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = `
        <div class="profile-header">
            <div class="profile-avatar">${iniciales}</div>
            <div class="profile-info">
                <h4>${alumno.nombre}</h4>
                <p>ID: ${alumno.alumno_id}</p>
                ${alumno.ci ? `<p>CI: ${alumno.ci.valor} (${alumno.ci.categoria})</p>` : '<p>CI: No disponible</p>'}
            </div>
        </div>
        
        <div class="profile-sections">
            <div class="profile-section">
                <h5>Inteligencias Múltiples</h5>
                <div class="inteligencias-chart">
                    ${inteligenciasHTML}
                </div>
                ${alumno.inteligencias_predominantes.length > 0 ? `
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e9ecef;">
                        <strong>Inteligencias predominantes:</strong>
                        <p>${alumno.inteligencias_predominantes.map(intel => `${intel.tipo} (${intel.puntaje})`).join(', ')}</p>
                    </div>
                ` : ''}
            </div>
            
            ${calificacionesHTML}
            
            ${estadisticasHTML}
        </div>
    `;
}

async function generateAIRecommendations() {
    if (!currentStudentProfile) {
        showStatus('Primero debes cargar el perfil de un alumno', 'warning');
        return;
    }
    
    const container = document.getElementById('aiRecommendations');
    container.innerHTML = `
        <div class="ai-loading">
            <i class="fas fa-robot fa-spin"></i>
            <p><strong>🌟 Miko Analizando Perfil</strong></p>
            <p>Miko está analizando el perfil de <strong>${currentStudentProfile.nombre}</strong>...</p>
            <p>Generando recomendaciones personalizadas automáticamente ⚡</p>
            <p>Esto puede tomar unos segundos.</p>
        </div>
    `;
    
    try {
        const response = await fetch(`${API_BASE_URL}/ai-assistant/generate-recommendations/${currentStudentProfile.alumno_id}`, {
            method: 'POST'
        });
        
        if (!response.ok) throw new Error('Error al generar recomendaciones');
        
        const data = await response.json();
        
        if (data.success) {
            displayAIRecommendations(data);
            showStatus('✅ Recomendaciones de Miko generadas automáticamente', 'success');
        } else {
            container.innerHTML = `
                <div class="ai-error">
                    <h4><i class="fas fa-exclamation-triangle"></i> Error en Miko</h4>
                    <p>${data.error || 'No se pudieron generar recomendaciones'}</p>
                    <button class="btn btn-primary" onclick="generateAIRecommendations()">
                        <i class="fas fa-redo"></i> Reintentar
                    </button>
                </div>
            `;
            showStatus('❌ Error al generar recomendaciones automáticamente', 'error');
        }
        
    } catch (error) {
        container.innerHTML = `
            <div class="ai-error">
                <h4><i class="fas fa-exclamation-triangle"></i> Error</h4>
                <p>${error.message}</p>
                <button class="btn btn-primary" onclick="generateAIRecommendations()">
                    <i class="fas fa-redo"></i> Reintentar
                </button>
            </div>
        `;
        showStatus(`❌ Error: ${error.message}`, 'error');
    }
}

function displayAIRecommendations(data) {
    const container = document.getElementById('aiRecommendations');
    
    let summaryHTML = '';
    if (data.analysis_summary) {
        const summary = data.analysis_summary;
        summaryHTML = `
            <div class="ai-summary">
                <h5><i class="fas fa-chart-bar"></i> Resumen del Análisis de Miko</h5>
                <div class="ai-summary-grid">
                    ${summary.fortalezas && summary.fortalezas.length > 0 ? `
                        <div class="ai-summary-section">
                            <h6>Fortalezas</h6>
                            <ul class="ai-summary-list">
                                ${summary.fortalezas.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${summary.areas_mejora && summary.areas_mejora.length > 0 ? `
                        <div class="ai-summary-section">
                            <h6>Áreas de Mejora</h6>
                            <ul class="ai-summary-list">
                                ${summary.areas_mejora.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${summary.recomendaciones_principales && summary.recomendaciones_principales.length > 0 ? `
                        <div class="ai-summary-section">
                            <h6>Recomendaciones Principales</h6>
                            <ul class="ai-summary-list">
                                ${summary.recomendaciones_principales.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${summary.actividades_sugeridas && summary.actividades_sugeridas.length > 0 ? `
                        <div class="ai-summary-section">
                            <h6>Actividades Sugeridas</h6>
                            <ul class="ai-summary-list">
                                ${summary.actividades_sugeridas.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    container.innerHTML = `
        <div class="ai-response-header">
            <i class="fas fa-robot"></i>
            <h4>Recomendaciones de Miko para ${data.student_name}</h4>
        </div>
        
        <div class="ai-response-content">
            ${data.recommendations}
        </div>
        
        ${summaryHTML}
    `;
    
    // Mostrar sección de chat después de generar recomendaciones
    document.getElementById('aiChatSection').style.display = 'block';
}

// Funciones para Chat con IA
function initializeChat() {
    // Función simplificada - el chat personal se inicializa cuando se selecciona un alumno
    console.log('Chat personal disponible - selecciona un alumno para comenzar');
}

async function handleChatSubmit(event) {
    event.preventDefault();
    
    if (!currentStudentProfile) {
        showStatus('Primero debes cargar el perfil de un alumno', 'warning');
        return;
    }
    
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Limpiar input
    chatInput.value = '';
    
    // Agregar mensaje del usuario
    addChatMessage(message, 'user');
    
    // Mostrar indicador de escritura
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/ai-assistant/chat/${currentStudentProfile.alumno_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) throw new Error('Error en el chat');
        
        const data = await response.json();
        
        // Ocultar indicador de escritura
        hideTypingIndicator();
        
        if (data.success) {
            addChatMessage(data.response, 'assistant');
        } else {
            addChatError(data.error || 'Error en la respuesta de la IA');
        }
        
    } catch (error) {
        hideTypingIndicator();
        addChatError(`Error: ${error.message}`);
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function addChatMessage(content, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const time = new Date().toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = `chat-avatar ${sender}`;
    avatar.textContent = sender === 'user' ? 'Tú' : 'Miko';
    
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    
    // Formatear contenido (convertir saltos de línea en párrafos)
    const paragraphs = content.split('\n').filter(p => p.trim());
    paragraphs.forEach((paragraph, index) => {
        const p = document.createElement('p');
        p.textContent = paragraph;
        bubble.appendChild(p);
    });
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'chat-time';
    timeDiv.textContent = time;
    bubble.appendChild(timeDiv);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll al final
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addChatError(errorMessage) {
    const chatMessages = document.getElementById('chatMessages');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'chat-error';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${errorMessage}`;
    
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-typing';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <i class="fas fa-robot fa-spin"></i>
        <span>Miko está escribiendo...</span>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

async function loadChatHistory() {
    if (!currentStudentProfile) {
        showStatus('Primero debes cargar el perfil de un alumno', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/ai-assistant/conversation-history/${currentStudentProfile.alumno_id}`);
        if (!response.ok) throw new Error('Error al cargar historial');
        
        const data = await response.json();
        
        if (data.success && data.messages.length > 0) {
            // Limpiar chat actual
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = '';
            
            // Agregar mensajes del historial
            data.messages.forEach(msg => {
                if (msg.role === 'user' || msg.role === 'assistant') {
                    addChatMessage(msg.content, msg.role);
                }
            });
            
            showStatus(`Historial cargado: ${data.messages.length} mensajes`, 'success');
        } else {
            showStatus('No hay historial de conversación', 'info');
        }
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function clearChatHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/ai-assistant/chat/clear`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            document.getElementById('chatMessages').innerHTML = `
                <div class="chat-welcome">
                    <i class="fas fa-robot"></i>
                    <p>¡Hola! Soy Miko, tu asistente pedagógica personal. Puedes hacerme preguntas específicas sobre el alumno seleccionado.</p>
                    <p><strong>Ejemplos de preguntas:</strong></p>
                    <ul>
                        <li>"¿Cómo puedo ayudarle con matemáticas?"</li>
                        <li>"¿Qué actividades le recomiendas para mejorar su concentración?"</li>
                        <li>"¿Cómo puedo motivarlo más en clase?"</li>
                        <li>"¿Qué estrategias funcionan mejor para su tipo de inteligencia?"</li>
                    </ul>
                </div>
            `;
            showStatus('Historial de chat limpiado', 'success');
        } else {
            throw new Error('Error al limpiar el historial');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// === Funciones para la gestión de Profesores ===

// Inicializar estado de autenticación
function initializeAuth() {
    // Cargar token y usuario del localStorage si existen
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('currentUser');
    
    if (savedToken && savedUser) {
        currentToken = savedToken;
        currentUser = savedUser;
        showAuthenticatedState(currentUser);
    } else {
        showNotAuthenticatedState();
    }
}

// Mostrar estado autenticado
function showAuthenticatedState(user) {
    document.getElementById('notAuthenticated').style.display = 'none';
    document.getElementById('authenticated').style.display = 'block';
    document.getElementById('currentUser').textContent = user;
    document.getElementById('tokenInfo').style.display = 'block';
    document.getElementById('tokenValue').textContent = currentToken;
    document.getElementById('tokenType').textContent = 'Bearer';
}

// Mostrar estado no autenticado
function showNotAuthenticatedState() {
    document.getElementById('notAuthenticated').style.display = 'block';
    document.getElementById('authenticated').style.display = 'none';
    document.getElementById('tokenInfo').style.display = 'none';
}

// Registrar nuevo profesor
async function handleProfesorRegister(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const contrasena = formData.get('Contrasena');
    const contrasenaConfirm = formData.get('ContrasenaConfirm');
    
    if (contrasena !== contrasenaConfirm) {
        showStatus('Las contraseñas no coinciden', 'error');
        return;
    }
    
    const data = {
        Nombre: formData.get('Nombre'),
        DNI: formData.get('DNI'),
        Contrasena: contrasena
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al registrar profesor');
        }
        
        const profesor = await response.json();
        showStatus(`Profesor ${profesor.Nombre} registrado exitosamente`, 'success');
        event.target.reset();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Iniciar sesión
async function handleProfesorLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const identifier = formData.get('username');
    const password = formData.get('password');
    
    const data = new URLSearchParams();
    data.append('username', identifier);
    data.append('password', password);
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al iniciar sesión');
        }
        
        const tokenData = await response.json();
        currentToken = tokenData.access_token;
        
        // Obtener información del profesor para mostrar su nombre
        const profesorResponse = await fetch(`${API_BASE_URL}/profesores/me`, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });
        
        if (profesorResponse.ok) {
            const profesor = await profesorResponse.json();
            currentUser = profesor.Nombre;
        } else {
            // Si no se puede obtener el nombre, usar el identificador
            currentUser = identifier;
        }
        
        // Guardar en localStorage
        localStorage.setItem('authToken', currentToken);
        localStorage.setItem('currentUser', currentUser);
        
        showAuthenticatedState(currentUser);
        showStatus('Inicio de sesión exitoso', 'success');
        event.target.reset();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Cerrar sesión
function logout() {
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    showNotAuthenticatedState();
    showStatus('Sesión cerrada exitosamente', 'success');
}

// Copiar token al portapapeles
function copyToken() {
    if (currentToken) {
        navigator.clipboard.writeText(currentToken).then(() => {
            showStatus('Token copiado al portapapeles', 'success');
        }).catch(() => {
            showStatus('Error al copiar el token', 'error');
        });
    }
}

// Inicializar chat personal
async function initializePersonalChat() {
    const studentSelect = document.getElementById('chatStudentSelect');
    const studentId = studentSelect.value;
    
    if (!studentId) {
        showStatus('Por favor selecciona un alumno para el chat personal', 'warning');
        return;
    }
    
    const studentName = studentSelect.options[studentSelect.selectedIndex].text;
    currentChatStudentId = parseInt(studentId);
    currentChatStudentName = studentName;
    
    // Mostrar el contenedor de chat
    document.getElementById('chatContainer').style.display = 'block';
    document.getElementById('chatStudentName').textContent = studentName;
    
    // Limpiar mensajes anteriores
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '<div class="chat-loading"><i class="fas fa-spinner fa-spin"></i> Inicializando chat personal...</div>';
    
    try {
        // Obtener mensaje de bienvenida personalizado
        const response = await fetch(`${API_BASE_URL}/personal-chat/welcome/${studentId}`, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Error al inicializar chat personal');
        }
        
        const data = await response.json();
        
        // Mostrar mensaje de bienvenida
        chatMessages.innerHTML = `
            <div class="chat-message">
                <div class="chat-avatar assistant">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="chat-bubble assistant">
                    <p>${(data.welcome_message || '').replace(/\n/g, '</p><p>')}</p>
                    <div class="chat-time">${new Date().toLocaleTimeString()}</div>
                </div>
            </div>
        `;
        
        showStatus(`Chat personal iniciado para ${studentName}`, 'success');
        
    } catch (error) {
        chatMessages.innerHTML = `
            <div class="chat-error">
                <i class="fas fa-exclamation-triangle"></i>
                Error al inicializar chat personal: ${error.message}
            </div>
        `;
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Función de debug para verificar el estado del token
function debugTokenStatus() {
    console.log('=== DEBUG TOKEN STATUS ===');
    console.log('currentToken:', currentToken ? 'Presente' : 'Ausente');
    console.log('currentUser:', currentUser);
    console.log('localStorage authToken:', localStorage.getItem('authToken') ? 'Presente' : 'Ausente');
    console.log('localStorage currentUser:', localStorage.getItem('currentUser'));
    console.log('========================');
}

// Enviar mensaje personal (público, sin autenticación)
async function handlePersonalChatSubmit(event) {
    event.preventDefault();
    
    if (!currentChatStudentId) {
        showStatus('Primero debes seleccionar un alumno para el chat personal', 'warning');
        return;
    }
    
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Limpiar input
    chatInput.value = '';
    
    // Agregar mensaje del usuario
    addPersonalChatMessage(message, true);
    
    // Mostrar indicador de escritura
    showPersonalChatTyping();
    
    try {
        // Verificar si hay token de autenticación
        if (!currentToken) {
            // Si no hay autenticación, usar el endpoint público
            const response = await fetch(`${API_BASE_URL}/personal-chat/send-message-public`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    alumno_id: currentChatStudentId,
                    mensaje: message
                })
            });
            
            if (!response.ok) {
                throw new Error('Error en el chat público');
            }
            
            const data = await response.json();
            
            // Ocultar indicador de escritura
            hidePersonalChatTyping();
            
            if (data.success) {
                addPersonalChatMessage(data.response, false);
            } else {
                addPersonalChatError(data.error || 'Error en la respuesta de Miko');
            }
        } else {
            // Si hay autenticación, usar el endpoint privado
            const response = await fetch(`${API_BASE_URL}/personal-chat/send-message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${currentToken}`
                },
                body: JSON.stringify({
                    alumno_id: currentChatStudentId,
                    mensaje: message
                })
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    showStatus('⚠️ Sesión expirada. Por favor, inicia sesión nuevamente', 'warning');
                    // Limpiar token expirado
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('currentUser');
                    currentToken = null;
                    currentUser = null;
                    showNotAuthenticatedState();
                    hidePersonalChatTyping();
                    return;
                } else {
                    throw new Error('Error en el chat');
                }
            }
            
            const data = await response.json();
            
            // Ocultar indicador de escritura
            hidePersonalChatTyping();
            
            if (data.success) {
                addPersonalChatMessage(data.response, false);
            } else {
                addPersonalChatError(data.error || 'Error en la respuesta de Miko');
            }
        }
        
    } catch (error) {
        hidePersonalChatTyping();
        addPersonalChatError(`Error: ${error.message}`);
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Añadir mensaje al chat personal
function addPersonalChatMessage(content, isUser) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user' : ''}`;
    
    const avatarClass = isUser ? 'user' : 'assistant';
    const avatarIcon = isUser ? 'fas fa-user' : 'fas fa-robot';
    
    messageDiv.innerHTML = `
        <div class="chat-avatar ${avatarClass}">
            <i class="${avatarIcon}"></i>
        </div>
        <div class="chat-bubble ${avatarClass}">
            <p>${(content || '').replace(/\n/g, '</p><p>')}</p>
            <div class="chat-time">${new Date().toLocaleTimeString()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Mostrar error en el chat personal
function addPersonalChatError(errorMessage) {
    const chatMessages = document.getElementById('chatMessages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'chat-error';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        ${errorMessage}
    `;
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Mostrar indicador de escritura
function showPersonalChatTyping() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'chat-typing';
    typingDiv.innerHTML = `
        <i class="fas fa-robot"></i>
        <span>Miko está escribiendo...</span>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Ocultar indicador de escritura
function hidePersonalChatTyping() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Cargar historial del chat personal
async function loadPersonalChatHistory() {
    if (!currentChatStudentId) {
        showStatus('Primero debes seleccionar un alumno para el chat personal', 'warning');
        return;
    }
    
    // Verificar si hay token de autenticación
    if (!currentToken) {
        showStatus('⚠️ Para ver el historial necesitas iniciar sesión como profesor', 'warning');
        document.getElementById('chatContainer').style.display = 'block';
        document.getElementById('chatStudentName').textContent = currentChatStudentName;
        
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="chat-welcome">
                <i class="fas fa-robot"></i>
                <p>¡Hola! Soy Miko, tu asistente pedagógica personal.</p>
                <p>Para ver el historial de conversaciones, necesitas <strong>iniciar sesión como profesor</strong>.</p>
                <p>Mientras tanto, puedes:</p>
                <ul>
                    <li>✅ Iniciar un <strong>nuevo chat</strong> con recomendaciones frescas</li>
                    <li>✅ Hacer preguntas sobre el desarrollo educativo</li>
                    <li>✅ Obtener consejos personalizados</li>
                </ul>
                <button onclick="startNewChat()" class="btn btn-success">
                    <i class="fas fa-plus"></i> Iniciar Nuevo Chat
                </button>
            </div>
        `;
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/personal-chat/history/${currentChatStudentId}`, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                showStatus('⚠️ Sesión expirada. Por favor, inicia sesión nuevamente', 'warning');
                // Limpiar token expirado
                localStorage.removeItem('authToken');
                localStorage.removeItem('currentUser');
                currentToken = null;
                currentUser = null;
                showNotAuthenticatedState();
            } else {
                throw new Error('Error al cargar historial');
            }
            return;
        }
        
        const data = await response.json();
        
        // Mostrar el contenedor de chat si no está visible
        document.getElementById('chatContainer').style.display = 'block';
        document.getElementById('chatStudentName').textContent = data.alumno_nombre;
        
        // Limpiar mensajes actuales
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = '';
        
        if (data.mensajes.length === 0) {
            chatMessages.innerHTML = `
                <div class="chat-welcome">
                    <i class="fas fa-robot"></i>
                    <p>No hay conversaciones previas con ${data.alumno_nombre}.</p>
                    <p>¡Comienza una nueva conversación personalizada!</p>
                    <button onclick="startNewChat()" class="btn btn-success">
                        <i class="fas fa-plus"></i> Iniciar Nuevo Chat
                    </button>
                </div>
            `;
        } else {
            // Mostrar mensajes del historial
            data.mensajes.forEach(msg => {
                addPersonalChatMessage(msg.mensaje, msg.es_usuario);
            });
        }
        
        showStatus(`Historial cargado: ${data.total_mensajes} mensajes`, 'success');
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Limpiar historial del chat personal
async function clearPersonalChatHistory() {
    if (!currentChatStudentId) {
        showStatus('Primero debes seleccionar un alumno para el chat personal', 'warning');
        return;
    }
    
    // Verificar si hay token de autenticación
    if (!currentToken) {
        showStatus('⚠️ Para limpiar el historial necesitas iniciar sesión como profesor', 'warning');
        return;
    }
    
    if (!confirm(`¿Estás seguro de que quieres limpiar todo el historial de conversación con ${currentChatStudentName}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/personal-chat/clear/${currentChatStudentId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                showStatus('⚠️ Sesión expirada. Por favor, inicia sesión nuevamente', 'warning');
                // Limpiar token expirado
                localStorage.removeItem('authToken');
                localStorage.removeItem('currentUser');
                currentToken = null;
                currentUser = null;
                showNotAuthenticatedState();
            } else {
                throw new Error('Error al limpiar historial');
            }
            return;
        }
        
        // Limpiar chat actual
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="chat-welcome">
                <i class="fas fa-robot"></i>
                <p>Historial de conversación limpiado para ${currentChatStudentName}.</p>
                <p>¡Puedes comenzar una nueva conversación!</p>
                <button onclick="startNewChat()" class="btn btn-success">
                    <i class="fas fa-plus"></i> Iniciar Nuevo Chat
                </button>
            </div>
        `;
        
        showStatus('Historial de conversación limpiado exitosamente', 'success');
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Cargar alumnos para el selector de chat
async function loadStudentsForPersonalChat() {
    const select = document.getElementById('chatStudentSelect');
    
    try {
        const response = await fetch(`${API_BASE_URL}/alumnos/`);
        if (!response.ok) throw new Error('Error al cargar alumnos');
        
        const alumnos = await response.json();
        
        // Limpiar opciones existentes
        select.innerHTML = '<option value="">Seleccionar alumno...</option>';
        
        // Agregar opciones
        alumnos.forEach(alumno => {
            const option = document.createElement('option');
            option.value = alumno.Alumno_ID;
            option.textContent = alumno.Nombre;
            select.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error al cargar alumnos para chat:', error);
    }
}

// Inicializar chat personal para un alumno específico (público)
async function initializePersonalChatForStudent(alumnoId, alumnoNombre) {
    currentChatStudentId = parseInt(alumnoId);
    currentChatStudentName = alumnoNombre;
    
    // Actualizar el selector de chat si existe
    const chatStudentSelect = document.getElementById('chatStudentSelect');
    if (chatStudentSelect) {
        chatStudentSelect.value = alumnoId;
    }
    
    // Mostrar el contenedor de chat
    document.getElementById('chatContainer').style.display = 'block';
    document.getElementById('chatStudentName').textContent = alumnoNombre;
    
    // Limpiar mensajes anteriores
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '<div class="chat-loading"><i class="fas fa-spinner fa-spin"></i> Inicializando chat personal...</div>';
    
    try {
        // Obtener mensaje de bienvenida personalizado (sin autenticación)
        const response = await fetch(`${API_BASE_URL}/personal-chat/welcome/${alumnoId}`);
        
        if (!response.ok) {
            throw new Error('Error al inicializar chat personal');
        }
        
        const data = await response.json();
        
        // Mostrar mensaje de bienvenida
        chatMessages.innerHTML = `
            <div class="chat-message">
                <div class="chat-avatar assistant">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="chat-bubble assistant">
                    <p>${(data.welcome_message || '').replace(/\n/g, '</p><p>')}</p>
                    <div class="chat-time">${new Date().toLocaleTimeString()}</div>
                </div>
            </div>
        `;
        
        showStatus(`Chat personal iniciado para ${alumnoNombre}`, 'success');
        
    } catch (error) {
        chatMessages.innerHTML = `
            <div class="chat-error">
                <i class="fas fa-exclamation-triangle"></i>
                Error al inicializar chat personal: ${error.message}
            </div>
        `;
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Iniciar nuevo chat con recomendaciones frescas
async function startNewChat() {
    if (!currentChatStudentId) {
        showStatus('Primero debes seleccionar un alumno para el chat personal', 'warning');
        return;
    }
    
    // Mostrar el contenedor de chat si no está visible
    document.getElementById('chatContainer').style.display = 'block';
    document.getElementById('chatStudentName').textContent = currentChatStudentName;
    
    // Limpiar mensajes anteriores
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '<div class="chat-loading"><i class="fas fa-spinner fa-spin"></i> Generando nuevas recomendaciones de Miko...</div>';
    
    try {
        // Obtener recomendaciones frescas sin historial
        const response = await fetch(`${API_BASE_URL}/personal-chat/recommendations/${currentChatStudentId}`);
        
        if (!response.ok) {
            throw new Error('Error al obtener recomendaciones');
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Limpiar mensajes y mostrar las nuevas recomendaciones
            chatMessages.innerHTML = '';
            
            // Agregar mensaje de bienvenida
            addPersonalChatMessage(`¡Hola ${data.student_name}! 😊 Soy Miko, tu asistente pedagógica personal.`, false);
            
            // Agregar las recomendaciones como un mensaje de Miko
            addPersonalChatMessage(data.recommendations, false);
            
            showStatus('✅ Nuevo chat iniciado con recomendaciones frescas de Miko', 'success');
        } else {
            throw new Error(data.error || 'Error al generar recomendaciones');
        }
        
    } catch (error) {
        chatMessages.innerHTML = `
            <div class="chat-error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error al iniciar nuevo chat: ${error.message}</p>
                <button onclick="startNewChat()" class="btn btn-primary">
                    <i class="fas fa-redo"></i> Reintentar
                </button>
            </div>
        `;
        showStatus(`❌ Error: ${error.message}`, 'error');
    }
}

// Funciones de Clustering
async function processClustering() {
    const statusDiv = document.getElementById('clusteringStatus');
    const button = document.getElementById('processClusteringBtn');
    
    statusDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Procesando clustering...</div>';
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-cogs fa-spin"></i> Procesando...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/clustering/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al procesar clustering');
        }
        
        const result = await response.json();
        
        statusDiv.innerHTML = `
            <div class="status-message success">
                <i class="fas fa-check-circle"></i>
                <strong>¡Clustering completado!</strong><br>
                ${result.message}<br>
                <strong>Alumnos procesados:</strong> ${result.alumnos_procesados}<br>
                <strong>Alumnos actualizados:</strong> ${result.alumnos_actualizados}
            </div>
        `;
        
        // Mostrar análisis
        if (result.analisis) {
            displayClusteringAnalysis(result.analisis, result.recomendaciones);
        }
        
    } catch (error) {
        statusDiv.innerHTML = `
            <div class="status-message error">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>Error:</strong> ${error.message}
            </div>
        `;
    } finally {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-cogs"></i> Procesar Clustering';
    }
}

async function loadClusterStatistics() {
    const container = document.getElementById('clusterStatistics');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando estadísticas...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/clustering/statistics`);
        if (!response.ok) throw new Error('Error al cargar estadísticas');
        
        const data = await response.json();
        displayClusterStatistics(data.statistics);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayClusterStatistics(stats) {
    const container = document.getElementById('clusterStatistics');
    
    let html = '<div class="clustering-stats">';
    
    // Estadísticas de K-Means
    html += '<div class="cluster-section">';
    html += '<h4><i class="fas fa-chart-pie"></i> Estadísticas K-Means</h4>';
    if (stats.kmeans && stats.kmeans.length > 0) {
        html += '<div class="stats-grid">';
        stats.kmeans.forEach(cluster => {
            html += `
                <div class="stat-card">
                    <div class="stat-header">Cluster ${cluster.cluster}</div>
                    <div class="stat-content">
                        <p><strong>Cantidad:</strong> ${cluster.count}</p>
                        <p><strong>CI Promedio:</strong> ${cluster.avg_ci.toFixed(1)}</p>
                        <p><strong>Calificación Promedio:</strong> ${cluster.avg_grades.toFixed(1)}</p>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    } else {
        html += '<p class="no-data">No hay datos de clusters K-Means</p>';
    }
    html += '</div>';
    
    // Estadísticas de DBSCAN
    html += '<div class="cluster-section">';
    html += '<h4><i class="fas fa-chart-scatter"></i> Estadísticas DBSCAN</h4>';
    if (stats.dbscan && stats.dbscan.length > 0) {
        html += '<div class="stats-grid">';
        stats.dbscan.forEach(cluster => {
            html += `
                <div class="stat-card">
                    <div class="stat-header">Cluster ${cluster.cluster}</div>
                    <div class="stat-content">
                        <p><strong>Cantidad:</strong> ${cluster.count}</p>
                        <p><strong>CI Promedio:</strong> ${cluster.avg_ci.toFixed(1)}</p>
                        <p><strong>Calificación Promedio:</strong> ${cluster.avg_grades.toFixed(1)}</p>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    } else {
        html += '<p class="no-data">No hay datos de clusters DBSCAN</p>';
    }
    html += '</div>';
    
    html += '</div>';
    container.innerHTML = html;
}

async function loadClusteringAnalysis() {
    const container = document.getElementById('clusterStatistics');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando análisis completo...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/clustering/analysis`);
        if (!response.ok) throw new Error('Error al cargar análisis');
        
        const data = await response.json();
        displayClusteringAnalysis(data.analysis);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayClusteringAnalysis(analysis, recommendations = null) {
    const container = document.getElementById('clusterStatistics');
    
    let html = '<div class="clustering-analysis">';
    
    // Resumen general
    html += '<div class="analysis-summary">';
    html += '<h4><i class="fas fa-chart-line"></i> Resumen del Análisis</h4>';
    html += `<p><strong>Total de alumnos:</strong> ${analysis.total_alumnos}</p>`;
    html += `<p><strong>Clusters K-Means:</strong> ${analysis.clusters_kmeans}</p>`;
    html += `<p><strong>Clusters DBSCAN:</strong> ${analysis.clusters_dbscan}</p>`;
    html += '</div>';
    
    // Distribución de clusters
    if (analysis.distribucion_kmeans) {
        html += '<div class="cluster-distribution">';
        html += '<h4><i class="fas fa-chart-pie"></i> Distribución K-Means</h4>';
        html += '<div class="distribution-grid">';
        Object.entries(analysis.distribucion_kmeans).forEach(([cluster, count]) => {
            const percentage = ((count / analysis.total_alumnos) * 100).toFixed(1);
            html += `
                <div class="distribution-item">
                    <div class="distribution-label">${cluster}</div>
                    <div class="distribution-bar">
                        <div class="distribution-fill" style="width: ${percentage}%"></div>
                    </div>
                    <div class="distribution-count">${count} (${percentage}%)</div>
                </div>
            `;
        });
        html += '</div>';
        html += '</div>';
    }
    
    if (analysis.distribucion_dbscan) {
        html += '<div class="cluster-distribution">';
        html += '<h4><i class="fas fa-chart-scatter"></i> Distribución DBSCAN</h4>';
        html += '<div class="distribution-grid">';
        Object.entries(analysis.distribucion_dbscan).forEach(([cluster, count]) => {
            const percentage = ((count / analysis.total_alumnos) * 100).toFixed(1);
            html += `
                <div class="distribution-item">
                    <div class="distribution-label">${cluster}</div>
                    <div class="distribution-bar">
                        <div class="distribution-fill" style="width: ${percentage}%"></div>
                    </div>
                    <div class="distribution-count">${count} (${percentage}%)</div>
                </div>
            `;
        });
        html += '</div>';
        html += '</div>';
    }
    
    // Recomendaciones si están disponibles
    if (recommendations) {
        html += '<div class="clustering-recommendations">';
        html += '<h4><i class="fas fa-lightbulb"></i> Recomendaciones</h4>';
        
        if (recommendations.kmeans && recommendations.kmeans.general_insights) {
            html += '<div class="recommendation-section">';
            html += '<h5>K-Means - Insights Generales</h5>';
            html += '<ul>';
            recommendations.kmeans.general_insights.forEach(insight => {
                html += `<li>${insight}</li>`;
            });
            html += '</ul>';
            html += '</div>';
        }
        
        if (recommendations.dbscan && recommendations.dbscan.general_insights) {
            html += '<div class="recommendation-section">';
            html += '<h5>DBSCAN - Insights Generales</h5>';
            html += '<ul>';
            recommendations.dbscan.general_insights.forEach(insight => {
                html += `<li>${insight}</li>`;
            });
            html += '</ul>';
            html += '</div>';
        }
        
        html += '</div>';
    }
    
    html += '</div>';
    container.innerHTML = html;
}

async function loadAlumnosWithClusters() {
    const container = document.getElementById('alumnosWithClusters');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando alumnos con clusters...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/clustering/alumnos`);
        if (!response.ok) throw new Error('Error al cargar alumnos');
        
        const data = await response.json();
        displayAlumnosWithClusters(data.alumnos);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayAlumnosWithClusters(alumnos) {
    const container = document.getElementById('alumnosWithClusters');
    
    if (alumnos.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay alumnos con clusters</div>';
        return;
    }
    
    container.innerHTML = alumnos.map(alumno => `
        <div class="item-card cluster-card">
            <div class="item-header">
                <div class="item-title">${alumno.nombre || 'Sin nombre'}</div>
                <div class="cluster-badges">
                    <span class="cluster-badge kmeans">K-Means: ${alumno.cluster_kmeans}</span>
                    <span class="cluster-badge dbscan">DBSCAN: ${alumno.cluster_dbscan}</span>
                </div>
            </div>
            <div class="item-details">
                <div class="alumno-info">
                    <p><strong>ID:</strong> ${alumno.alumno_id}</p>
                    <p><strong>CI:</strong> ${alumno.ci || 'N/A'}</p>
                    <p><strong>Promedio:</strong> ${alumno.promedio_calificaciones || 'N/A'}</p>
                    <p><strong>Competencias:</strong> ${alumno.cantidad_competencias || 0}</p>
                </div>
                <div class="alumno-details">
                    <div class="inteligencias-summary">
                        <strong>Inteligencias:</strong> ${alumno.inteligencias.length} tipos
                        ${alumno.inteligencias.length > 0 ? `(Max: ${Math.max(...alumno.inteligencias.map(i => i.puntaje))})` : ''}
                    </div>
                    <div class="calificaciones-summary">
                        <strong>Calificaciones:</strong> ${alumno.calificaciones.length} competencias
                        ${alumno.calificaciones.length > 0 ? `(Promedio: ${(alumno.calificaciones.reduce((sum, c) => {
                            const val = c.calificacion === 'A' ? 4 : c.calificacion === 'B' ? 3 : c.calificacion === 'C' ? 2 : 1;
                            return sum + val;
                        }, 0) / alumno.calificaciones.length).toFixed(1)})` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Funciones de Gestión de Profesores y Cursos
async function loadProfesores() {
    const container = document.getElementById('profesoresList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando profesores...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/`);
        if (!response.ok) throw new Error('Error al cargar profesores');
        
        const profesores = await response.json();
        displayProfesores(profesores);
        
        // Actualizar selects de profesores
        updateProfesorSelects(profesores);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayProfesores(profesores) {
    const container = document.getElementById('profesoresList');
    
    if (profesores.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay profesores registrados</div>';
        return;
    }
    
    container.innerHTML = profesores.map(profesor => `
        <div class="item-card">
            <div class="item-header">
                <div class="item-title">${profesor.Nombre}</div>
                <div class="item-actions">
                    <button class="btn btn-success" onclick="editProfesor(${profesor.Profesor_ID})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn btn-danger" onclick="deleteProfesor(${profesor.Profesor_ID})">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                    <button class="btn btn-info" onclick="verCursosProfesor(${profesor.Profesor_ID})">
                        <i class="fas fa-book"></i> Ver Cursos
                    </button>
                </div>
            </div>
            <div class="item-details">
                <p><strong>ID:</strong> ${profesor.Profesor_ID}</p>
                <p><strong>DNI:</strong> ${profesor.DNI}</p>
            </div>
        </div>
    `).join('');
}

function updateProfesorSelects(profesores) {
    const selects = [
        'asignarProfesor',
        'verCursosProfesor', 
        'estadisticasProfesor'
    ];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            // Mantener la opción por defecto
            const defaultOption = select.querySelector('option[value=""]');
            select.innerHTML = '';
            if (defaultOption) {
                select.appendChild(defaultOption);
            }
            
            // Agregar opciones de profesores
            profesores.forEach(profesor => {
                const option = document.createElement('option');
                option.value = profesor.Profesor_ID;
                option.textContent = profesor.Nombre;
                select.appendChild(option);
            });
        }
    });
}

async function loadCursosDisponibles() {
    const container = document.getElementById('profesoresList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando cursos disponibles...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/cursos/disponibles`);
        if (!response.ok) throw new Error('Error al cargar cursos');
        
        const cursos = await response.json();
        displayCursosDisponibles(cursos);
        
        // Actualizar select de cursos
        updateCursoSelect(cursos);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayCursosDisponibles(cursos) {
    const container = document.getElementById('profesoresList');
    
    if (cursos.length === 0) {
        container.innerHTML = '<div class="status-message info">No hay cursos disponibles</div>';
        return;
    }
    
    container.innerHTML = `
        <div class="status-message success">
            <i class="fas fa-check-circle"></i>
            <strong>Cursos Disponibles (${cursos.length})</strong>
        </div>
        ${cursos.map(curso => `
            <div class="item-card">
                <div class="item-header">
                    <div class="item-title">${curso.Nombre}</div>
                </div>
                <div class="item-details">
                    <p><strong>ID:</strong> ${curso.Curso_ID}</p>
                </div>
            </div>
        `).join('')}
    `;
}

function updateCursoSelect(cursos) {
    const select = document.getElementById('asignarCurso');
    if (select) {
        // Mantener la opción por defecto
        const defaultOption = select.querySelector('option[value=""]');
        select.innerHTML = '';
        if (defaultOption) {
            select.appendChild(defaultOption);
        }
        
        // Agregar opciones de cursos
        cursos.forEach(curso => {
            const option = document.createElement('option');
            option.value = curso.Curso_ID;
            option.textContent = curso.Nombre;
            select.appendChild(option);
        });
    }
}

async function asignarCursoProfesor() {
    const profesorId = document.getElementById('asignarProfesor').value;
    const cursoId = document.getElementById('asignarCurso').value;
    
    if (!profesorId || !cursoId) {
        showStatus('Por favor selecciona un profesor y un curso', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/${profesorId}/cursos/${cursoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al asignar curso');
        }
        
        const result = await response.json();
        showStatus(result.message, 'success');
        
        // Limpiar selects
        document.getElementById('asignarProfesor').value = '';
        document.getElementById('asignarCurso').value = '';
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function desasignarCursoProfesor() {
    const profesorId = document.getElementById('asignarProfesor').value;
    const cursoId = document.getElementById('asignarCurso').value;
    
    if (!profesorId || !cursoId) {
        showStatus('Por favor selecciona un profesor y un curso', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/${profesorId}/cursos/${cursoId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al desasignar curso');
        }
        
        const result = await response.json();
        showStatus(result.message, 'success');
        
        // Limpiar selects
        document.getElementById('asignarProfesor').value = '';
        document.getElementById('asignarCurso').value = '';
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function loadCursosProfesor() {
    const profesorId = document.getElementById('verCursosProfesor').value;
    if (!profesorId) {
        document.getElementById('cursosProfesor').innerHTML = '';
        return;
    }
    
    const container = document.getElementById('cursosProfesor');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando cursos del profesor...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/${profesorId}/cursos`);
        if (!response.ok) throw new Error('Error al cargar cursos del profesor');
        
        const cursos = await response.json();
        displayCursosProfesor(cursos);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayCursosProfesor(cursos) {
    const container = document.getElementById('cursosProfesor');
    
    if (cursos.length === 0) {
        container.innerHTML = '<div class="status-message info">Este profesor no tiene cursos asignados</div>';
        return;
    }
    
    container.innerHTML = `
        <div class="status-message success">
            <i class="fas fa-check-circle"></i>
            <strong>Cursos Asignados (${cursos.length})</strong>
        </div>
        ${cursos.map(curso => `
            <div class="item-card">
                <div class="item-header">
                    <div class="item-title">${curso.Nombre}</div>
                </div>
                <div class="item-details">
                    <p><strong>ID:</strong> ${curso.Curso_ID}</p>
                </div>
            </div>
        `).join('')}
    `;
}

async function loadEstadisticasProfesor() {
    const profesorId = document.getElementById('estadisticasProfesor').value;
    if (!profesorId) {
        document.getElementById('estadisticasProfesor').innerHTML = '';
        return;
    }
    
    const container = document.getElementById('estadisticasProfesor');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Cargando estadísticas...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/${profesorId}/estadisticas`);
        if (!response.ok) throw new Error('Error al cargar estadísticas');
        
        const estadisticas = await response.json();
        displayEstadisticasProfesor(estadisticas);
    } catch (error) {
        container.innerHTML = `<div class="status-message error">Error: ${error.message}</div>`;
    }
}

function displayEstadisticasProfesor(estadisticas) {
    const container = document.getElementById('estadisticasProfesor');
    
    container.innerHTML = `
        <div class="stats-container">
            <h3>Estadísticas de ${estadisticas.nombre}</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-title">Total Cursos</div>
                    <div class="stat-number">${estadisticas.total_cursos}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">Total Alumnos</div>
                    <div class="stat-number">${estadisticas.total_alumnos}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">Promedio Calificaciones</div>
                    <div class="stat-number">${estadisticas.promedio_calificaciones.toFixed(2)}</div>
                </div>
            </div>
            
            <div class="cursos-section">
                <h4>Cursos Asignados</h4>
                ${estadisticas.cursos_asignados.length > 0 ? 
                    estadisticas.cursos_asignados.map(curso => `
                        <div class="curso-item">
                            <strong>${curso.Nombre}</strong> (ID: ${curso.Curso_ID})
                        </div>
                    `).join('') : 
                    '<p>No hay cursos asignados</p>'
                }
            </div>
        </div>
    `;
}

async function editProfesor(profesorId) {
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/${profesorId}`);
        if (!response.ok) throw new Error('Error al cargar profesor');
        
        const profesor = await response.json();
        showEditModal('profesor', profesor);
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function deleteProfesor(profesorId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este profesor?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/profesores/${profesorId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Error al eliminar profesor');
        
        showStatus('Profesor eliminado exitosamente', 'success');
        loadProfesores();
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function verCursosProfesor(profesorId) {
    // Seleccionar el profesor en el select y cargar sus cursos
    const select = document.getElementById('verCursosProfesor');
    if (select) {
        select.value = profesorId;
        loadCursosProfesor();
    }
}