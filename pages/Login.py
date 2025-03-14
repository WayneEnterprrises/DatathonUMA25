import streamlit as st
import time
from security.auth import authenticate_user
from DB.db import register_user

def login_form():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "username" not in st.session_state:
        st.session_state["username"] = "Usuario Anónimo"

    if "login_mode" not in st.session_state:
        st.session_state["login_mode"] = None
        
    st.markdown(
    """
    <style>
        body {
            background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
            color: white;
            text-align: center;
        }
        .stButton button {
            width: 250px;
            height: 50px;
            font-size: 18px;
            font-weight: bold;
            background-color: #4A90E2;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stButton button:hover {
            background-color: #357ABD;
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.title("🦇ArkhamMed - LLM Médico🦇")
        
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Iniciar sesión", icon="🟢"):
            st.session_state["login_mode"] = "login"

    with col2:
        if st.button("Registrarse", icon="📝"):
            st.session_state["login_mode"] = "register"

    if st.session_state["login_mode"] == "login":
        st.subheader("🔑 Iniciar sesión")
        username = st.text_input("Usuario", key="login_user", value="")
        password = st.text_input("Contraseña", type="password", key="login_pass", value="")
        login_button = st.button("Acceder")

        if login_button:
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Bienvenido, {username}!")
            else:
                st.error("Usuario o contraseña incorrectos.")
            time.sleep(2)
            st.rerun()

    elif st.session_state["login_mode"] == "register":
        st.subheader("📝 Registrarse")
        new_username = st.text_input("Nuevo usuario", key="register_user")
        new_password = st.text_input("Nueva contraseña", type="password", key="register_pass")
        repeat_new_password = st.text_input("Repite nueva contraseña", type="password", key="repeat_register_pass")
        register_button = st.button("Crear cuenta")

        if register_button:
            if new_password != repeat_new_password:
                st.error("❌ Las contraseñas no coinciden. Prueba de nuevo.")
            elif not new_username or not new_password or not repeat_new_password:
                st.error("❌ Todos los campos son obligatorios.")
            elif register_user(new_username, new_password):
                st.success("✅ Registro exitoso. Ahora puedes iniciar sesión.")
            else:
                st.error("❌ El usuario ya existe. Prueba con otro nombre.")