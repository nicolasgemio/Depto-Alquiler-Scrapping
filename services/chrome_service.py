from selenium import webdriver
import os
import re
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from models.departamento import DepartmentDto
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from datetime import datetime, timezone
from selenium.webdriver.chrome.service import Service
from typing import List
import logging

class ChromeService():
    def __init__(self, ml_url, arg_url):
        self.logger = logging.getLogger(__name__)
        self.MERCADOLIBRE_URL = ml_url
        self.ARGENPROP_URL = arg_url

    def start_browser(self):
        options = webdriver.ChromeOptions()
        carpeta_inicio_usuario = os.path.expanduser("~")
        if platform.system() == "Windows":
            binary = None  # Chrome normal en Windows
        else:
            # Para Linux / Raspberry Pi OS
            binary_candidates = ["/usr/bin/chromium-browser", "/usr/bin/chromium"]
            binary = next((p for p in binary_candidates if Path(p).exists()), None)

        # Chromedriver instalado por apt
        driver_path_candidates = ["/usr/bin/chromedriver", "/snap/bin/chromedriver"]
        driver_path = next((p for p in driver_path_candidates if Path(p).exists()), None)

        opts = Options()
        if binary:
            opts.binary_location = binary

        options.add_argument("--headless=new")  # Usar el nuevo modo headless recomendado
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")

        # Especifica la ruta al ChromeDriver si no está en el PATH
        # service = Service(executable_path="C:/ruta/a/chromedriver.exe")
        service = Service(executable_path=driver_path)  # Si chromedriver está en el PATH

        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 5)


    def get_ml_departamentos(self, url) -> List[DepartmentDto]:
        try:
            departamentos = []
            # Abre la página de Mercado Libre
            self.driver.get(url)

            # Espera algunos segundos para que la página cargue (opcional)
            self.driver.implicitly_wait(10)

            # Realiza las acciones que necesites aquí (por ejemplo, buscar algo, navegar, etc.)
            elementos = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ol.ui-search-layout.ui-search-layout--grid > li"))
            )

            for li in elementos:
                try:
                    titulo = li.find_element(By.CLASS_NAME, "poly-component__title").text  # Ajusta la clase real
                    precio = li.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text  # Ajusta la clase real
                    precio_parsed = int(str(precio).replace('.', '').replace(',', ''))
                    direccion = li.find_element(By.CLASS_NAME, "poly-component__location").text  # Ajusta la clase real

                    # portada = li.find_element(By.CLASS_NAME, "poly-card__portada")

                    enlace = li.find_element(By.CLASS_NAME, "poly-component__title").get_attribute("href")

                    pattern = r"MLA-\d+"  # Busca "MLA-" seguido de uno o más dígitos
                    codigo = re.search(pattern, enlace).group()

                    depto = DepartmentDto(codigo, titulo, direccion, precio_parsed, enlace, datetime.now(timezone.utc))

                    departamentos.append(depto)

                except Exception as e:
                    self.logger.error(f'Error procesando un elemento: {e}')
        except e:
            self.logger.error(f'error general de get_ml_departamentos: {e}')
        finally:
            self.driver.close()
            self.driver.quit()
            return departamentos

    def get_arg_departamentos(self, url):
        try:
            departamentos = []
            
            # Abre la página de Argenprop
            self.driver.get(url)

            # Espera algunos segundos para que la página cargue (opcional)
            self.driver.implicitly_wait(10)

            # Realiza las acciones que necesites aquí (por ejemplo, buscar algo, navegar, etc.)
            elementos = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.listing__items > div.listing__item"))
            )

            for div in elementos:
                try:
                    titulo = div.find_element(By.CLASS_NAME, "card__title").text  # Ajusta la clase real
                    precio = div.find_element(By.CLASS_NAME, "card__price").text  # Ajusta la clase real
                    precio_parsed = int(str(precio).replace('.', '').replace(',', '').replace('$', '').split('+')[0].strip())
                    direccion = div.find_element(By.CLASS_NAME, "card__address").text  # Ajusta la clase real

                    enlace = div.find_element(By.CLASS_NAME, "card").get_attribute("href")

                    id = div.get_attribute("id")
                    codigo = f"ARG-{id}"
                    depto = DepartmentDto(codigo, titulo, direccion, precio_parsed, enlace, datetime.now(timezone.utc))

                    departamentos.append(depto)

                except Exception as e:
                    self.logger.error(f'Error procesando un elemento: {e}')

        except Exception as e:
            self.logger.error(f'Error procesando un elemento: {e}')
        finally:
            self.driver.close()
            self.driver.quit()
            return departamentos