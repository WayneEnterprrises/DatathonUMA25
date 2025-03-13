from .config import client
import time
import json
import pandas as pd
import os

#Estos archivos se cargan siempre, ya que constituyen la base de conocimiento
#Se guardan los paths relativos para que sean accesibles
CSV_FILES = [
    "data/resumen_evolucion.csv",
    "data/resumen_lab_iniciales.csv",
    "data/resumen_medicacion.csv",
    "data/resumen_notas.csv",
    "data/resumen_pacientes.csv",
    "data/resumen_procedimientos.csv"
]

def load_csv_to_json(csv_path):
    """Carga un CSV y lo convierte en un JSON legible por el LLM, manejando errores y delimitadores."""
    try:
        # Detectar delimitador automáticamente
        with open(csv_path, "r", encoding="utf-8") as f:
            first_line = f.readline()
            delimiter = "," if "," in first_line else ";"

        # Leer CSV con delimitador detectado y manejar errores
        df = pd.read_csv(csv_path, delimiter=delimiter, on_bad_lines="skip", encoding="utf-8")

        return df.to_dict(orient="records")  # Convertir a JSON lista de diccionarios
    
    except pd.errors.ParserError as e:
        print(f"❌ Error de parsing en {csv_path}: {e}")
        return []
    except Exception as e:
        print(f"❌ Error cargando {csv_path}: {e}")
        return []


def load_all_csvs():
    """Carga los 6 CSVs esenciales y los estructura en un diccionario."""
    csv_data = {}
    for file_path in CSV_FILES:
        if not isinstance(file_path, str):  # Validar que no sea una lista
            print(f"⚠️ Advertencia: Se esperaba una ruta de archivo, pero se recibió un {type(file_path)}: {file_path}")
            continue

        file_name = os.path.basename(file_path).replace(".csv", "")
        csv_data[file_name] = load_csv_to_json(file_path)

    return csv_data

def process_chat_message(prompt, idioma, file_context, additional_csv_path=None, conver_history=[], max_history=100):
    """Procesa el mensaje del usuario y genera respuesta del LLM, incluyendo los 6 CSVs automáticamente."""
    
    # Cargar automáticamente los 6 CSVs fijos
    csv_data = load_all_csvs()
    #print(csv_data) Funciona
    # Cargar CSV adicional si se proporciona
    if additional_csv_path:
        csv_data["archivo_adicional"] = load_csv_to_json(additional_csv_path)

    # Convertir CSVs a JSON legible para Claude
    csv_json = json.dumps(csv_data, indent=2)
    #print(csv_json) Funciona
    # Limitar la cantidad de mensajes en la memoria
    trimmed_history = conver_history[-max_history:] # De momemento no quiero limitar el historial, ya que no ralentiza la aplicación


    preprompt = f"""Traduce la respuesta al idioma seleccionado: {idioma}.
    Solo da la respuesta en el idioma que te he pedido.
    Eres un médico profesional, quiero que respondas con un vocabulario técnico
    y añadas información relevante a la consulta.
    

    📄 **Contexto de archivos adjuntos**:
    {file_context}

    📊 **Datos estructurados de los CSVs médicos**:
    {csv_json}

    **Pregunta del usuario**:
    {prompt}
    """

    # Convertir historial a JSON estructurado
    history_messages = [{"role": "user", "content": msg["content"]} for msg in trimmed_history]

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