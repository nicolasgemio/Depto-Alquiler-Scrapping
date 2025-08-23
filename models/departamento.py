import uuid

class DepartmentDto():
    def __init__(self, codigo, titulo, direccion, precio, link, creacion):
        self.department_id = uuid.uuid4()
        self.title = titulo
        self.link = link
        self.address = direccion
        self.neighborhood = ""
        self.photo_url = ""
        self.price = precio
        self.price_currency = ""
        self.publication_date = None
        self.create_date = creacion
        self.department_code = codigo
