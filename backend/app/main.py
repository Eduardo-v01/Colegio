import logging
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import database, models
from app.database.database import get_db
from app.routers import alumnos, cursos, competencias, upload, inteligencias, ci, ai_assistant, profesores, personal_chat, clustering

# Configurar logging detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Gestión de Alumnos", version="2.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Crear tablas al iniciar
models.Base.metadata.create_all(bind=database.engine)

# Incluir routers
app.include_router(upload.router, prefix="/api")
app.include_router(alumnos.router, prefix="/api")
app.include_router(cursos.router, prefix="/api")
app.include_router(competencias.router, prefix="/api")
app.include_router(inteligencias.router, prefix="/api")
app.include_router(ci.router, prefix="/api")
app.include_router(ai_assistant.router, prefix="/api")
app.include_router(profesores.router, prefix="/api")
app.include_router(personal_chat.router, prefix="/api")
app.include_router(clustering.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Sistema de Gestión de Alumnos v2.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0"}

@app.get("/frontend")
def serve_frontend():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)