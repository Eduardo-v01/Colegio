from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from typing import List

from app.database import crud, database, models
from app.schemas import profesor as profesor_schema
from app.services import auth

router = APIRouter(
    prefix="/profesores",
    tags=["profesores"],
)

async def get_current_profesor(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        dni: str = payload.get("sub")
        if dni is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    profesor = crud.get_profesor_by_dni(db, dni=dni)
    if profesor is None:
        raise credentials_exception
    return profesor

# Endpoints de autenticación
@router.post("/register", response_model=profesor_schema.Profesor)
def register_profesor(profesor: profesor_schema.ProfesorCreate, db: Session = Depends(database.get_db)):
    db_profesor = crud.get_profesor_by_dni(db, dni=profesor.DNI)
    if db_profesor:
        raise HTTPException(status_code=400, detail="DNI already registered")
    return crud.create_profesor(db=db, profesor=profesor)

@router.post("/login", response_model=profesor_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    profesor = crud.get_profesor_by_dni_or_name(db, identifier=form_data.username)
    if not profesor or not auth.verify_password(form_data.password, profesor.Contrasena_Hash.decode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="DNI/Nombre o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": profesor.DNI}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=profesor_schema.Profesor)
async def read_profesor_me(current_profesor = Depends(get_current_profesor)):
    return current_profesor

# Endpoints CRUD para profesores
@router.get("/", response_model=List[profesor_schema.Profesor])
def get_profesores(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Obtener lista de todos los profesores"""
    profesores = crud.get_profesores(db, skip=skip, limit=limit)
    return profesores

@router.get("/{profesor_id}", response_model=profesor_schema.Profesor)
def get_profesor(profesor_id: int, db: Session = Depends(database.get_db)):
    """Obtener un profesor específico por ID"""
    profesor = crud.get_profesor(db, profesor_id=profesor_id)
    if profesor is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

@router.put("/{profesor_id}", response_model=profesor_schema.Profesor)
def update_profesor(profesor_id: int, profesor: profesor_schema.ProfesorUpdate, db: Session = Depends(database.get_db)):
    """Actualizar información de un profesor"""
    db_profesor = crud.update_profesor(db, profesor_id=profesor_id, profesor=profesor)
    if db_profesor is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return db_profesor

@router.delete("/{profesor_id}")
def delete_profesor(profesor_id: int, db: Session = Depends(database.get_db)):
    """Eliminar un profesor"""
    success = crud.delete_profesor(db, profesor_id=profesor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return {"message": "Profesor eliminado exitosamente"}

# Endpoints para gestión de cursos de profesores
@router.get("/{profesor_id}/cursos", response_model=List[profesor_schema.CursoInfo])
def get_profesor_cursos(profesor_id: int, db: Session = Depends(database.get_db)):
    """Obtener cursos asignados a un profesor"""
    cursos = crud.get_profesor_cursos(db, profesor_id=profesor_id)
    return cursos

@router.post("/{profesor_id}/cursos/{curso_id}")
def asignar_curso_profesor(profesor_id: int, curso_id: int, db: Session = Depends(database.get_db)):
    """Asignar un curso a un profesor"""
    success = crud.asignar_curso_profesor(db, profesor_id=profesor_id, curso_id=curso_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo asignar el curso")
    return {"message": "Curso asignado exitosamente"}

@router.delete("/{profesor_id}/cursos/{curso_id}")
def desasignar_curso_profesor(profesor_id: int, curso_id: int, db: Session = Depends(database.get_db)):
    """Desasignar un curso de un profesor"""
    success = crud.desasignar_curso_profesor(db, profesor_id=profesor_id, curso_id=curso_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo desasignar el curso")
    return {"message": "Curso desasignado exitosamente"}

@router.get("/cursos/disponibles", response_model=List[profesor_schema.CursoInfo])
def get_cursos_disponibles(db: Session = Depends(database.get_db)):
    """Obtener todos los cursos disponibles"""
    cursos = crud.get_cursos_disponibles(db)
    return cursos

# Endpoints para estadísticas de profesores
@router.get("/{profesor_id}/estadisticas")
def get_profesor_estadisticas(profesor_id: int, db: Session = Depends(database.get_db)):
    """Obtener estadísticas de un profesor"""
    estadisticas = crud.get_profesor_estadisticas(db, profesor_id=profesor_id)
    if estadisticas is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return estadisticas 