from sqlalchemy.orm import Session
from DB.database import SessionLocal, User, Patient, Chat

def get_db():
    """Crea una nueva sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_patients(username):
    """Devuelve la lista de pacientes de un usuario."""
    db = next(get_db())
    return db.query(Patient).filter(Patient.username == username).all()

def add_patient(username, patient_name):
    """Agrega un paciente a la base de datos."""
    db = next(get_db())
    existing_patient = db.query(Patient).filter(Patient.username == username, Patient.name == patient_name).first()
    if not existing_patient:
        new_patient = Patient(name=patient_name, username=username)
        db.add(new_patient)
        db.commit()

def save_chat_message(patient_id, role, message):
    """Guarda un mensaje en la base de datos asociado a un paciente."""
    db = next(get_db())
    new_message = Chat(patient_id=patient_id, role=role, message=message)
    db.add(new_message)
    db.commit()

def load_chat_history(patient_id):
    """Carga el historial de chat de un paciente."""
    db = next(get_db())
    return db.query(Chat).filter(Chat.patient_id == patient_id).all()

def register_user(username, password):
    """Registra un usuario en la base de datos SQLite."""
    db = next(get_db())
    if db.query(User).filter(User.username == username).first():
        return False  # Usuario ya existe
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    return True