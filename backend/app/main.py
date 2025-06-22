from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import database, models
from app.database.database import get_db
from app.routers import alumnos, cursos, competencias, upload, inteligencias, ci, ai_assistant

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"message": "Sistema de Gestión Educativa"}

@app.get("/frontend")
def serve_frontend():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)