from models.departamento import DepartmentDto
import logging
class FireStoreService():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = None

    def get_departamentos(self):
        if self.db is None:
            self.conect_database()

        lista_departamentos = []
        deptos = self.db.collection("deptos").stream()

        for d in deptos:
            detpo_id = d.id
            depto_data = d.to_dict()
            departamento = DepartmentDto(
                detpo_id,
                depto_data.get('codigo'),
                depto_data.get('titulo'),
                depto_data.get('direccion'),
                depto_data.get('precio'),
                depto_data.get('link'),
                depto_data.get('rejected_n'),
                depto_data.get('rejected_a'),
                depto_data.get('creacion'),
                depto_data.get('favorito_n'),
                depto_data.get('favorito_a'),
                depto_data.get('comentario_n'),
                depto_data.get('comentario_a')
                )
            lista_departamentos.append(departamento)

        return lista_departamentos
    
    def add_departamento(self, departamento):
        if self.db is None:
            self.conect_database()  # Asegurar que la DB está conectada

        # Crear un diccionario con los datos del departamento
        departamento_data = {
            "codigo": departamento.codigo,
            "titulo": departamento.titulo,
            "direccion": departamento.direccion,
            "precio": departamento.precio,
            "link": departamento.link,
            "rejected_n": departamento.rejected_n,
            "rejected_a": departamento.rejected_a,
            "creacion": departamento.creacion,
            "favorito_n": departamento.favorito_n,
            "favorito_a": departamento.favorito_a,
            "comentario_n": departamento.comentario_n,
            "comentario_a": departamento.comentario_a
        }

        # Agregar el documento a la colección "deptos"
        nuevo_doc_ref = self.db.collection("deptos").add(departamento_data)
        departamento.id = nuevo_doc_ref[1].id
        self.logger.info(f'Departamento agregado con ID: {nuevo_doc_ref[1].id}')

        return departamento


