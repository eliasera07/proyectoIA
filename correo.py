
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(destinatario, asunto, mensaje):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "elias2015.era@gmail.com"
    smtp_password = "sbrwwkklearuqulm"  # Reemplaza con la contraseña generada

    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain"))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, destinatario, msg.as_string())
    server.quit()

    print("Correo enviado exitosamente.")
