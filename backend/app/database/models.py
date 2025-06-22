from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, BLOB
from sqlalchemy.orm import relationship
from .database import Base

class Alumno(Base):
    __tablename__ = "Alumnos"
    Alumno_ID = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String, nullable=False)
    Promedio_Calificaciones = Column(Float)
    Cantidad_Competencias = Column(Integer)
    CI = Column(Integer)
    Cluster_KMeans = Column(Integer)
    Cluster_DBSCAN = Column(Integer)
    Recomendaciones_Basicas = Column(Text)
    calificaciones = relationship("AlumnoCompetencia", back_populates="alumno")
    inteligencias = relationship("Inteligencia", back_populates="alumno")

class Curso(Base):
    __tablename__ = "Cursos"
    Curso_ID = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String, unique=True, nullable=False)
    competencias = relationship("CompetenciaPlantilla", back_populates="curso")

class CompetenciaPlantilla(Base):
    __tablename__ = "CompetenciaPlantilla"
    CompetenciaPlantilla_ID = Column(Integer, primary_key=True, index=True)
    Curso_ID = Column(Integer, ForeignKey("Cursos.Curso_ID"))
    Codigo_Competencia = Column(String, nullable=False)
    Descripcion = Column(Text)
    curso = relationship("Curso", back_populates="competencias")

class AlumnoCompetencia(Base):
    __tablename__ = "AlumnoCompetencia"
    AlumnoCompetencia_ID = Column(Integer, primary_key=True, index=True)
    Alumno_ID = Column(Integer, ForeignKey("Alumnos.Alumno_ID"))
    CompetenciaPlantilla_ID = Column(Integer, ForeignKey("CompetenciaPlantilla.CompetenciaPlantilla_ID"))
    Calificacion = Column(String(1), nullable=False)
    Conclusion_descriptiva = Column(Text)
    alumno = relationship("Alumno", back_populates="calificaciones")

class Inteligencia(Base):
    __tablename__ = "Inteligencias"
    Inteligencia_ID = Column(Integer, primary_key=True, index=True)
    Alumno_ID = Column(Integer, ForeignKey("Alumnos.Alumno_ID"))
    Tipo_Inteligencia = Column(String, nullable=False)
    Puntaje = Column(Float, nullable=False)
    alumno = relationship("Alumno", back_populates="inteligencias")