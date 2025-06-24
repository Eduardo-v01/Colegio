from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.services import excel_processor
from app.database.database import get_db
import tempfile
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload")
async def upload_excel(
    file: UploadFile = File(...), 
    actualizar_existentes: bool = Query(True, description="Si es True, actualiza datos existentes. Si es False, solo crea nuevos registros"),
    db: Session = Depends(get_db)
):
    logger.info(f"Recibiendo archivo: {file.filename}")
    logger.info(f"Modo actualización: {'Activado' if actualizar_existentes else 'Desactivado'}")
    
    # Validar tipo de archivo
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Formato de archivo no válido. Solo se permiten archivos .xlsx y .xls")
    
    # Validar tamaño del archivo (máximo 10MB)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El archivo es demasiado grande. Máximo 10MB")
    
    tmp_path = None
    try:
        # Guardar archivo temporal
        logger.info("Guardando archivo temporal...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
            logger.info(f"Archivo temporal guardado en: {tmp_path}")
        
        # Verificar que el archivo se guardó correctamente
        if not os.path.exists(tmp_path):
            raise HTTPException(status_code=500, detail="Error al guardar el archivo temporal")
        
        # Procesar archivo
        logger.info("Iniciando procesamiento del archivo...")
        result = excel_processor.procesar_excel(db, tmp_path, modo_actualizacion=actualizar_existentes)
        logger.info("Procesamiento completado exitosamente")
        
        return result
        
    except HTTPException:
        # Re-lanzar HTTPExceptions sin modificar
        raise
    except Exception as e:
        logger.error(f"Error procesando archivo: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error procesando archivo: {str(e)}. Verifica que el archivo tenga las hojas requeridas: 'notas', 'inteligencia', 'ci'"
        )
    finally:
        # Limpiar archivo temporal
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
                logger.info("Archivo temporal eliminado")
            except Exception as e:
                logger.warning(f"Error eliminando archivo temporal: {str(e)}")