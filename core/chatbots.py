import re

from pymed import PubMed
from .config import client, client_PEDRO
import time
import json
import plotly.express as px
from DB.dbInterface import *
from openai import OpenAI


# Función para analizar si el prompt del usuario requiere estadísticas
# Se consulta a Claude para determinar si la pregunta necesita gráficos o tablas
def analyze_prompt_for_statistics(prompt):
    """
    Usa Claude para analizar si el prompt necesita generación de estadísticas.
    """
    analysis_prompt = f"""
    Analiza la siguiente consulta y responde con 'SI' si requiere datos estadísticos, 
    como gráficos, tablas o estadísticas generales. Si no se necesitan estadísticas, responde 'NO'.
    Recuerda que cualquier dato que sea un porcentaje o que pueda traducirse a un porcentaje se considera estadistico.
    **IMPORTANTE**
    Responde unicamente con SI o NO nada mas.
    Consulta: {prompt}
    """
    
    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        analysis_result = response.choices[0].message.content.strip()
        print(analysis_result)
        return analysis_result.upper() == "SI"
    except Exception as e:
        print(f"Error en el análisis del prompt: {e}")
        return False

# Función para generar datos estadísticos con base en la consulta del usuario
# Si Claude detecta que se requieren estadísticas, esta función genera datos estructurados en JSON
def generate_statistics_data(prompt):
    """
    Usa Claude para generar datos estadísticos con base en la pregunta del usuario.
    """
    
    
    stats_prompt = f"""
     Devuelve una lista de datos numéricos estructurados de la siguiente forma:
    {{ "categorias": ["Categoria1(Unidad1)", "Categoria2(Unidad2)"], "valores": [10, 20] }}
    Asegúrate de devolver solo un JSON válido sin explicaciones adicionales.
    Extrae la información para rellenar la lista de este texto:
    {prompt}
    
    Asegúrate de devolver solo un JSON válido sin explicaciones adicionales.
    """
    
    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": stats_prompt}]
        )
        
        stats_text = response.choices[0].message.content.strip()
        print("Respuesta de Claude para estadísticas:", stats_text)  # Debugging
        
        if not stats_text:
            raise ValueError("Claude no devolvió una respuesta válida para las estadísticas.")
        
        stats_data = json.loads(stats_text)
        return stats_data
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return None
    except Exception as e:
        print(f"Error en la generación de estadísticas: {e}")
        return None
    


    
# Función para generar un gráfico interactivo con Plotly a partir de los datos obtenidos
def plot_statistics(stats_data):
    """
    Genera un gráfico interactivo con Plotly basado en los datos obtenidos.
    """
    if not stats_data or "categorias" not in stats_data or "valores" not in stats_data:
        return None
    
    fig = px.bar(x=stats_data["categorias"], y=stats_data["valores"],
                 labels={'x': 'Categorías', 'y': 'Valores'},
                 title="Datos Estadísticos Generados",
                 color=stats_data["valores"],
                 color_continuous_scale="viridis")
    
    return fig

#def añadirEnlances_ChatGPT(promptInput):

 #   prompt = f"""Eres un agente especializado en proveer artículos de pubMed (https://pubmed.ncbi.nlm.nih.gov/). Tu función es proveer enlaces
  #  relevantes a artículos para este texto generado por un asistente médico de un doctor: {promptInput}, 
   # """

    #completion = client_PEDRO.chat.completions.create(
       # model="gpt-4o",
       # messages=[
       #     {
     ##       "role": "assistant",
     #       "content": prompt,
    #        }
  #      ]
#    )   
   # response_text = completion.choices[0].message.content if completion.choices else "No se encontraron enlaces relevantes."
    #print(response_text)
   # return response_text
    

    #Este agente ya devuelve los enlaces sin errores a pubMed
    #Hace falta añadirlo a continuación de process_chat_message en el prompt
# ✅ Función combinada para generar y limpiar palabras clave
# 📌 Función para generar y limpiar palabras clave
def generar_y_limpiar_palabras_clave(promptInput):
    """
    Genera palabras clave médicas en base al prompt de entrada y limpia la salida
    para asegurar que sea un JSON válido.
    """
    prompt = f"""Eres un agente especializado en generar palabras clave médicas relevantes 
    para búsquedas en bases de datos como PubMed. 
    Tu tarea es devolver únicamente palabras clave relevantes en formato JSON para el siguiente texto , elige solo las 5 palabras clave más relevantes y devuelvelas en INGLÉS:
    
    {promptInput}
    
    **Formato de respuesta JSON esperado:** 
    {{
      "palabras_clave": ["término1", "término2", "término3"]
    }}
    
    No devuelvas explicaciones, solo el JSON válido.
    """

    try:
        completion = client_PEDRO.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = completion.choices[0].message.content.strip()
        return limpiar_json(response_text)  # Llamamos a limpiar_json antes de cargar el JSON
    except Exception as e:
        print(f"Error en la API de generación de palabras clave: {e}")
        return {"palabras_clave": []}

