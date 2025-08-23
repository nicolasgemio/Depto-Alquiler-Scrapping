from datetime import datetime, timezone
import requests
import os

class ArgenpropService():
    #ARGENPROP_URL="https://www.argenprop.com/departamentos/alquiler/belgrano-o-las-canitas-o-palermo-o-recoleta-asu-o-villa-crespo/pesos-600000-850000?desde-50-m2-cubiertos"
    def get_url(self, filters_dict):
        arg_url = arg_url = os.getenv("ARGENPROP_URL")

        # Ciudad
        # ciudades = filters_dict.get('ciudad', [])
        # if len(ciudades) > 0:
        #     arg_url += self.get_ciudad_filters(ciudades)

        # Barrios
        filtros_barrios = filters_dict.get('barrio', [])
        if len(filtros_barrios) > 0:
            arg_url += self.get_barrio_filter(filtros_barrios) + '/'

        # Ambientes
        ambientes = filters_dict.get("ambiente", [])
        if len(ambientes) > 0:
            arg_url += self.get_ambientes_filter(ambientes)

        # Dormitorios
        dormitorios = filters_dict.get("dormit", [])
        if len(dormitorios) > 0:
            arg_url += self.get_dormitorios_filters(dormitorios)

        # Precios
        min_price_filters = filters_dict.get("min_price", [])
        max_price_filters = filters_dict.get("max_price", [])
        if len(min_price_filters) > 0 or len(max_price_filters) > 0:
            arg_url += self.get_precio_filters(min_price_filters, max_price_filters)

        # Publicado hoy
        arg_url += self.get_publicado_hoy()

        # Metros cuadrados
        min_m_cuad_filters = filters_dict.get("min_m_cuad", [])
        max_m_cuad_filters = filters_dict.get("max_m_cuad", [])
        if len(min_m_cuad_filters) > 0 or len(max_m_cuad_filters) > 0:
            arg_url += self.get_m_cuadrados_filter(min_m_cuad_filters, max_m_cuad_filters)


       


        return arg_url


    def get_barrio_filter(self, filters_list):
            return '-o-'.join([barrio.filter_value for barrio in filters_list])
    
    def get_precio_filters(self, min_price_filters, max_price_filters):

        if len(min_price_filters) > 0 and len(max_price_filters) > 0:
            return f'pesos-{min_price_filters[0].filter_value}-{max_price_filters[0].filter_value}'
        
        elif len(min_price_filters) > 0:
            return f'pesos-desde-{min_price_filters[0].filter_value}'
        else:
            return f'pesos-hasta-{max_price_filters[0].filter_value}'

    def get_publicado_hoy(self) -> str:
        return '?orden-masnuevos'
    
    def get_m_cuadrados_filter(self, min_m_cuadrado_filters, max_m_cuadrado_filters):
        if len(min_m_cuadrado_filters) > 0 and len(max_m_cuadrado_filters):
            return f'{min_m_cuadrado_filters[0].filter_value}-{max_m_cuadrado_filters[0].filter_value}-m2-cubiertos'
        elif len(min_m_cuadrado_filters) > 0:
            return f'&desde-{min_m_cuadrado_filters[0].filter_value}-m2-cubiertos'
        else:
            return f'&hasta-{max_m_cuadrado_filters[0].filter_value}-m2-cubiertos'
    
    def get_ciudad_filters(self, ciudades):
         return '-'.join(ciudades[0].filter_value.lower().split(' ')) + '/'
           
    def get_ambientes_filter(self, ambientes_filters):
        ambiente = ambientes_filters[0].filter_value
        return f'monoambiente/' if ambiente == '1' else f'{ambiente}-ambientes/'
    
    def get_dormitorios_filters(self, dormitorios_filters):
        dormitorio = dormitorios_filters[0].filter_value

        if dormitorio == '1':
             return '1-dormitorio/'
        else:
            return f'{dormitorio}-dormitorios/'