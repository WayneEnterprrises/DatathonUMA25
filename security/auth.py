from DB.dbInterface import User, Session
import streamlit as st

def authenticate_user(username, password):
    """Verifica si el usuario y la contraseña son correctos en la base de datos."""
    session = Session()
    user = session.query(User).filter(User.username == username, User.password == password).first()
    session.close()
    return user is not None

def check_authentication():
    """🔐 Verifica si el usuario ha iniciado sesión antes de cargar la página."""
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("🔒 Debes iniciar sesión para acceder a esta página.")
        st.stop()


