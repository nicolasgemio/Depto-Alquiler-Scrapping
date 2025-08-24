from dotenv import load_dotenv
import os
import json
import logging
from typing import List
from models.search import Search
from dtos.department_mail_dto import DepartmentMailDto
from utils.injector_dependency import DependencyInjector

class App():
    def __init__(self):
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

        self.logger = logging.getLogger(__name__)

        load_dotenv(override=False)

        injector = DependencyInjector()
        self.chrome_service = injector.get_chrome_service()
        self.mail_service = injector.get_mail_service()
        self.depto_scrap_api_service = injector.get_depto_scrap_api_service()
        self.mercadolibre_service = injector.get_mercadolibre_service()
        self.argenprop_service = injector.get_argenprop_service()

    def parse_searches_response(self, searches_raw) -> List[Search]:
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

    def get_departments(self, departments, search_id):
        new_search_departments = []
        codes_to_add = []

        if len(departments):
            codes = [department.department_code for department in departments]
            codes_to_add = self.depto_scrap_api_service.get_nonexistent_department_codes(codes)

        for d in departments:
            if d.department_code in codes_to_add:
                department_id = self.depto_scrap_api_service.create_department(d)
                d.department_id = department_id
 
        codes_to_search = [d.department_code for d in departments if d.department_code not in codes_to_add]
        if len(codes_to_search) > 0:
            departments_not_loaded = self.depto_scrap_api_service.get_not_loaded(search_id, codes_to_search)

            for d in departments_not_loaded:
                search_department_id = self.depto_scrap_api_service.create_search_department(search_id, d.department_id)
                new_search_departments.append(DepartmentMailDto(d.department_code, d.title, search_department_id))

        return new_search_departments

    def scrap_search(self, search: Search):
        filters_dict = {}
        for f in search.search_filters:
            filters_dict.setdefault(f.name, []).append(f)

        ml_url = self.mercadolibre_service.get_url(filters_dict)
        arg_url = self.argenprop_service.get_url(filters_dict)
            
        new_search_departments = []

        self.chrome_service.start_browser()
        ml_departamentos = self.chrome_service.get_ml_departamentos(ml_url)

        self.chrome_service.start_browser()
        arg_departamentos = self.chrome_service.get_arg_departamentos(arg_url)

        new_search_departments = self.get_departments(ml_departamentos, search.search_id)
        new_search_departments += self.get_departments(arg_departamentos, search.search_id)
        
        mensaje = ""
        for department_mail in new_search_departments:
            mensaje += f"<p><strong>{department_mail.code} - {department_mail.title}</strong><br><a href='{os.getenv('BASE_URI')}/departments/{department_mail.search_department_id}'>Ver</a></p><hr>"

        if mensaje:
            self.mail_service.send_email(mensaje)

        self.logger.info(f'Actualización terminada, {len(new_search_departments)} departamentos cargados en la búsqueda {search.search_id}')

    def main(self):
        searches = self.depto_scrap_api_service.get_all_departments()
        searches_mapped = self.parse_searches_response(searches)

        for search in searches_mapped:
            self.scrap_search(search)

if __name__ == "__main__":
    try:
        app = App()
        app.main()
    except Exception as e:
        app.logger.error("Error en la ejecución principal: %s", e)