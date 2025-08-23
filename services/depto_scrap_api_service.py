from datetime import datetime, timezone
import requests
from models.departamento import DepartmentDto
import os

class DeptoScrapAPIService():

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

        response = requests.post(url, json=department_data)

        if response.status_code == 201:
            return response.json().get("department_id", None)
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")
    
    def get_if_is_loaded(self, search_id, department_code):
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/searches/exists/search/{search_id}/department/{department_code}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json().get('is_loaded', True), response.json().get('department_id', None)
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def create_search_department(self, search_id, department_id):
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/searches/search/{search_id}/department/{department_id}"

        response = requests.post(url)

        if response.status_code == 200:
            return response.json().get('search_department_id', None)
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def get_nonexistent_department_codes(api_url: str, codes: list[str]) -> list[str]:
        """
        Consulta el endpoint /departments/exists y retorna los códigos que no existen en la base de datos.
    
        Args:
            api_url (str): URL base de la API
            codes (list[str]): Lista de códigos a verificar
    
        Returns:
            list[str]: Lista de códigos que no existen en la base de datos
        """
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/departments/exists"
        payload = {"codes": codes}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("nonexistent_codes", [])
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")    
    
    def get_all_departments(self):
        """
        Realiza una petición GET al endpoint /all para obtener todos los departamentos.

        Returns:
            list[dict]: Lista de departamentos obtenidos del endpoint.
        Raises:
            Exception: Si la respuesta no es exitosa.
        """
        api_url = os.getenv("BASE_URI")
        url = f"{api_url}/all"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("searches", [])
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    