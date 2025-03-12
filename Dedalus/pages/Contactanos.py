import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from security.auth import check_authentication

st.set_page_config(page_title="Contactanos", page_icon=":bat:")
check_authentication()
st.title("📩 Ayuda")
st.write("Escríbenos para cualquier duda.")

email = st.text_input("Tu correo electrónico:", placeholder="ejemplo@email.com")

mensaje = st.text_area("Tu mensaje:", placeholder="Escribe aquí tu consulta...")

REMITENTE = "byanicoyt@gmail.com" 
PASSWORD = "qfdq caso mfab rgki"  
DESTINATARIO_ADMIN = "byanicoyt@gmail.com" 

def enviar_correo(destinatario, asunto, cuerpo):
    msg = MIMEMultipart()
    msg["From"] = REMITENTE
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(REMITENTE, PASSWORD)
        server.sendmail(REMITENTE, destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"❌ No se pudo enviar el correo: {str(e)}")
        return False

if st.button("Enviar mensaje"):
    if email and mensaje:
        asunto_usuario = "Gracias por su consulta"
        cuerpo_usuario = "Hemos recibido correctamente su mensaje, le atenderemos a la mayor brevedad posible 😊. \n \nAtentamente,  ArkhamMed."
        exito_usuario = enviar_correo(email, asunto_usuario, cuerpo_usuario)

        asunto_admin = f"Consulta de {email}"
        cuerpo_admin = f"📩 Nueva consulta de {email}:\n\n{mensaje}"
        exito_admin = enviar_correo(DESTINATARIO_ADMIN, asunto_admin, cuerpo_admin)

        if exito_usuario and exito_admin:
            st.success("✅ Tu mensaje ha sido enviado correctamente.")
        else:
            st.error("❌ Hubo un error al enviar los correos.")
    else:
        st.warning("⚠️ Por favor, completa todos los campos antes de enviar.")