# ✅ Función para limpiar JSON
def limpiar_json(response_text):
    """
    Extrae solo el bloque JSON de un texto con posibles caracteres adicionales.
    """
    try:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            json_text = match.group(0)
            return json.loads(json_text)  # Intentar parsear JSON
        else:
            raise ValueError("No se encontró un JSON válido en la respuesta.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return {"palabras_clave": []}

# ✅ Función para buscar en PubMed usando pyMed
def obtener_info_pubmed(palabras_clave, max_results=10):
    """
    Realiza una consulta a PubMed usando pymed con las palabras clave y devuelve títulos y enlaces a artículos relevantes.
    """
    pubmed = PubMed(tool="MedicalAgent", email="thedrakeishere12@gmail.com")  # Configuración de pyMed
    print(palabras_clave)
    query = " OR ".join(palabras_clave)  # Construcción de la query combinando palabras clave con OR
    results = pubmed.query(query, max_results=max_results)  # Ejecutar la consulta

    resultados = []
    for article in results:
        title = article.title if article.title else "Título no disponible"
   
    # 📌 Extraer solo el primer PubMed ID válido
        pubmed_ids = article.pubmed_id.split(";") if article.pubmed_id else []
        pubmed_ids = [id.strip() for id in pubmed_ids if id.strip().isdigit()]  # Filtrar solo IDs numéricos

        if pubmed_ids:  # Verificar que haya al menos un ID válido
            pubmed_id = pubmed_ids[0]  # Tomar solo el primer ID válido
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}"
            resultados.append(f"- [{title}]({url})")

    return resultados if resultados else ["No se encontraron artículos relevantes en PubMed."]

# ✅ Función principal que integra el generador de palabras clave con la búsqueda en PubMed
def generar_info_adicional(promptInput):
    """
    Genera palabras clave médicas en base al prompt de entrada y obtiene información relevante de PubMed.
    """
    palabras_clave = generar_y_limpiar_palabras_clave(promptInput)  # Obtener palabras clave
    if not palabras_clave["palabras_clave"]:
        return "No se encontraron términos relevantes."

    # Usar palabras clave para obtener datos de PubMed
    info_pubmed = obtener_info_pubmed(palabras_clave["palabras_clave"])

    # Construcción del texto final basado en la información obtenida
    texto_info = "**📚 Información relevante encontrada:**\n\n"

    if info_pubmed:
        texto_info += "🔎 **PubMed:**\n" + "\n".join(info_pubmed) + "\n\n"

    return texto_info if info_pubmed else "No se encontró información relevante en PubMed."


#Este método debe llamarse al seleccionar un paciente, a modo introductorio, se le pasa la información resumen del paciente y un link de aumentación de datos.
#IDEA si Claude.puede leer páginas web subir la información a una página para no consumir tokens
def returnPatientSummary(idioma, selected_patient, userName):
    json_resumen_paciente = json_info_from_instance_class(selected_patient)
    prompt = f"""Traduce la respuesta al idioma seleccionado: {idioma}.
    Solo da la respuesta en el idioma que te he pedido.
    Eres un médico profesional, quiero que respondas con un vocabulario técnico
    y añadas información relevante a la consulta.
    
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
    
    


def process_chat_message(prompt, idioma, conver_history, selected_patient, userName):

    patient_json_info = all_patient_info(selected_patient.PacienteID)

    """Procesa el mensaje del usuario y genera respuesta del LLM, incluyendo los 6 CSVs automáticamente."""

    if conver_history is None:
        conver_history = []
    # Convertir info paciente a JSON legible para Claude, información resumen o completa (puede variar dependiendo del prompt)
    #patient_json_info = json_info_from_instance_class(selected_patient)
    #patient_json_all_info =  all_patient_info(selected_patient.PatientID) (int)
    #Método all_patient_info()
    
    preprompt = f"""Traduce la respuesta al idioma seleccionado: {idioma}.
    Solo da la respuesta en el idioma que te he pedido.
    Eres un asistente de médico profesional ayudando al Dr. {userName}, y eres parte de un sistema más grande en el que otro agente se
    encargará de generar enlaces y otro de realizar las gráficas. No digas nada sobre que no puedes generar gráficas o enlaces estás serán añadidas por el otro agente.
    
    Quiero que respondas con un vocabulario técnico
    y añadas información relevante a la consulta.

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
    