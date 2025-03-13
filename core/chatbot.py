from .config import client
import time

def process_chat_message(chat_history, prompt, idioma, file_context):
    """🔄 Genera la respuesta del LLM con memoria del chat en tiempo real"""
    
    preprompt = f"Este es el historial del chat en curso:\n{chat_history}\n\n"
    preprompt += f"Traduce la respuesta al idioma seleccionado: {idioma}. \
    Solo da la respuesta en el idioma que te he pedido. \
    Eres un médico profesional, quiero que respondas con un vocabulario técnico \
    y añadas información relevante a la consulta."

    complete_prompt = f"""📄 **Contexto de archivos adjuntos**:
    {file_context}

    **Pregunta del usuario**:
    {prompt}
    """

    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": preprompt + complete_prompt}],
            stream=True  
        )

        #Particiono el mensaje para poder pasarlo como chunks para que el modelo lo procese en tiempo real
        for chunk in response:
            if hasattr(chunk, "choices") and chunk.choices:
                yield chunk.choices[0].delta.content or ""
            time.sleep(0.04)  

    except Exception:
        yield "Lo sentimos, nuestro LLM no está disponible en este momento, por favor inténtelo más tarde."
