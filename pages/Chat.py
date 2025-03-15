import streamlit as st
from core.image_processing import process_image
from core.chatbots import process_chat_message, returnPatientSummary
from security.auth import check_authentication
from DB.dbInterface import get_all_patients, load_chat_history, save_chat_message
import time

st.set_page_config(page_title="Welcome to Bruce!!", page_icon=":bat:")

# 🚀 Asegurar que solo los usuarios autenticados puedan acceder
check_authentication()

username = st.session_state["username"]

st.title("Presentamos a Bruce!!")

# 📌 Seleccionar Paciente
st.markdown("### Selecciona un paciente")
patients = get_all_patients()
patient_names = [p.Nombre for p in patients]

selected_patient_name = st.selectbox(
    label="Selecciona un paciente",
    label_visibility="hidden",
    options=patient_names,
    index=None,
    placeholder="Selecciona un paciente disponible"
)

if selected_patient_name:
    # 📌 Selector de idioma
    idioma = st.selectbox("Selecciona el idioma", ["Español", "Inglés", "Francés"])

    # 📂 Adjuntar archivos
    st.markdown("### Adjunta archivos a Bruce")
    archivos = st.file_uploader("Seleccionar archivos para adjuntar", accept_multiple_files=True)

    historial_chat = st.checkbox("Quiero recordar el historial de chat")

    selected_patient = next(p for p in patients if p.Nombre == selected_patient_name)

    # 📌 Cargar historial de conversación si el paciente cambia
    if "selected_patient_id" not in st.session_state or st.session_state["selected_patient_id"] != selected_patient.PacienteID:
        chat_entry = load_chat_history(selected_patient.PacienteID)
        st.session_state["chat_history"] = [{"role": entry.role, "content": entry.message} for entry in chat_entry]
        st.session_state["selected_patient_id"] = selected_patient.PacienteID  # ✅ Guardamos el paciente actual

    # 📌 Mostrar el historial como un chat real
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 📌 Entrada del usuario
    prompt = st.chat_input("Pregunta a Bruce sobre algo que necesites saber de tus pacientes")

    # ✅ Si el historial está vacío, mostrar un mensaje de bienvenida
    if not st.session_state["chat_history"]:
        with st.chat_message("assistant"):
            welcome_message = returnPatientSummary(idioma, selected_patient, username)
            welcome_container = st.empty()
            full_welcome = ""
            for chunk in welcome_message:
                full_welcome += chunk
                welcome_container.markdown(full_welcome + "▌")
                time.sleep(0.02)

            welcome_container.markdown(full_welcome)
            save_chat_message(selected_patient.PacienteID, "assistant", full_welcome)
            st.session_state["chat_history"].append({"role": "assistant", "content": full_welcome})

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        # ✅ Agregar el nuevo mensaje correctamente
        st.session_state["chat_history"].append({"role": "user", "content": prompt})

        file_context = ""
        if archivos:
            with st.spinner('🔍 Analizando archivos...'):
                file_context = "\n".join([process_image(file) for file in archivos])

        with st.chat_message("assistant"):
            response_container = st.empty()

            # ✅ Enviar historial si el usuario seleccionó la opción
            history_context = st.session_state["chat_history"] if historial_chat else None

            response_stream = process_chat_message(prompt, idioma, file_context, history_context, selected_patient)

            if response_stream:
                full_response = ""
                for chunk in response_stream:
                    full_response += chunk
                    response_container.markdown(full_response + "▌")
                    time.sleep(0.05)

                response_container.markdown(full_response)
                st.session_state["chat_history"].append({"role": "assistant", "content": full_response})

            else:
                response_container.markdown("Nuestro LLM no se encuentra disponible en estos momentos, lamentamos los inconvenientes.")
                st.session_state["chat_history"].append({"role": "assistant", "content": "Nuestro LLM no se encuentra disponible en estos momentos."})
