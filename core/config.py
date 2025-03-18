import openai
from openai import OpenAI


OPENAI_API_KEY_CLAUDE = "sk-rZ86GerKTg0qnRkXS-NXDQ"
OPENAI_BASE_URL_CLAUDE = "https://litellm.dccp.pbu.dedalus.com"


OPENAI_API_KEY_CHATGPT = "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"

client_PEDRO = OpenAI(api_key=OPENAI_API_KEY_CHATGPT)


client = openai.OpenAI(api_key=OPENAI_API_KEY_CLAUDE, base_url=OPENAI_BASE_URL_CLAUDE)





