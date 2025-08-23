from datetime import datetime, timezone
import requests
import os

class MercadolibreService():

    def get_url(self, filters_dict):
        ml_url = ml_url = os.getenv("MERCADOLIBRE_URL")
         # Ambientes
        ambientes = filters_dict.get("ambiente", [])
        if len(ambientes) > 0:
            ml_url += self.get_ambientes_filter(ambientes)

        # Dormitorios
        dormitorios = filters_dict.get("dormit", [])
        if len(dormitorios) > 0:
            ml_url += self.get_dormitorios_filters(dormitorios)

        # Ciudad
        ciudades = filters_dict.get('ciudad', [])
        if len(ciudades) > 0:
            ml_url += self.get_ciudad_filters(ciudades)

        # Barrios
        filtros_barrios = filters_dict.get('barrio', [])
        if len(filtros_barrios) > 0:
            ml_url += self.get_barrio_filter(filtros_barrios) + '/'

        # Precios
        min_price_filters = filters_dict.get("min_price", [])
        max_price_filters = filters_dict.get("max_price", [])
        if len(min_price_filters) > 0 or len(max_price_filters) > 0:
            ml_url += self.get_precio_filters(min_price_filters, max_price_filters)

        # Metros cuadrados
        min_m_cuad_filters = filters_dict.get("min_m_cuad", [])
        max_m_cuad_filters = filters_dict.get("max_m_cuad", [])
        if len(min_m_cuad_filters) > 0 or len(max_m_cuad_filters) > 0:
            ml_url += self.get_m_cuadrados_filter(min_m_cuad_filters, max_m_cuad_filters)
       
        # Publicado hoy
        ml_url += self.get_publicado_hoy()

        return ml_url


    def get_barrio_filter(self, filters_list):
            return '-o-'.join([barrio.filter_value for barrio in filters_list])
    
    def get_precio_filters(self, min_price_filters, max_price_filters):
        min_price = min_price_filters[0].filter_value if min_price_filters else "0"
        max_price = max_price_filters[0].filter_value if max_price_filters else "0"
        
        price_range_str = f"_PriceRange_{min_price}ARS-{max_price}ARS"

        if price_range_str != '':
            return f'{price_range_str}'
        return ''
    
    def get_publicado_hoy(self) -> str:
        return '_PublishedToday_YES'
    
    def get_m_cuadrados_filter(self, min_m_cuadrado_filters, max_m_cuadrado_filters):
        min_m_cuadrado = min_m_cuadrado_filters[0].filter_value if min_m_cuadrado_filters else "*"
        max_m_cuadrado = max_m_cuadrado_filters[0].filter_value if max_m_cuadrado_filters else "*"
        return f'_COVERED*AREA_{min_m_cuadrado}-{max_m_cuadrado}'
    
    def get_ciudad_filters(self, ciudades):
         return '-'.join(ciudades[0].filter_value.lower().split(' ')) + '/'
           
    def get_ambientes_filter(self, ambientes_filters):
        ambiente = ambientes_filters[0].filter_value
        return f'{ambiente}-ambiente/' if ambiente == '1' else f'{ambiente}-ambientes/'
    
    def get_dormitorios_filters(self, dormitorios_filters):
        dormitorio = dormitorios_filters[0].filter_value

        if dormitorio == '0':
             return 'sin-dormitorios/'
        elif dormitorio == '1':
             return '1-dormitorio/'
        else:
            return f'{dormitorio}-dormitorios/'