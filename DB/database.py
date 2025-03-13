from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os
import pandas as pd
# Definir la base de datos SQLite

#Deberíamos cambiar el nombre de la base de datos
# Definir la base de datos SQLite
DB_FILE = "BruceLLM.db"
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Definir el modelo de base de datos
Base = declarative_base()


class ResumenEvolucion(Base):
    __tablename__ = "resumen_evolucion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer)
    fecha = Column(String)
    evolucion = Column(Text)

class ResumenLabIniciales(Base):
    __tablename__ = "resumen_lab_iniciales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer)
    fecha = Column(String)
    resultados = Column(Text)

class ResumenMedicacion(Base):
    __tablename__ = "resumen_medicacion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer)
    fecha = Column(String)
    medicamento = Column(String)
    dosis = Column(String)

class ResumenNotas(Base):
    __tablename__ = "resumen_notas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer)
    fecha = Column(String)
    nota = Column(Text)

class ResumenPacientes(Base):
    __tablename__ = "resumen_pacientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    edad = Column(Integer)
    sexo = Column(String)
    alergias = Column(String)
    motivo_ingreso = Column(Text)

class ResumenProcedimientos(Base):
    __tablename__ = "resumen_procedimientos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer)
    procedimientos = Column(Text)
    tratamientos = Column(Text)

# Crear las tablas en la base de datos
csv_files = {
    "resumen_evolucion": "data/resumen_evolucion.csv",
    "resumen_lab_iniciales": "data/resumen_lab_iniciales.csv",
    "resumen_medicacion": "data/resumen_medicacion.csv",
    "resumen_notas": "data/resumen_notas.csv",
    "resumen_pacientes": "data/resumen_pacientes.csv",
    "resumen_procedimientos": "data/resumen_procedimientos.csv",
}

# Función para importar los datos de los CSV a la base de datos
def import_csvs_to_db():
    """Carga los CSVs en la base de datos para evitar procesarlos en cada consulta."""
    db = SessionLocal()

    for table_name, file_path in csv_files.items():
        try:
            # Cargar el CSV en un DataFrame
            df = pd.read_csv(file_path, delimiter=",", on_bad_lines="skip", encoding="utf-8")
            print(df)
            # Guardar en la base de datos (reemplaza la tabla si ya existe)
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            print(f"✅ {table_name} importado correctamente.")

        except Exception as e:
            print(f"❌ Error importando {table_name}: {e}")
            
    db.commit()
    db.close()

import_csvs_to_db()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    patients = relationship("Patient", back_populates="user", cascade="all, delete-orphan")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, ForeignKey("users.username"), nullable=False)

    user = relationship("User", back_populates="patients")
    chats = relationship("Chat", back_populates="patient", cascade="all, delete-orphan")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" o "assistant"
    message = Column(Text, nullable=False)

    patient = relationship("Patient", back_populates="chats")

# Crear la base de datos si no existe
if not os.path.exists(DB_FILE):
    Base.metadata.create_all(engine)

# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(bind=engine)

