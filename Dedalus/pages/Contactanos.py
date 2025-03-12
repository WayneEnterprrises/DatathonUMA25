import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Contactanos", page_icon=":bat:")

st.title("📩 Ayuda")
st.write("Escríbenos para cualquier duda.")

# Campo para el correo electrónico
email = st.text_input("Tu correo electrónico:", placeholder="ejemplo@email.com")

# Área de texto para escribir la consulta
mensaje = st.text_area("Tu mensaje:", placeholder="Escribe aquí tu consulta...")

# Configuración del servidor SMTP
REMITENTE = "byanicoyt@gmail.com"  # Reemplaza con tu correo
PASSWORD = "qfdq caso mfab rgki"  # Reemplaza con la contraseña de aplicación de Gmail
DESTINATARIO_ADMIN = "byanicoyt@gmail.com"  # Donde quieres recibir los mensajes

# Función para enviar correo
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

# Botón de enviar con validación
if st.button("Enviar mensaje"):
    if email and mensaje:
        # Enviar confirmación al usuario
        asunto_usuario = "Gracias por su consulta"
        cuerpo_usuario = "Hemos recibido correctamente su mensaje, le atenderemos a la mayor brevedad posible 😊. \n \nAtentamente,  ArkhamMed."
        exito_usuario = enviar_correo(email, asunto_usuario, cuerpo_usuario)

        # Enviar el mensaje de ayuda al administrador
        asunto_admin = f"Consulta de {email}"
        cuerpo_admin = f"📩 Nueva consulta de {email}:\n\n{mensaje}"
        exito_admin = enviar_correo(DESTINATARIO_ADMIN, asunto_admin, cuerpo_admin)

        # Mostrar mensaje en pantalla
        if exito_usuario and exito_admin:
            st.success("✅ Tu mensaje ha sido enviado correctamente.")
        else:
            st.error("❌ Hubo un error al enviar los correos.")
    else:
        st.warning("⚠️ Por favor, completa todos los campos antes de enviar.")
