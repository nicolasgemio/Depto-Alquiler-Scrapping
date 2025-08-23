from models.departamento import Departamento
from datetime import datetime, timezone
import requests
from models.departamento import DepartmentDto
import os

class Department_service():

    def get_getpertments_to_insert(self, departments: list[DepartmentDto]):
       for department in departments:
           #Llamar a endpoint que dice si cada departamento existe.
           pass
           
    