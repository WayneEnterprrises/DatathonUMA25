import openai
from openai import OpenAI


OPENAI_API_KEY_CLAUDE = "<Your-API-Key>"
OPENAI_BASE_URL_CLAUDE = "<Base_url>"


OPENAI_API_KEY_CHATGPT = "<Your-ChatGPT-API-Key>"

client_PEDRO = OpenAI(api_key=OPENAI_API_KEY_CHATGPT)


client = openai.OpenAI(api_key=OPENAI_API_KEY_CLAUDE, base_url=OPENAI_BASE_URL_CLAUDE)





