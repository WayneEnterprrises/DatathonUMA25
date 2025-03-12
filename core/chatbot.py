from .config import client

def process_chat_message(prompt, idioma, file_context, conver_history):

    """Procesa el mensaje del usuario y genera respuesta del LLM"""

    preprompt = f"Traduce la respuesta al idioma seleccionado: {idioma}. \
    Solo da la respuesta en el idioma que te he pedido. \
    Eres un médico profesional, quiero que respondas con un vocabulario técnico \
    y añadas información relevante a la consulta:"

    complete_prompt = f"""📄 **Contexto de archivos adjuntos**:
    {file_context}

    **Pregunta del usuario**:
    {prompt}
    """
    print(conver_history)
    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": preprompt + complete_prompt + "".join([f"**Historial de conversación**:\n{msg['content']}\n" for msg in conver_history])}],
        )

        respuesta_ia = response.choices[0].message.content if response.choices else ""
        return respuesta_ia or "Lo sentimos, no pudimos generar una respuesta en este momento."

    except Exception:
        print()
        return "Lo sentimos, nuestro LLM no está disponible en este momento, por favor inténtelo más tarde."
