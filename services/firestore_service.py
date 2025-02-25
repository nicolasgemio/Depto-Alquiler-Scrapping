import firebase_admin
from firebase_admin import credentials, firestore
from models.departamento import Departamento
class FireStoreService():

    def __init__(self):
        self.db = None

    def conect_database(self):
        # Ruta al archivo JSON de tus credenciales
        cred = credentials.Certificate('scrapping-deptos-firebase-adminsdk-fbsvc-6339a65ce9.json')

        # Inicializa la app de Firebase con las credenciales
        firebase_admin.initialize_app(cred)

        # Conéctate a Firestore
        self.db = firestore.client()

    def get_departamentos(self):
        if self.db is None:
            self.conect_database()

        lista_departamentos = []
        deptos = self.db.collection("deptos").stream()

        for d in deptos:
            detpo_id = d.id
            depto_data = d.to_dict()
            departamento = Departamento(
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
                depto_data.get('favorito_a')
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
            "favorito_a": departamento.favorito_a
        }

        # Agregar el documento a la colección "deptos"
        nuevo_doc_ref = self.db.collection("deptos").add(departamento_data)

        print(f"Departamento agregado con ID: {nuevo_doc_ref[1].id}")


