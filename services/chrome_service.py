from selenium import webdriver
import os
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from firebase_admin import firestore
from models.departamento import Departamento

class ChromeService():
    def __init__(self, ml_url):
        self.ML_URL = ml_url

    def start_browser(self):
        options = webdriver.ChromeOptions()
        carpeta_inicio_usuario = os.path.expanduser("~")
        ruta_usuario = os.path.join(carpeta_inicio_usuario, "AppData", "Local", "Google", "Chrome", "User Data")
        options.add_argument(f"--user-data-dir={ruta_usuario}")
        options.add_argument(f"profile-directory=Profile 11")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)


    def get_ml_departamentos(self):
        try:
            departamentos = []
            # Abre la página de Mercado Libre
            self.driver.get(self.ML_URL)

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
                    direccion = li.find_element(By.CLASS_NAME, "poly-component__location").text  # Ajusta la clase real

                    portada = li.find_element(By.CLASS_NAME, "poly-card__portada")

                    enlace = li.find_element(By.CLASS_NAME, "poly-component__title").get_attribute("href")

                    pattern = r"MLA-\d+"  # Busca "MLA-" seguido de uno o más dígitos
                    codigo = re.search(pattern, enlace).group()

                    depto = Departamento(None, codigo, titulo, direccion, precio, enlace, False, False, firestore.SERVER_TIMESTAMP, False, False)

                    departamentos.append(depto)

                except Exception as e:
                    print(f"Error procesando un elemento: {e}")
        except:
            print('error general de get_ml_departamentos')
        finally:
            self.driver.close()
            self.driver.quit()
            return departamentos

        