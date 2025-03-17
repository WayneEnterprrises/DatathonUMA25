import time
import json
import openai

# Configuration
OPENAI_API_KEY = "sk-rZ86GerKTg0qnRkXS-NXDQ"
OPENAI_BASE_URL = "https://litellm.dccp.pbu.dedalus.com"

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

# Prompt
prompt = f"""Devuelveme este mensaje eliminando las url que no estén activas:

Guía de práctica clínica para el manejo del ictus isquémico agudo (Sociedad Española de Neurología): https://www.sen.es/pdf/2014/GUIA_ICTUS_2014.pdf

Manejo de la hipertensión en el ictus agudo (Revista Española de Cardiología): https://www.revespcardiol.org/es-manejo-hipertension-arterial-el-ictus-articulo-S0300893218301131

Rehabilitación del ictus (Sociedad Española de Rehabilitación y Medicina Física): https://www.sermef.es/wp-content/uploads/2016/06/sermef_manual_ictus.pdf

Manejo de la diabetes en pacientes hospitalizados (Sociedad Española de Endocrinología y Nutrición): https://www.seen.es/ModulGEX/workspace/publico/modulos/web/docs/apartados/1034/160620_105727_7128864936.pdf

"""

import openai # openai v1.0.0+
client = openai.OpenAI(api_key=OPENAI_API_KEY,base_url=OPENAI_BASE_URL) # set proxy to base_url
# request sent to model set on litellm proxy, `litellm --model`
response = client.chat.completions.create(model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0", messages = [
    {
        "role": "user",
        "content": prompt
    }
])
 
print(response) # print response