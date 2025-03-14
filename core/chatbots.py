from .config import client
import time
import json

from DB.dbInterface import *

def process_chat_message(prompt, idioma, file_context, conver_history, selected_patient):
    """Procesa el mensaje del usuario y genera respuesta del LLM, incluyendo los 6 CSVs automáticamente."""
    
    if conver_history is None:
        conver_history = []
    # Convertir info paciente a JSON legible para Claude
    patient_json_info = json_info_from_instance_class(selected_patient)

    #En selected_patient tenemos una instancia del objeto ORM resumen pacientes del paciente seleccionado, una fila
    
    #La idea sería poder mandarle a claude toda la información de los pacientes
    # Limitar la cantidad de mensajes en la memoria
    
    preprompt = f"""Traduce la respuesta al idioma seleccionado: {idioma}.
    Solo da la respuesta en el idioma que te he pedido.
    Eres un médico profesional, quiero que respondas con un vocabulario técnico
    y añadas información relevante a la consulta, añade enlaces de interes sobre las enfermedades que se traten en la conversacion.
    

    📄 **Contexto de archivos adjuntos**:
    {file_context}

    📊 **Datos estructurados de la información clínica del paciente al ingresar en el centro de salud**:
    {patient_json_info}

    Debes comprender la información proporcionada para poder responder correctamente a las preguntas
    que se te impone, puedes cumplimentar tus observaciones con tablas estadisticas sobre las enfermedades 
    comentadas.

    **Pregunta del usuario**:
    {prompt}
    """

    # Convertir historial a JSON estructurado
    history_messages = [{"role": "user", "content": msg["content"]} for msg in conver_history]
    """
    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": preprompt}] + history_messages,
            stream=True  
        )

        buffer = []
        for chunk in response:
            if hasattr(chunk, "choices") and chunk.choices:
                chunk_text = chunk.choices[0].delta.content or ""
                buffer.append(chunk_text)

                # Control de latencia dinámico según la cantidad de chunks
                if len(buffer) % 5 == 0:
                    time.sleep(0.05)
                
                yield "".join(buffer)
                buffer.clear()

    except Exception as e:
        print(f"Error en la API: {e}")
        return "Lo sentimos, nuestro LLM no está disponible en este momento, por favor inténtelo más tarde."
    """