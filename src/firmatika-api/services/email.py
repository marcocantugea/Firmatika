import os
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail
import smtplib
from email.mime.text import MIMEText
import traceback


load_dotenv()

def enviar_codigo_verificacion(email: str, codigo: str, url_verificacion: str = None):
    if url_verificacion:
        mensaje = f"Tu código de verificación es: {codigo}\nVerifica tu identidad aquí: {url_verificacion}"
    else:
        mensaje = f"Tu código de verificación es: {codigo}"
    
    msg = MIMEText(mensaje)
    msg["Subject"] = "Verificación Firmatika"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = email

    try:
        with smtplib.SMTP(os.getenv("MAILTRAP_HOST"), int(os.getenv("MAILTRAP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("MAILTRAP_USER"), os.getenv("MAILTRAP_PASS"))
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        traceback.print_exc()