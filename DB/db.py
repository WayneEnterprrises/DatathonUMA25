from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import streamlit as st
import json

dataBaseUrl = "sqlite:///BruceLLM.db"
#Crea un enlace entre la base de datos real y la base de datos de la aplicación
engine = create_engine(dataBaseUrl)

metadata = MetaData()
metadata.reflect(bind=engine)

Base = automap_base(metadata=metadata)
#Refleja las tablas de la base de datos en la base de datos de la aplicación
Base.prepare(autoload_with=engine)

#Crea una sesión de la base de datos (comunicación con la base de datos, pseudoSocket)
Session = sessionmaker(bind=engine)
session = Session()

Notas = Base.classes.resumen_notas
Evolucion = Base.classes.resumen_evolucion
Medicacion = Base.classes.resumen_medicacion
LabIniciales = Base.classes.resumen_lab_iniciales
Pacientes = Base.classes.resumen_pacientes
Procedimientos = Base.classes.resumen_procedimientos
User = Base.classes.users
Chat = Base.classes.chats

def instance_to_dict(instance):
    """Convert an automapped instance to a dictionary."""
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

def json_info_from_instance_class(instance_class):
    """Convert an automapped class to a json object."""
    class_dict = instance_to_dict(instance_class)
    json_object = json.dumps(class_dict, indent=2)
    return json_object

def get_user_by_username(username):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user

def get_patient(patient_id):
    session = Session()
    patient = session.query(Pacientes).filter(Pacientes.id == patient_id).first()
    session.close()
    return patient

def get_all_patients():
    """Devuelve todos los pacientes del médico que esta autenticado actualmente."""
    session = Session()
    user = get_user_by_username(st.session_state["username"])
    patients = session.query(Pacientes).filter(Pacientes.Medico == user.ID).all()
    session.close()
    return patients

def save_chat_message(patient_id, role, message):
    """Guarda un mensaje en la base de datos asociado a un paciente."""
    session = Session()
    new_message = Chat(patient_id=patient_id, role=role, message=message)
    session.add(new_message)
    session.close()

def register_user(username, password):
    """Registra un usuario en la base de datos SQLite."""
    session = Session()
    if session.query(User).filter(User.username == username).first():
        return False  # Usuario ya existe
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.close()
    return True

def load_chat_history(patient_id):
    """Carga el historial de chat de un paciente."""
    session = Session()
    chat = session.query(Chat).filter(Chat.patient_id == patient_id).all()
    session.close()
    return chat
