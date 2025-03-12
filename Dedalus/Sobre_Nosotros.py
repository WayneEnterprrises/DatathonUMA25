import streamlit as st
import time
from security.auth import register_user, authenticate_user

st.set_page_config(page_title="Bienvenido a ArkhamMed", page_icon=":bat:", layout="centered")

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

if not st.session_state["authenticated"]:

    st.title("🦇ArkhamMed - LLM Médico🦇")

    st.markdown(
        """
        <h3 style='text-align: center; font-weight: bold;'>🦇Bienvenido a ArkhamMed🦇</h3>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🟢 Iniciar sesión"):
            st.session_state["login_mode"] = "login"

    with col2:
        if st.button("📝 Registrarse"):
            st.session_state["login_mode"] = "register"

    if st.session_state["login_mode"] == "login":
        st.subheader("🔑 Iniciar sesión")
        username = st.text_input("Usuario", key="login_user")
        password = st.text_input("Contraseña", type="password", key="login_pass")
        login_button = st.button("Acceder")

        if login_button:
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Bienvenido, {username}!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

    elif st.session_state["login_mode"] == "register":
        st.subheader("📝 Registrarse")
        new_username = st.text_input("Nuevo usuario", key="register_user")
        new_password = st.text_input("Nueva contraseña", type="password", key="register_pass")
        register_button = st.button("Crear cuenta")

        if register_button:
            if register_user(new_username, new_password):
                st.success("✅ Registro exitoso. Ahora puedes iniciar sesión.")
                st.session_state["login_mode"] = "login"
            else:
                st.error("❌ El usuario ya existe. Prueba con otro nombre.")

    st.stop()  # Bloquear la carga de la página hasta que inicie sesión


st.title("Presentación del Equipo")
st.write(f"Bienvenido {st.session_state['username']} al equipo ArkhamMed de la Universidad de Málaga")

st.image("assets/logoDatathon.png", caption="Arkham Analytics", use_column_width=True)

st.markdown("<h2 style='text-align: center; font-weight: bold;'>Conócenos</h2>", unsafe_allow_html=True)

equipo = [
    {
        "nombre": "Ángel Nicolás Escaño López",
        "github": "https://github.com/JustBeWell",
        "linkedin": "https://www.linkedin.com/in/angel-nicolas-escaño-lopez-32031426b/",
    },
    {
        "nombre": "José Canto Peral",
        "github": "https://github.com/Anon2148",
        "linkedin": "https://www.linkedin.com/in/jose-c-ln/",
    },
    {
        "nombre": "Diego Sicre Cortizo",
        "github": "https://github.com/DiegoSicre",
        "linkedin": "https://www.linkedin.com/in/diego-sicre-cortizo-b1897b233/",
    }
]

for miembro in equipo:
    st.markdown(
        f"""
        <h2 style="text-align: center;">{miembro['nombre']}</h2>
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <a href="{miembro['github']}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="40" style="margin-right: 10px;">
            </a>
            <a href="{miembro['linkedin']}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="40" style="margin-left: 10px;">
            </a>
        </div>
        <hr>
        """,
        unsafe_allow_html=True
    )
