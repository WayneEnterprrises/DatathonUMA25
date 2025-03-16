from .config import client
import time
import json

from DB.dbInterface import *


#Este método debe llamarse al seleccionar un paciente, a modo introductorio, se le pasa la información resumen del paciente y un link de aumentación de datos.
#IDEA si Claude.puede leer páginas web subir la información a una página para no consumir tokens
def returnPatientSummary(idioma, selected_patient, userName):
    json_resumen_paciente = json_info_from_instance_class(selected_patient)
    prompt = f"""Traduce la respuesta al idioma seleccionado: {idioma}.
    Solo da la respuesta en el idioma que te he pedido.
    Eres un médico profesional, quiero que respondas con un vocabulario técnico
    y añadas información relevante a la consulta, añade enlaces de interes sobre las enfermedades que se traten en la conversacion.
    
    Debes saludar al Dr.{userName} y hacer un resumen con la información del paciente {json_resumen_paciente}.
    Termina la respuesta pidiedo al Dr. Más instrucciones para continuar
    """
    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": prompt}] ,
            stream=True  
        )
        buffer = []
        for chunk in response:
            if hasattr(chunk, "choices") and chunk.choices:
                chunk_text = chunk.choices[0].delta.content or ""
                buffer.append(chunk_text)

                # Control de latencia dinámico según la cantidad de chunks
                if len(buffer) % 5 == 0:
                    time.sleep(0.02)
                
                yield "".join(buffer)
                buffer.clear()

    except Exception as e:
        print(f"Error en la API: {e}")
        return "Lo sentimos, nuestro LLM no está disponible en este momento, por favor inténtelo más tarde."
    
    


def process_chat_message(prompt, idioma, file_context, conver_history, selected_patient):

    patient_json_info = json_info_from_instance_class(selected_patient)

    """Procesa el mensaje del usuario y genera respuesta del LLM, incluyendo los 6 CSVs automáticamente."""

    if conver_history is None:
        conver_history = []
    # Convertir info paciente a JSON legible para Claude, información resumen o completa (puede variar dependiendo del prompt)
    #patient_json_info = json_info_from_instance_class(selected_patient)
    #patient_json_all_info =  all_patient_info(selected_patient.PatientID) (int)
    #Método all_patient_info()
    
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
                    time.sleep(0.02)
                
                yield "".join(buffer)
                buffer.clear()

    except Exception as e:
        print(f"Error en la API: {e}")
        return "Lo sentimos, nuestro LLM no está disponible en este momento, por favor inténtelo más tarde."