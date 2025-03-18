import json
import re
from .chatbots import generar_info_adicional
from .config import client, client_PEDRO
from pymed import PubMed
# 📌 Texto de prueba
prompt  = """El paciente Carlos García, de 22 años, ingresó en la UCI el 20/09/2023 por los siguientes motivos:

Polidipsia
Poliuria
Vómitos
Confusión
Estos síntomas, junto con la deshidratación severa y la respiración de Kussmaul observadas al ingreso, son indicativos de una cetoacidosis diabética (CAD) en el contexto de una diabetes mellitus tipo 1 mal controlada.

Los tratamientos implementados para abordar esta emergencia metabólica fueron:

Fluidoterapia intravenosa: Se administró suero fisiológico 1000 ml por vía intravenosa rápida para corregir la deshidratación severa.

Insulinoterapia:

Insulina regular en perfusión intravenosa continua a 0.1 U/kg/h para reducir la hiperglucemia y la cetosis.
Insulina glargina 20 U subcutánea nocturna como terapia basal.
Corrección de electrolitos:

Cloruro de potasio 20 mEq intravenoso cada 4 horas para prevenir la hipopotasemia.
Bicarbonato de sodio 50 mEq intravenoso en dosis única para corregir la acidosis metabólica severa (pH 7.1).
Monitorización estrecha: Se colocó un catéter venoso central para facilitar la administración de fluidos y medicamentos, así como para el control hemodinámico en la UCI.

Evaluación continua: Se realizaron controles seriados de glucemia, electrolitos y gases arteriales para ajustar el tratamiento.

Manejo de complicaciones: Se realizó una radiografía de tórax para descartar infecciones pulmonares como factor precipitante de la CAD.

Este abordaje terapéutico multifacético está diseñado para corregir la hiperglucemia, la cetoacidosis, los desequilibrios electrolíticos y la deshidratación, que son las alteraciones fisiopatológicas fundamentales en la CAD. El objetivo es estabilizar al paciente y prevenir las complicaciones potencialmente mortales asociadas a esta condición."""

import json
import re
from pymed import PubMed
from .config import client, client_PEDRO

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
def obtener_info_pubmed(palabras_clave, max_results=4):
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

print(generar_info_adicional(prompt))

"""'
palabras_clave = ["diabetes mellitus", "cetoacidosis", "insulinoterapia"]
resultados = obtener_info_pubmed(palabras_clave, max_results=5)

print("🔎 **Resultados de PubMed:**")
for resultado in resultados:
    print(resultado)
    """