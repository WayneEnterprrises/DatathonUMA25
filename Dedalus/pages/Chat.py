import streamlit as st
from llm.image_processing import process_image
from llm.chatbot import process_chat_message

st.set_page_config(page_title="ArkhamMed LLM", page_icon=":bat:")

st.title("LLM Médico")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

idioma = st.selectbox("Selecciona el idioma", ["Español", "Inglés", "Francés"])

# 📂 Selector de archivos (debajo del chat)
st.markdown("### Adjuntar Archivos")
archivos = st.file_uploader("Seleccionar archivos para adjuntar", accept_multiple_files=True)

# Historial de conversación
st.markdown("### Historial de conversación")
for mensaje in st.session_state.chat_history:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu mensaje...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Analizar archivos si los hay
    file_context = ""
    if archivos:
        with st.spinner('🔍 Analizando archivos...'):
            file_context = "\n".join([process_image(file) for file in archivos])

    # Generar respuesta del chatbot
    respuesta_ia = process_chat_message(prompt, idioma, file_context)

    with st.chat_message("assistant"):
        st.markdown(respuesta_ia)

    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_ia})
