from flask import jsonify
from pymongo import MongoClient
from typing import Iterable, Optional
import models.Nota as Nota
import uuid
from datetime import datetime

class NotasRepositoryMongo:
    def __init__(self,):
        self.client = MongoClient('mongodb://root:example@mongodb:27017/')
        self.db = self.client["Notas"]
        self.notas_collection = self.db["notas"]

    def crear_nota(self, titulo, texto, isTerminado, isImportante, email_usuario):

        fecha_actual = datetime.now()
        nota = {
            "_id": uuid.uuid4().hex,
            "titulo": titulo,
            "texto": texto,
            "fechaCreacion": fecha_actual.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "fechaUltimaModifcacion": fecha_actual.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "isTerminado": isTerminado,
            "isImportante": isImportante,
            "email_usuario": email_usuario
        }
        self.notas_collection.insert_one(nota)
        return nota["_id"]

    def obtener_nota_por_id(self, nota_id, usuario_email):
        return self.notas_collection.find_one({"_id": nota_id, "email_usuario": usuario_email})

    def obtener_notas_por_usuario(self, email_usuario):
        return list(self.notas_collection.find({"email_usuario": email_usuario}))

    def actualizar_nota(self, nota_id, titulo=None, texto=None, isTerminado=None, isImportante=None):
        update_data = {"fechaUltimaModifcacion": datetime.now()}
        if titulo:
            update_data["titulo"] = titulo
        if texto:
            update_data["texto"] = texto
        if isTerminado is not None:
            update_data["isTerminado"] = isTerminado
        if isImportante is not None:
            update_data["isImportante"] = isImportante

        self.notas_collection.update_one({"_id": nota_id}, {"$set": update_data})

    def borrar_nota(self, nota_id, usuario_email):
        nota = self.notas_collection.find_one({"_id": nota_id, "email_usuario": usuario_email})
        if nota:
            self.notas_collection.delete_one({"_id": nota_id})
            return True  
        else:
            return False  

