import openai
from transformers import pipeline

OPENAI_API_KEY = "sk-rZ86GerKTg0qnRkXS-NXDQ"
OPENAI_BASE_URL = "https://litellm.dccp.pbu.dedalus.com"

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

vision_model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
