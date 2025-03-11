import streamlit as st
# from langchain.chains import LLMChain
# from langchain.llms.bedrock import Bedrock
# from langchain.prompts import PromptTemplate
from transformers import pipeline
from PIL import Image
import io
# import boto3
import os
import openai 

client = openai.OpenAI(api_key="sk-rZ86GerKTg0qnRkXS-NXDQ", base_url="https://litellm.dccp.pbu.dedalus.com") 

# os.environ['AWS_PROFILE'] = "Anon2148"
# bedrock_client = boto3.client(
#     service_name="bedrock-runtime",
#     region_name="us-east-1"
# )

# modelID= "anthropic.claude-v2"

# llm = Bedrock(
#     model_id=modelID,
#     client=bedrock_client,
#     model_kwargs={"max_tokens_to_sample": 2000, "temperature": 0.7}
# )

# def llm_function(language, data):
#     prompt = PromptTemplate(
#         template="You are a medical chat bot, translate {data} into {language} and respond with a medical approach",
#         input_variables=["language", "data"],
#     )
#     bedrock_chain = LLMChain(llm=llm, prompt=prompt)
#     response = bedrock_chain({'language': language, 'data': data})
#     return response['text']

# Initialize the vision model from Hugging Face
vision_model = pipeline("image-to-text", 
    model="Salesforce/blip-image-captioning-large"  # or "microsoft/git-large-coco"
)

def process_image(image_file):
    """Process an image with enhanced error handling"""
    try:
        # List of supported formats
        supported_formats = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
        
        # Check file format
        file_extension = image_file.name.lower().split('.')[-1]
        if file_extension not in supported_formats:
            return f"Unsupported image format: {file_extension}. Please use: {', '.join(supported_formats)}"
        
        # Process image
        image = Image.open(image_file)
        
        # Convert if needed
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        
        # Get image description
        result = vision_model(image)
        
        # Add basic image properties to the analysis
        width, height = image.size
        return f"""Image Analysis:
        - Size: {width}x{height}
        - Format: {file_extension.upper()}
        - Description: {result[0]['generated_text']}"""
    
    except Exception as e:
        return f"Error processing image: {str(e)}"


def process_files_and_generate_context(files):
    """Process all uploaded files and generate context"""
    context = []
    for file in files:
        file_type = file.type.split('/')[0]  # Get main file type (image, text, etc)
        
        if file_type == 'image':
            image_description = process_image(file)
            context.append(f"Image analysis of {file.name}: {image_description}")
        else:
            # Handle other file types if needed
            context.append(f"File attached: {file.name} (type: {file.type})")
    
    return "\n".join(context)


st.set_page_config(page_title="Wayne's LLM", page_icon=":bat:")

st.title("LLM Médico")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

idioma = st.selectbox("Selecciona el idioma", ["Español", "Inglés", "Francés"])

codigos_idioma = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr"
}

mensajes_error = {
    "es": "Lo sentimos, nuestro LLM no está disponible en este momento, por favor inténtelo de nuevo más tarde.",
    "en": "Sorry, our LLM is not available at the moment, please try again later.",
    "fr": "Désolé, notre LLM n'est pas disponible pour le moment, veuillez réessayer plus tard."
}


prompt = st.chat_input("Escribe tu mensaje...")

st.markdown("### Adjuntar Archivos")
archivos = st.file_uploader("Seleccionar archivos para adjuntar", accept_multiple_files=True)

st.markdown("### Historial de conversación")
for mensaje in st.session_state.chat_history:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])


if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat_history.append({"role": "user", "content": prompt})

    try:

        file_context = ""
        if archivos:
            with st.spinner('Analyzing uploaded files...'):
                file_context = process_files_and_generate_context(archivos)
                st.write("File analysis complete!")

        complete_prompt = f"""Context from uploaded files:
        {file_context}

        User question:
        {prompt}"""

        preprompt = f"Traduce la respuesta al idioma seleccionado: {idioma}. Solo da la respuesta en el idioma que te he pedido. \
        Eres un médico profesional, quiero que respondas con un vocabulario técnico y añadas información relevante a la consulta:"

        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[
                {"role": "user", "content": preprompt + complete_prompt}
            ]
        )

        respuesta_ia = response.choices[0].message.content if response.choices else ""

        if not respuesta_ia:
            respuesta_traducida = mensajes_error[codigos_idioma[idioma]]
        else:
            respuesta_traducida = respuesta_ia

    except Exception as e:
        respuesta_traducida = mensajes_error[codigos_idioma[idioma]]

    with st.chat_message("assistant"):
        st.markdown(respuesta_traducida)

    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_traducida})
