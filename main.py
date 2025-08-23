
from services.firestore_service import FireStoreService
from services.chrome_service import ChromeService
from services.mail_service import MailService
from services.depto_scrap_api_service import DeptoScrapAPIService
from services.mercadolibre_service import MercadolibreService
from services.argenprop_service import ArgenpropService
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List
from models.search import Search
from dtos.department_mail_dto import DepartmentMailDto
import json
import logging

os.makedirs("logs", exist_ok=True)
# Config básica: stdout + archivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),                     # Jenkins lo muestra en consola
        logging.FileHandler("logs/app.log", "a", "utf-8")  # Guarda histórico
    ]
)

logger = logging.getLogger(__name__)

firestore_service = None
chrome_service = None
mail_service = None
depto_scrap_api_service = None
mercadolibre_service = None
argenprop_service = None

def parse_searches_response(searches_raw) -> List[Search]:
    """
    Parsea la respuesta del endpoint /all y devuelve una lista de instancias Search.
    """
    # Si los elementos están doblemente serializados como string, deserializa:
    searches = []
    for s in searches_raw:
        if isinstance(s, str):
            s = json.loads(s)
        searches.append(Search.from_dict(s))
    return searches

def __main__():
    global firestore_service, chrome_service, mail_service, depto_scrap_api_service, mercadolibre_service, argenprop_service

    load_dotenv(override=False)

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

    if depto_scrap_api_service is None:
        depto_scrap_api_service = DeptoScrapAPIService()

    if mercadolibre_service is None:
        mercadolibre_service = MercadolibreService()

    if argenprop_service is None:
        argenprop_service = ArgenpropService()

    searches = depto_scrap_api_service.get_all_departments()
    searches_mapped = parse_searches_response(searches)
    
    for search in searches_mapped:
        filters_dict = {}
        for f in search.search_filters:
            filters_dict.setdefault(f.name, []).append(f)

        ml_url = mercadolibre_service.get_url(filters_dict)
        arg_url = argenprop_service.get_url(filters_dict)
        #MERCADOLIBRE_URL="https://inmuebles.mercadolibre.com.ar/alquiler/capital-federal/belgrano-o-palermo-o-villa-crespo-o-recoleta-o-las-canitas/_PriceRange_600000ARS-850000ARS_PublishedToday_YES_COVERED*AREA_50-*_NoIndex_True_True_55-*_YES_NoIndex#applied_filter_id%3DCOVERED_AREA%26applied_filter_name%3DSuperficie+cubierta%26applied_filter_order%3D8%26applied_value_id%3D50-*%26applied_value_name%3D50-*%26applied_value_order%3D5%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue"
        
        new_deptos = []
        new_search_departments = []

        chrome_service.start_browser()
        ml_departamentos = chrome_service.get_ml_departamentos(ml_url)

        chrome_service.start_browser()
        arg_departamentos = chrome_service.get_arg_departamentos(arg_url)

        if len(ml_departamentos):
            ml_codes = [department.department_code for department in ml_departamentos]
            ml_codes_to_add = depto_scrap_api_service.get_nonexistent_department_codes(ml_codes)
    
        if len(arg_departamentos):
            arg_codes = [department.department_code for department in arg_departamentos]
            arg_codes_to_add = depto_scrap_api_service.get_nonexistent_department_codes(arg_codes)

        for d in ml_departamentos:
            is_loaded = False
            if d.department_code in ml_codes_to_add:
                department_id = depto_scrap_api_service.create_department(d)
                d.department_id = department_id
                new_deptos.append(d)
            else:
                is_loaded, department_id = depto_scrap_api_service.get_if_is_loaded(search.search_id, d.department_code)

            if not is_loaded:
                search_department_id = depto_scrap_api_service.create_search_department(search.search_id, department_id)
                new_search_departments.append(DepartmentMailDto(d.title, d.department_code, search_department_id))


        for d in arg_departamentos:
            is_loaded = False
            if d.department_code in arg_codes_to_add:
                department_id = depto_scrap_api_service.create_department(d)
                d.department_id = department_id
                new_deptos.append(d)
            else:
                is_loaded = depto_scrap_api_service.get_if_is_loaded(search.search_id, d.department_code)

            if not is_loaded:
                search_department_id = depto_scrap_api_service.create_search_department(search.search_id, department_id)
                new_search_departments.append(DepartmentMailDto(d.title, d.department_code, search_department_id))


        mensaje = ""
        for department_mail in new_search_departments:
            mensaje += f"<p><strong>{department_mail.code} - {department_mail.title}</strong><br><a href='{os.getenv('BASE_URI')}/departments/{department_mail.search_department_id}'>Ver</a></p><hr>"

        if mensaje != "":
            mail_service.send_email(mensaje)

        ahora = datetime.now()
        formato = ahora.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f'Actualización terminada, {len(new_search_departments)} departamentos cargados en la búsqueda {search.search_id}')

if __name__ == "__main__":
    try:
        __main__()
    except Exception as e:
       logger.error("Error en la ejecución principal: %s", e)