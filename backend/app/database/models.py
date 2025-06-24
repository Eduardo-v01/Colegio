from sqlalchemy import (
    Column, Integer, String, Float, Text, BLOB,
    ForeignKey, Table, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabla de asociación N:M para Profesores y Cursos
ProfesorCurso = Table('ProfesorCurso', Base.metadata,
    Column('Profesor_ID', Integer, ForeignKey('Profesores.Profesor_ID'), primary_key=True),
    Column('Curso_ID', Integer, ForeignKey('Cursos.Curso_ID'), primary_key=True)
)

class Alumno(Base):
    __tablename__ = "Alumnos"
    Alumno_ID = Column(Integer, primary_key=True)
    Nombre = Column(Text, nullable=False)
    Promedio_Calificaciones = Column(Float)
    Cantidad_Competencias = Column(Integer)
    CI = Column(Integer)
    Cluster_KMeans = Column(Integer)
    Cluster_DBSCAN = Column(Integer)
    Recomendaciones_Basicas = Column(Text)

    # Relaciones
    calificaciones = relationship("AlumnoCompetencia", back_populates="alumno", cascade="all, delete-orphan")
    inteligencias = relationship("Inteligencia", back_populates="alumno", cascade="all, delete-orphan")

class Profesor(Base):
    __tablename__ = "Profesores"
    Profesor_ID = Column(Integer, primary_key=True)
    Nombre = Column(Text, nullable=False)
    DNI = Column(Text, unique=True, nullable=False)
    Contrasena_Hash = Column(BLOB, nullable=False)

    # Relación N:M con Cursos
    cursos = relationship("Curso", secondary=ProfesorCurso, back_populates="profesores")

class Curso(Base):
    __tablename__ = "Cursos"
    Curso_ID = Column(Integer, primary_key=True)
    Nombre = Column(Text, unique=True, nullable=False)

    # Relación N:M con Profesores
    profesores = relationship("Profesor", secondary=ProfesorCurso, back_populates="cursos")
    # Relación 1:N con CompetenciaPlantilla
    plantilla_competencias = relationship("CompetenciaPlantilla", back_populates="curso", cascade="all, delete-orphan")

class CompetenciaPlantilla(Base):
    __tablename__ = "CompetenciaPlantilla"
    CompetenciaPlantilla_ID = Column(Integer, primary_key=True)
    Curso_ID = Column(Integer, ForeignKey("Cursos.Curso_ID"), nullable=False)
    Codigo_Competencia = Column(Text, nullable=False)
    Descripcion = Column(Text)

    # Relación N:1 con Curso
    curso = relationship("Curso", back_populates="plantilla_competencias")
    # Relaciones
    calificaciones_alumnos = relationship("AlumnoCompetencia", back_populates="competencia", cascade="all, delete-orphan")
    
    __table_args__ = (PrimaryKeyConstraint('CompetenciaPlantilla_ID'),)


class AlumnoCompetencia(Base):
    __tablename__ = "AlumnoCompetencia"
    AlumnoCompetencia_ID = Column(Integer, primary_key=True)
    Alumno_ID = Column(Integer, ForeignKey("Alumnos.Alumno_ID"), nullable=False)
    CompetenciaPlantilla_ID = Column(Integer, ForeignKey("CompetenciaPlantilla.CompetenciaPlantilla_ID"), nullable=False)
    Calificacion = Column(Text, nullable=False)
    Conclusion_descriptiva = Column(Text)

    # Relaciones
    alumno = relationship("Alumno", back_populates="calificaciones")
    competencia = relationship("CompetenciaPlantilla", back_populates="calificaciones_alumnos")
    
    __table_args__ = (PrimaryKeyConstraint('AlumnoCompetencia_ID'),)


class Inteligencia(Base):
    __tablename__ = "Inteligencias"
    Inteligencia_ID = Column(Integer, primary_key=True)
    Alumno_ID = Column(Integer, ForeignKey("Alumnos.Alumno_ID"), nullable=False)
    Tipo_Inteligencia = Column(Text, nullable=False)
    Puntaje = Column(Float, nullable=False)

    # Relación N:1 con Alumno
    alumno = relationship("Alumno", back_populates="inteligencias")

class ConversacionIA(Base):
    __tablename__ = "ConversacionesIA"
    Conversacion_ID = Column(Integer, primary_key=True)
    Alumno_ID = Column(Integer, ForeignKey("Alumnos.Alumno_ID"), nullable=False)
    Profesor_ID = Column(Integer, ForeignKey("Profesores.Profesor_ID"), nullable=False)
    Mensaje = Column(Text, nullable=False)
    Es_Usuario = Column(Integer, nullable=False)  # 1 = Profesor, 0 = IA
    Fecha_Creacion = Column(Text, nullable=False)  # ISO format string
    Contexto_Alumno = Column(Text)  # JSON con datos del alumno al momento de la conversación
    
    # Relaciones
    alumno = relationship("Alumno")
    profesor = relationship("Profesor")