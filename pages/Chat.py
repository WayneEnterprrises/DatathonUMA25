import streamlit as st
from core.image_processing import process_image
from core.chatbots import process_chat_message, generar_info_adicional, returnPatientSummary,analyze_prompt_for_statistics,generate_statistics_data,plot_statistics
from security.auth import check_authentication
from DB.dbInterface import get_all_patients, load_chat_history, save_chat_message
import time

st.set_page_config(page_title="Welcome to Bruce!!", page_icon=":bat:")

# 🚀 Asegurar que solo los usuarios autenticados puedan acceder
check_authentication()

username = st.session_state["username"]

st.title("🦇Bruce's LLM🦇")

# 📌 Seleccionar Paciente
st.markdown("### Selecciona al paciente con el que quieras trabajar")
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
    idioma = st.selectbox("Selecciona el idioma en el que quieras tu respuesta", ["Español", "Inglés", "Francés"])

    # 📂 Adjuntar archivos
    st.markdown("### Adjunta archivos a Bruce")
    archivos = st.file_uploader("Seleccionar archivos para adjuntar", accept_multiple_files=True)

    selected_patient = next(p for p in patients if p.Nombre == selected_patient_name)

    # 📌 Borrar el historial de conversación si el paciente cambia
    if "selected_patient_id" not in st.session_state or st.session_state["selected_patient_id"] != selected_patient.PacienteID:
        st.session_state["chat_history"] = []
        st.session_state["selected_patient_id"] = selected_patient.PacienteID  # ✅ Guardamos el paciente actual

# 📌 Mostrar el historial como un chat real
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 📌 Entrada del usuario
    prompt = st.chat_input("Pregunta a Bruce sobre algo que necesites saber de tu pacientes")

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
        
        needs_statistics = analyze_prompt_for_statistics(prompt)
        print(needs_statistics)
        stats_image = None
        if "stats_images" not in st.session_state:
            st.session_state["stats_images"] = []
            
        with st.chat_message("assistant"):
            response_container = st.empty()

            #Cargar el historial de toda la conversación actual
            history_context = st.session_state["chat_history"]

            response_stream = process_chat_message(prompt, idioma, file_context, history_context, selected_patient, username)

            if response_stream:
                full_response = ""
                full_response_without_links = ""
                for chunk in response_stream:
                    full_response += chunk
                    full_response_without_links += chunk
                    response_container.markdown(full_response + "▌")
                    time.sleep(0.05)
                
                #with st.spinner("🔍 Buscando enlaces de interés..."):
                 #   extra_info = añadirEnlances_ChatGPT(full_response)
                  #  full_response = full_response + extra_info if extra_info else full_response
                
                with st.spinner("🔍 Buscando información médica relevante..."):
                    extra_info = generar_info_adicional(full_response)
                    full_response += f"\n\n{extra_info}" if extra_info else ""

                response_container.markdown(full_response)
                st.session_state["chat_history"].append({"role": "assistant", "content": full_response})
                print(full_response_without_links)
                if needs_statistics:
                    with st.spinner("🚀Generando estadísticas..."):
                        stats_data = generate_statistics_data(full_response_without_links)
                        stats_image = plot_statistics(stats_data)
                        if stats_image:
                            st.plotly_chart(stats_image, use_container_width=True)
                            st.session_state["stats_images"].append(stats_image)  # Agregar la nueva imagen a la lista

            else:
                response_container.markdown("Nuestro LLM no se encuentra disponible en estos momentos, lamentamos los inconvenientes.")
                st.session_state["chat_history"].append({"role": "assistant", "content": "Nuestro LLM no se encuentra disponible en estos momentos."})
