from openai import OpenAI

OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

def añadirEnlances_ChatGPT(promptInput):

    prompt = f"""Eres un agente especializado en proveer artículos de pubMed (https://pubmed.ncbi.nlm.nih.gov/). Tu función es proveer enlaces
    relevantes a artículos para este texto generado por un asistente médico de un doctor: {promptInput}. 
    """

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "assistant",
            "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content

prompt = """ El paciente Juan Pérez recibió los siguientes medicamentos durante su hospitalización por neumonía adquirida en la comunidad, complicada por su EPOC preexistente:

Ceftriaxona: 2 g IV cada 24 horas Motivo: Antibiótico de amplio espectro para tratar la infección bacteriana causante de la neumonía. La ceftriaxona es eficaz contra muchos patógenos respiratorios comunes.

Azitromicina: 500 mg VO cada 24 horas Motivo: Antibiótico macrólido que complementa la cobertura antibiótica, especialmente eficaz contra patógenos atípicos como Mycoplasma pneumoniae y Legionella. También posee efectos antiinflamatorios que pueden ser beneficiosos en pacientes con EPOC.

Salbutamol: 5 mg nebulizado cada 6 horas Motivo: Broncodilatador de acción rápida para aliviar la broncoconstricción y mejorar la función respiratoria, especialmente importante en pacientes con EPOC y neumonía.

Paracetamol: 1 g VO cada 8 horas Motivo: Analgésico y antipirético para controlar la fiebre y aliviar el malestar general asociado a la infección.

Tiotropio: Inhalado (dosis no especificada) Motivo: Broncodilatador de acción prolongada indicado para el manejo a largo plazo de la EPOC. Se optimizó su uso al alta para mejorar el control de la enfermedad de base.

La combinación de estos medicamentos está dirigida a:

Tratar la infección respiratoria (antibióticos)
Mejorar la función pulmonar (broncodilatadores)
Controlar los síntomas (antipiréticos)
Manejar la EPOC subyacente (broncodilatadores de mantenimiento)
Es importante destacar que el manejo farmacológico se complementó con otras medidas terapéuticas como oxigenoterapia, fisioterapia respiratoria y movilización temprana."""



print(añadirEnlances_ChatGPT(prompt))
