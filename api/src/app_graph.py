import asyncio
from flask import Flask, request
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

class CrearNota(graphene.Mutation):
    class Arguments:
        titulo = graphene.String(required=True)
        texto = graphene.String(required=True)
        isImportante = graphene.Boolean(required=True)
        isTerminado = graphene.Boolean(required=True)

    id = graphene.ID()
    success = graphene.Boolean()

    def mutate(self, info,titulo, texto, isImportante, isTerminado):
        # Validar las credenciales del usuario
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not user_repo.validar_credenciales(email, password):
            raise Exception("Credenciales inválidas")

        # Crear la nota y obtener su ID
        nota_id = nota_repo.crear_nota(titulo, texto, isImportante, isTerminado, email)
        
        # Retornar la ID de la nota y éxito
        return CrearNota(id=nota_id, success=True)



class Mutations(graphene.ObjectType):
    CrearNota = CrearNota.Field()

# Define las consultas (queries)
class Query(graphene.ObjectType):
    notas = graphene.List(NotaType)
    
    def resolve_notas(self, notas):
        
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not user_repo.validar_credenciales(email, password):
            raise Exception("Credenciales inválidas")
        notas = nota_repo.obtener_notas_por_usuario(email)
        return [NotaMapper.map_nota_to_notatype(nota) for nota in notas]


schema = graphene.Schema(query=Query, mutation=Mutations)

app = Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    asyncio.run(debug=True)
