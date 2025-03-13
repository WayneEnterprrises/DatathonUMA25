import streamlit as st
from core.image_processing import process_image
from core.chatbots import process_chat_message
from security.auth import check_authentication
from DB.db import get_patients, add_patient, save_chat_message, load_chat_history
import time

st.set_page_config(page_title="Welcome to Bruce!!", page_icon=":bat:")

# 🚀 Asegurar que solo los usuarios autenticados puedan acceder
check_authentication()

username = st.session_state["username"]

st.title("Presentamos a Bruce!!")

# 📌 Seleccionar Paciente o Agregar Nuevo
st.markdown("### Selecciona un paciente")

patients = get_patients(username)
patient_names = [p.name for p in patients]
patient_names.append("➕ Agregar Nuevo Paciente")  # Opción para agregar paciente

selected_patient_name = st.selectbox("Selecciona un paciente", patient_names)

if selected_patient_name == "➕ Agregar Nuevo Paciente":
    new_patient_name = st.text_input("Nombre del nuevo paciente")
    if st.button("Guardar Paciente"):
        if new_patient_name:
            add_patient(username, new_patient_name)
            st.rerun()  # Recargar la página para reflejar cambios
else:
    selected_patient = next(p for p in patients if p.name == selected_patient_name)

     # 📌 Evitar duplicación del historial
    if "chat_history" not in st.session_state or st.session_state["selected_patient"] != selected_patient.id:
        st.session_state["chat_history"] = []  # Resetear historial antes de cargar nuevos mensajes
        chat_history = load_chat_history(selected_patient.id)
        
        # Evitar agregar mensajes repetidos
        unique_messages = set()
        for chat in chat_history:
            msg_tuple = (chat.role, chat.message)  # Convertir en tupla para evitar duplicados
            if msg_tuple not in unique_messages:
                st.session_state["chat_history"].append({"role": chat.role, "content": chat.message})
                unique_messages.add(msg_tuple)
        
        st.session_state["selected_patient"] = selected_patient.id

    # 📌 Selector de idioma
    idioma = st.selectbox("Selecciona el idioma", ["Español", "Inglés", "Francés"])

    # 📂 Adjuntar archivos
    st.markdown("### Adjunta archivos a Bruce")
    archivos = st.file_uploader("Seleccionar archivos para adjuntar", accept_multiple_files=True)

    # 📌 Mostrar el historial de conversación
    st.markdown("### Preguntale a Bruce lo que necesites saber")
    for mensaje in st.session_state.chat_history:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # 📌 Entrada del usuario
    prompt = st.chat_input("Pregunta a Bruce sobre algo que necesites saber de tus pacientes")

    if prompt:
        save_chat_message(selected_patient.id, "user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state["chat_history"].append({"role": "user", "content": prompt})

        file_context = ""
        if archivos:
            with st.spinner('🔍 Analizando archivos...'):
                file_context = "\n".join([process_image(file) for file in archivos])

        with st.chat_message("assistant"):
            response_container = st.empty()

            # 📌 Pasar el historial del chat como contexto al modelo
            response_stream = process_chat_message(prompt,idioma, file_context,None,st.session_state.chat_history)
            full_response = ""
            # 🔄 Desparticionar el mensaje y mostrarlo en tiempo real
            for chunk in response_stream:
                full_response += chunk
                response_container.markdown(full_response + "▌")
                time.sleep(0.05)

            response_container.markdown(full_response)

        save_chat_message(selected_patient.id, "assistant", full_response)

        st.session_state["chat_history"].append({"role": "assistant", "content": full_response})
