from datetime import datetime, timezone
import requests
from models.departamento import DepartmentDto
import os
from logger_config import configure_logger


class DeptoScrapAPIService():

    def __init__(self):
        self.logger = configure_logger("scrapping-app.service", propagate=True)

    def create_department(self, department: DepartmentDto):
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/departments/create"

        department_data = {
            "title": department.title,
            "link": department.link,
            "address": department.address,
            "neighborhood": department.neighborhood,
            "photo_url": department.photo_url,
            "price": department.price,
            "price_currency": department.price_currency,
            "publication_date": datetime.now(timezone.utc).isoformat(),
            "create_date": datetime.now(timezone.utc).isoformat(),
            "department_code": department.department_code
        }
        self.logger.info(f"Creando departamento: code={department.department_code} title={department.title}")
        try:
            response = requests.post(url, json=department_data)
            if response.status_code == 201:
                dept_id = response.json().get("department_id", None)
                self.logger.info(f"Departamento creado correctamente (department_id={dept_id})")
                return dept_id
            else:
                self.logger.error(f"Fallo al crear el departamento (code={department.department_code}): {response.status_code} - {response.text}")
                raise Exception(f"Error {response.status_code}: {response.text}")
        except requests.RequestException as ex:
            self.logger.error(f"Excepción al crear departamento (code={department.department_code}): {ex}")
            raise
    
    def get_not_loaded(self, search_id, codes: list[str]) -> list[DepartmentDto]:
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/searches/notloaded/search/{search_id}"
        payload = {"codes": codes}
        self.logger.info(f"Consultando departamentos no cargados en búsqueda {search_id}: total_codes={len(codes)}")
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                departments_data = response.json().get("departments", [])
                departments = [DepartmentDto(
                    dept["department_code"],
                    dept["title"],
                    dept.get("address", ""),
                    dept.get("price", 0),
                    dept.get("link", ""),
                    datetime.now(timezone.utc)
                ) for dept in departments_data]
                self.logger.info(f"Departamentos no cargados encontrados: {len(departments)}")
                return departments
            else:
                self.logger.warning(f"Fallo al consultar departamentos no cargados. search_id={search_id}, status={response.status_code}")
                raise Exception(f"Error {response.status_code}: {response.text}")
        except requests.RequestException as ex:
            self.logger.error(f"Excepción en get_not_loaded: search_id={search_id}, ex={ex}")
            raise
        
    def get_if_is_loaded(self, search_id, department_code):
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/searches/exists/search/{search_id}/department/{department_code}"
        self.logger.info(f"Verificando si departamento ya está cargado: search_id={search_id}, department_code={department_code}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                is_loaded = response.json().get('is_loaded', True)
                dep_id = response.json().get('department_id', None)
                self.logger.info(f"Resultado de verificación: is_loaded={is_loaded}, department_id={dep_id}")
                return is_loaded, dep_id
            else:
                self.logger.warning(f"No se pudo verificar existencia. search_id={search_id}, department_code={department_code}, status={response.status_code}")
                raise Exception(f"Error {response.status_code}: {response.text}")
        except requests.RequestException as ex:
            self.logger.error(f"Excepción en get_if_is_loaded: search_id={search_id}, department_code={department_code}, ex={ex}")
            raise

    def create_search_department(self, search_id, department_id):
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/searches/search/{search_id}/department/{department_id}"
        self.logger.info(f"Asociando departamento {department_id} a búsqueda {search_id}")
        try:
            response = requests.post(url)
            if response.status_code == 200:
                assoc_id = response.json().get('search_department_id', None)
                self.logger.info(f"Asociación creada correctamente (search_department_id={assoc_id})")
                return assoc_id
            else:
                self.logger.warning(f"Fallo al asociar. search_id={search_id}, department_id={department_id} status={response.status_code}")
                raise Exception(f"Error {response.status_code}: {response.text}")
        except requests.RequestException as ex:
            self.logger.error(f"Excepción en create_search_department: search_id={search_id}, department_id={department_id}, ex={ex}")
            raise

    def get_nonexistent_department_codes(self, codes: list[str]) -> list[str]:
        """
        Consulta el endpoint /departments/exists y retorna los códigos que no existen en la base de datos.

        Args:
            codes (list[str]): Lista de códigos a verificar

        Returns:
            list[str]: Lista de códigos que no existen en la base de datos
        """
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/departments/exists"
        payload = {"codes": codes}
        self.logger.info(f"Verificando existencia múltiple de códigos de departamento: total_codes={len(codes)}")
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                nonexistent = response.json().get("nonexistent_codes", [])
                self.logger.info(f"Códigos inexistentes encontrados: {nonexistent}")
                return nonexistent
            else:
                self.logger.warning(f"Fallo en verificación múltiple de códigos. Status={response.status_code}")
                raise Exception(f"Error {response.status_code}: {response.text}")
        except requests.RequestException as ex:
            self.logger.error(f"Excepción en get_nonexistent_department_codes: ex={ex}")
            raise    
    
    def get_all_searches(self):
        """
        Realiza una petición GET al endpoint /all para obtener todas las búsquedas.

        Returns:
            list[dict]: Lista de búsquedas obtenidos del endpoint.
        Raises:
            Exception: Si la respuesta no es exitosa.
        """
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/all"
        self.logger.info(f"Consultando todos los búsquedas..." )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                searches = response.json().get("searches", [])
                self.logger.info(f"Búsquedas recibidas: {len(searches)}.")
                return searches
            else:
                self.logger.warning(f"Fallo al obtener lista de búsquedas. Status={response.status_code}")
                raise Exception(f"Error {response.status_code}: {response.text}")
        except requests.RequestException as ex:
            self.logger.error(f"Excepción en get_all_searches: ex={ex}")
            raise

    