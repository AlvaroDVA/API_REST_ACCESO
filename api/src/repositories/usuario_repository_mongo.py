from pymongo import MongoClient

from models.usuario import Usuario

class UsuarioRepostiryMongo:
    def __init__(self,collection : str, db_user : str, db_password : str):
        self.collection = collection
        print("Conectado a la base de datos de Mongo / Usuarios")
        client = MongoClient('mongodb', 27017, username=db_user, password=db_password)

        self.db = client.testdb
        self.usuarios = self.db[self.collection]

        try: self.db.command("serverStatus")
        except Exception as exception:print(exception)
        else: print("Conectado a la Base de datos de MongoDB / Usuarios")

        