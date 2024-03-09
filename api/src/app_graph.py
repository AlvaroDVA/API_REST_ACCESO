import asyncio
from flask import Flask
from flask_graphql import GraphQLView
import graphene
from graphene import Mutation
from mappers.mappers import NotaMapper

# Importa las clases y funciones necesarias desde otros archivos
from models.NotaType import NotaType
from repositories.notas_repository_maria import NotasRepositoryMaria
from repositories.notas_repository_mongo import NotasRepositoryMongo
from repositories.usuario_repository_mongo import UsuarioRepostoryMongo

# Define las mutaciones

DB_TYPE = "mongodb"
if DB_TYPE == "mongodb":
    nota_repo = NotasRepositoryMongo()
    user_repo = UsuarioRepostoryMongo()
elif DB_TYPE == "mariadb":
    nota_repo = NotasRepositoryMaria()

# class Mutations(graphene.ObjectType):

# Define las consultas (queries)
class Query(graphene.ObjectType):
    notas = graphene.List(NotaType, email=graphene.String(required=True), password=graphene.String(required=True))

    def resolve_notas(self, info, email, password):
        if not user_repo.validar_credenciales(email, password):
            raise Exception("Credenciales inválidas")
        notas = nota_repo.obtener_notas_por_usuario(email)
        return [NotaMapper.map_nota_to_notatype(nota) for nota in notas]


#schema = graphene.Schema(query=Query, mutation=Mutations)
schema = graphene.Schema(query=Query)

app = Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    asyncio.run(debug=True)
