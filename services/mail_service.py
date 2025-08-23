from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class MailService():
    def __init__(self, smtp_server, smtp_port, email_usuario, email_password, destinatario='gemionicolas@gmail.com', asunto='Nuevos Departamentos publicados!'): 
        self.SMTP_SERVER = smtp_server
        self.SMTP_PORT = smtp_port
        self.EMAIL_USUARIO = email_usuario
        self.EMAIL_PASSWORD = email_password
        self.DESTINATARIO = destinatario
        self.ASUNTO = asunto

    def send_email(self, mensaje):
        msg = MIMEMultipart()
        msg["From"] = self.EMAIL_USUARIO
        msg["To"] = self.DESTINATARIO
        msg["Subject"] = self.ASUNTO

        msg.attach(MIMEText(mensaje, "html"))

        try:
            # Conectar con el servidor SMTP de Gmail
            servidor = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            servidor.starttls()  # Seguridad
            servidor.login(self.EMAIL_USUARIO, self.EMAIL_PASSWORD)
            servidor.sendmail(self.EMAIL_USUARIO, self.DESTINATARIO, msg.as_string())
            servidor.quit()

            print("Correo enviado con éxito.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

