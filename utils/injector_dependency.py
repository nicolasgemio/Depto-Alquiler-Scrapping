import os
from services.chrome_service import ChromeService
from services.mail_service import MailService
from services.depto_scrap_api_service import DeptoScrapAPIService
from services.mercadolibre_service import MercadolibreService
from services.argenprop_service import ArgenpropService

class DependencyInjector:
    def __init__(self):
        self._chrome_service = None
        self._mail_service = None
        self._depto_scrap_api_service = None
        self._mercadolibre_service = None
        self._argenprop_service = None

    def get_chrome_service(self):
        if not self._chrome_service:
            self._chrome_service = ChromeService(os.getenv("MERCADOLIBRE_URL"), os.getenv("ARGENPROP_URL"))
        return self._chrome_service

    def get_mail_service(self):
        if not self._mail_service:
            self._mail_service = MailService(
                os.getenv("SMTP_SERVER"),
                os.getenv("SMTP_PORT"),
                os.getenv("EMAIL_USUARIO"),
                os.getenv("EMAIL_PASSWORD"),
            )
        return self._mail_service

    def get_depto_scrap_api_service(self):
        if not self._depto_scrap_api_service:
            self._depto_scrap_api_service = DeptoScrapAPIService()
        return self._depto_scrap_api_service

    def get_mercadolibre_service(self):
        if not self._mercadolibre_service:
            self._mercadolibre_service = MercadolibreService()
        return self._mercadolibre_service

    def get_argenprop_service(self):
        if not self._argenprop_service:
            self._argenprop_service = ArgenpropService()
        return self._argenprop_service

# Luego en main.py:
# from injector_dependency import DependencyInjector
# injector = DependencyInjector()
# chrome_service = injector.get_chrome_service()
# mail_service = injector.get_mail_service()
# etc.