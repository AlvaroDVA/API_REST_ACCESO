import datetime
import asyncio
from flask import Flask, jsonify, request, abort
from pymongo.errors import PyMongoError
from bson import ObjectId
import os
from dotenv import dotenv_values

import asyncio

from repositories.notas_repository_mongo import NotasRepositoryMongo
from repositories.usuario_repository_mongo import UsuarioRepostiryMongo
from repositories.notas_repository_maria import NotasRepositoryMaria

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

DB_TYPE = "mongodb"

if DB_TYPE == "mongodb":
    nota_repo = NotasRepositoryMongo()
elif DB_TYPE == "mariadb":
    nota_repo = NotasRepositoryMaria()

from flask import Flask, jsonify, request

# Asegúrate de importar tus clases y módulos necesarios aquí
from pymongo.errors import PyMongoError

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# Obtener todas las notas del usuario  
@app.route('/notas', methods=['GET'])
def obtenerNotas():
    try:
        idc = request.headers.get('email')
        passw = request.headers.get('pass')
        if passw is None or idc is None:
            return jsonify({"message": "No hay credenciales"})
        
        print("Obtener Notas")
        notas = nota_repo.obtener_notas_por_usuario(idc)
        if not notas:
            return jsonify({"error": "No se han encontrado más notas"})
        
        notasSerializadas = []
        for nota in notas:
            if isinstance(nota, dict):
                notasSerializadas.append(nota)
            else:
                notasSerializadas.append(nota.to_dict())

        return jsonify(notasSerializadas)
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500  # Retorna el error 500 para indicar un error interno del servidor


# Traer nota por su id
@app.route('/notas/<id>', methods=['GET'])
def obtenerNotaPorId(id):
    try:
        idc = request.headers.get('email')
        passw = request.headers.get('pass')
        if passw is None or idc is None:
            return jsonify({"message": "No hay credenciales"})
        
        print(f"Obtener Nota con ID {id}")
        nota = nota_repo.obtener_nota_por_id(id, idc)
        if nota is None:
            return jsonify({"error": "No se ha encontrado la nota"})
        
        if isinstance(nota, dict):
            notaSerializada = nota
        else:
            notaSerializada = nota.to_dict()

        return jsonify(notaSerializada)
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500  # Retorna el error 500 para indicar un error interno del servidor



if __name__ == "__main__":
    app.run(debug=True)


# Nueva Nota    
@app.route('/notas', methods=['POST'])
def guardarNota():
    try:
        # Obtener el email del encabezado
        email = request.headers.get('email')
        if email is None:
            return jsonify({"error": "No se proporcionó el email en los encabezados"}), 400
        
        # Obtener los datos de la nota del cuerpo de la solicitud
        data = request.json
        titulo = data.get('titulo')
        texto = data.get('texto')
        isTerminado = data.get('isTerminado')
        isImportante = data.get('isImportante')
        
        if not titulo or not texto or isTerminado is None or isImportante is None:
            return jsonify({"error": "Faltan campos obligatorios en la solicitud"}), 400
        
        # Guardar la nueva nota en el repositorio
        nota_id = nota_repo.crear_nota(titulo, texto, isTerminado, isImportante, email)
        if nota_id:
            return jsonify({"success": True, "nota_id": str(nota_id)}), 200
        else:
            return jsonify({"error": "No se pudo guardar la nota"}), 500
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {e}"}), 500
    
@app.route('/notas/<id>', methods=['DELETE'])
def borrarNota(id):
    try:
        idc = request.headers.get('email')
        passw = request.headers.get('pass')
        if passw is None or idc is None:
            return jsonify({"message": "No hay credenciales"})

        # Intentar borrar la nota
        if nota_repo.borrar_nota(id, idc):
            return jsonify({"message": "Nota eliminada correctamente"})
        else:
            return jsonify({"error": "No se ha encontrado la nota o no tienes permiso para borrarla"})
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500  # Retorna el error 500 para indicar un error interno del servidor



if __name__ == '__main__':
    asyncio.run(debug=True)

