// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8001/api';

// Variables globales
let currentEditId = null;
let currentEditType = null;
let currentStudentProfile = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeChat(); // Inicializar chat
    loadAlumnos(); // Cargar datos iniciales
    loadAlumnosForSelect(); // Cargar alumnos para el select de inteligencias
    loadTiposInteligencia(); // Cargar tipos de inteligencia para el select
    loadStudentsForAI(); // Cargar alumnos para la IA
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
        case 'ai-assistant':
            loadStudentsForAI();
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
    const inteligenciasHTML = alumno.inteligencias.map(intel => `
        <div class="inteligencia-bar">
            <div class="inteligencia-label">${intel.tipo}</div>
            <div class="inteligencia-progress">
                <div class="inteligencia-fill" style="width: ${intel.puntaje}%"></div>
                <div class="inteligencia-value">${intel.puntaje}</div>
            </div>
        </div>
    `).join('');
    
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
            <p>La IA está analizando el perfil de ${currentStudentProfile.nombre}...</p>
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
        } else {
            container.innerHTML = `
                <div class="ai-error">
                    <h4><i class="fas fa-exclamation-triangle"></i> Error en la IA</h4>
                    <p>${data.error || 'No se pudieron generar recomendaciones'}</p>
                </div>
            `;
        }
        
    } catch (error) {
        container.innerHTML = `
            <div class="ai-error">
                <h4><i class="fas fa-exclamation-triangle"></i> Error</h4>
                <p>${error.message}</p>
            </div>
        `;
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function displayAIRecommendations(data) {
    const container = document.getElementById('aiRecommendations');
    
    let summaryHTML = '';
    if (data.analysis_summary) {
        const summary = data.analysis_summary;
        summaryHTML = `
            <div class="ai-summary">
                <h5><i class="fas fa-chart-bar"></i> Resumen del Análisis</h5>
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
            <h4>Recomendaciones para ${data.student_name}</h4>
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
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    
    chatForm.addEventListener('submit', handleChatSubmit);
    
    // Permitir enviar con Enter
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
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
    avatar.textContent = sender === 'user' ? 'Tú' : 'IA';
    
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
        <span>La IA está escribiendo...</span>
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
    if (!currentStudentProfile) {
        showStatus('Primero debes cargar el perfil de un alumno', 'warning');
        return;
    }
    
    if (!confirm('¿Estás seguro de que quieres limpiar todo el historial de conversación?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/ai-assistant/conversation/${currentStudentProfile.alumno_id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Error al limpiar historial');
        
        const data = await response.json();
        
        if (data.success) {
            // Limpiar chat actual
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="chat-welcome">
                    <i class="fas fa-robot"></i>
                    <p>¡Hola! Soy tu asistente pedagógica. Puedes hacerme preguntas específicas sobre el alumno seleccionado.</p>
                    <p><strong>Ejemplos de preguntas:</strong></p>
                    <ul>
                        <li>"¿Cómo puedo ayudarle con matemáticas?"</li>
                        <li>"¿Qué actividades le recomiendas para mejorar su concentración?"</li>
                        <li>"¿Cómo puedo motivarlo más en clase?"</li>
                        <li>"¿Qué estrategias funcionan mejor para su tipo de inteligencia?"</li>
                    </ul>
                </div>
            `;
            
            showStatus('Historial de conversación limpiado', 'success');
        }
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
} 