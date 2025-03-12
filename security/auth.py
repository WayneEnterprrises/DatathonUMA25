from sqlalchemy.orm import Session
from DB.database import SessionLocal, User, Chat
import streamlit as st

def get_db():
    """Crea una nueva sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_user(username, password):
    """Registra un usuario en la base de datos SQLite."""
    db = next(get_db())
    if db.query(User).filter(User.username == username).first():
        return False  
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    return True

def authenticate_user(username, password):
    """Verifica si el usuario y la contraseña son correctos en la base de datos."""
    db = next(get_db())
    user = db.query(User).filter(User.username == username, User.password == password).first()
    return user is not None

def check_authentication():
    """🔐 Verifica si el usuario ha iniciado sesión antes de cargar la página"""
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("🔒 Debes iniciar sesión para acceder a esta página.")
        st.stop()

def save_chat_message(username, role, message):
    """Guarda un mensaje en la base de datos."""
    db = next(get_db())
    new_message = Chat(username=username, role=role, message=message)
    db.add(new_message)
    db.commit()

def load_chat_history(username):
    """Carga el historial de chat del usuario."""
    db = next(get_db())
    return db.query(Chat).filter(Chat.username == username).all()
