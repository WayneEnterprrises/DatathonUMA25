from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData, select
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

#All of the methods should use modern sql alchemy syntax session.execute() https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute

def instance_to_dict(instance):
    """Convert an automapped instance to a dictionary."""
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns} #Itera todas las columnas, get attribute accede dinámicamente al valor del atributo column.name dentro del objeto instance, 
#que en este caso es una fila de la tabla.

def json_info_from_instance_class(instance_class):
    """Convert an automapped class to a json object."""
    
    class_dict = instance_to_dict(instance_class)
    
    json_object = json.dumps(class_dict, indent=2, ensure_ascii=False)
    
    return json_object

def all_patient_info(patient_id):
    
    statement_Pacientes = select(Pacientes).where(Pacientes.PacienteID == patient_id)
    statement_Notas = select(Notas).where(Notas.PacienteID == patient_id)
    statement_Evolucion = select(Evolucion).where(Evolucion.PacienteID == patient_id)
    statement_Medicacion = select(Medicacion).where(Medicacion.PacienteID == patient_id)
    statement_lab_Iniciales = select(LabIniciales).where(LabIniciales.PacienteID == patient_id)
    statement_Procedimientos = select(Procedimientos).where(Procedimientos.PacienteID == patient_id)
    
    #Desde la versión 2.0 de sqlAlchemy se recomienda utilizar execute, que devuelve un objeto result que es más eficiente en memoria
    #execute unifica la parte el core de sqlAlchemy (todo lo que es una forma de escribir queries, DML y DDL) y la parte ORM.
    
    #Al hacer result.scalars().all() se devuelve un iterable, en vez de una instancia (fila), en este caso estamos sacando información de un paciente, pero hay tablas en las que tenemos varias entradas,
    #por lo que hay que iterar
    listaDiccionarios = {
        "pacientes": [instance_to_dict(obj) for obj in session.execute(statement_Pacientes).scalars().all()],
        "notas": [instance_to_dict(obj) for obj in session.execute(statement_Notas).scalars().all()],
        "evolucion": [instance_to_dict(obj) for obj in session.execute(statement_Evolucion).scalars().all()],
        "medicacion": [instance_to_dict(obj) for obj in session.execute(statement_Medicacion).scalars().all()],
        "lab_iniciales": [instance_to_dict(obj) for obj in session.execute(statement_lab_Iniciales).scalars().all()],
        "procedimientos": [instance_to_dict(obj) for obj in session.execute(statement_Procedimientos).scalars().all()]
    } 
    json_object = json.dumps(listaDiccionarios, indent=2, ensure_ascii=False) #indent mete un indent en el json para que sea legible y ensure_ascii hace que no se codifiquen mal las tildes
    
    #print(json_object)
        #Añadirlos todos a un json
    
    #Ejecutamos todos los statements, añadiendo el resultado a un diccionario
    return json_object
    
    
    

        



def get_user_by_username(username):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user

def get_patient(patient_id):
    session = Session()
    patient = session.query(Pacientes).filter(Pacientes.id == patient_id).first() #Probablemente este método este mal, el atributo de la tabla es PacienteID, ya que se refiere a resumen pacientes
    session.close()
    return patient

def get_all_patients():
    """Devuelve todos los pacientes del médico que esta autenticado actualmente."""
    session = Session()
    #user = get_user_by_username(st.session_state["username"])
    #patients = session.query(Pacientes).filter(Pacientes.Medico == user.ID).all()
    patients = session.query(Pacientes).all()
    session.close()
    return patients

def register_user(username, password):
    """Registra un usuario en la base de datos SQLite."""
    session = Session()
    if session.query(User).filter(User.username == username).first():
        return False  # Usuario ya existe
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    session.close()
    return True
