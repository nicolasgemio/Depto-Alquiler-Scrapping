
from services.firestore_service import FireStoreService
from services.chrome_service import ChromeService
from services.mail_service import MailService
import time
from dotenv import load_dotenv
import os

firestore_service = None
chrome_service = None
mail_service = None

def __main__():
    global firestore_service, chrome_service, mail_service

    load_dotenv()

    if firestore_service is None:
        firestore_service = FireStoreService()
    
    if chrome_service is None:
        ml_url = os.getenv("MERCADOLIBRE_URL")
        arg_url = os.getenv("ARGENPROP_URL")
        chrome_service = ChromeService(ml_url, arg_url)
    
    if mail_service is None:
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        email_usuario = os.getenv("EMAIL_USUARIO")
        email_password = os.getenv("EMAIL_PASSWORD")
        mail_service = MailService(smtp_server, smtp_port, email_usuario, email_password)

    new_deptos = []
    
    departamentos = firestore_service.get_departamentos()

    chrome_service.start_browser()
    ml_departamentos = chrome_service.get_ml_departamentos()

    chrome_service.start_browser()
    arg_departamentos = chrome_service.get_arg_departamentos()

    codigos_existentes = {d.codigo for d in departamentos}

    for d in ml_departamentos:
        if d.codigo not in codigos_existentes:
            new_d = firestore_service.add_departamento(d)
            new_deptos.append(new_d)

    for d in arg_departamentos:
        if d.codigo not in codigos_existentes:
            new_d = firestore_service.add_departamento(d)
            new_deptos.append(new_d)

    mensaje = ""
    for d in new_deptos:
        mensaje += f"<p><strong>{d.codigo} - {d.titulo}</strong><br><a href='https://scarpdepto.vercel.app/departments/{ d.id }'>Ver</a></p><hr>"

    if mensaje != "":
        mail_service.send_email(mensaje)

    print('Actualización terminada')

if __name__ == "__main__":
    while True:
        __main__()
        time.sleep(900)