from openai import OpenAI

OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

def añadirEnlances_ChatGPT(promptInput):

    prompt = f"""Un agente LLM ha generado está respuesta: {promptInput}, 
    añade enlaces de fuentes reputadas en formato https:// de interes sobre las enfermedades que se traten en la conversacion 
    y NO MODIFIQUES EL CONTENIDO ORIGINAL verificando que las páginas siguen activas (no hay errores 404 o pone pageNotFound),
    mandame solo lo que iría después del mensaje original"""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "assistant",
            "content": prompt
            }
        ]
    )

    print(completion.choices[0].message.content)

añadirEnlances_ChatGPT("""Le saludo cordialmente y procedo a presentarle el resumen del caso clínico del paciente Juan Pérez:

Varón de 68 años, ingresado en el Servicio de Neumología el 01/05/2023 por cuadro de fiebre elevada y tos productiva. El diagnóstico principal corresponde al código CIE-10 233604007. Como antecedentes relevantes, destaca enfermedad pulmonar obstructiva crónica (EPOC) asociada a tabaquismo crónico e hipertensión arterial. No se reportan alergias conocidas.

Al ingreso, el paciente se encontraba hemodinámicamente estable, pero presentaba disnea de intensidad moderada. La sintomatología actual, sumada a sus condiciones preexistentes, sugiere un posible episodio de exacerbación de EPOC, aunque se requiere confirmación diagnóstica.

Quedo a la espera de sus instrucciones para proceder con la evaluación adicional y el plan terapéutico más apropiado para este caso. ¿Desea que realicemos alguna prueba complementaria o que iniciemos algún tratamiento específico?""")