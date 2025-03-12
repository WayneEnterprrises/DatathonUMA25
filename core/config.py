import openai
from transformers import pipeline

# Configuración de API Keys
OPENAI_API_KEY = "sk-rZ86GerKTg0qnRkXS-NXDQ"
OPENAI_BASE_URL = "https://litellm.dccp.pbu.dedalus.com"

# Inicializar cliente de OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

# Inicializar modelo de visión de Hugging Face
vision_model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
