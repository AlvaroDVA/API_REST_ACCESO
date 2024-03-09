

from flask import Flask, jsonify, request, abort
from graphene import ObjectType, String, Schema, ID, List, Field, Mutation, InputObjectType, Boolean

from repositories.notas_repository_maria import NotasRepositoryMaria
from repositories.notas_repository_mongo import NotasRepositoryMongo
from repositories.usuario_repository_mongo import UsuarioRepostoryMongo

from graphql import GraphQLField

app = Flask(__name__)

DB_TYPE = "mongodb"

if DB_TYPE == "mongodb":
    nota_repo = NotasRepositoryMongo()
    user_repo = UsuarioRepostoryMongo()
elif DB_TYPE == "mariadb":
    nota_repo = NotasRepositoryMaria()


if __name__ == '__main__':
    app.run(debug=True)