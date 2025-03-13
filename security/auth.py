from sqlalchemy.orm import Session
from DB.database import SessionLocal, User, Patient, Chat
import streamlit as st
from DB.db import get_db

def authenticate_user(username, password):
    """Verifica si el usuario y la contraseña son correctos en la base de datos."""
    db = next(get_db())
    user = db.query(User).filter(User.username == username, User.password == password).first()
    return user is not None

def check_authentication():
    """🔐 Verifica si el usuario ha iniciado sesión antes de cargar la página."""
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("🔒 Debes iniciar sesión para acceder a esta página.")
        st.stop()


