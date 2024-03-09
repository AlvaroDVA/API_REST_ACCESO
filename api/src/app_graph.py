import asyncio
from flask import Flask, request
from flask_graphql import GraphQLView
import graphene
from graphene import Mutation
from mappers.mappers import NotaMapper

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

    success = graphene.Boolean()
    id = graphene.ID()
    message = graphene.String()

    def mutate(self, info,titulo, texto, isImportante, isTerminado):
        # Validar las credenciales del usuario
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not user_repo.validar_credenciales(email, password):
            return CrearNota(success=True, message="Credenciales inválidas" , id=id)

        # Crear la nota y obtener su ID
        nota_id = nota_repo.crear_nota(titulo, texto, isImportante, isTerminado, email)
        
        # Retornar la ID de la nota y éxito
        return CrearNota(success=True, message="Nota Guardada" ,id=nota_id)
    
class EliminarNota(Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    res = graphene.Boolean()
    message = graphene.String()    
    id = graphene.ID()

    def mutate(self, info, id):
        # Validar las credenciales del usuario
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not user_repo.validar_credenciales(email, password):
            return (EliminarNota(id, "Credenciales invalidas", None))

        if (nota_repo.borrar_nota(id, email) == 0):
            return (EliminarNota(False, "La nota no se ha podido eliminar"), id)
        else:
            return (EliminarNota(True, "Nota eliminada", id))

class DeleteAll(Mutation):
    class Arguments:
        confirmacion = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, confirmacion):
        # Validar las credenciales del usuario
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not user_repo.validar_credenciales(email, password):
            return DeleteAll("Credenciales inválidas")

        if confirmacion == True:
            return DeleteAll("No has confirmado que quieres borrar todas las notas")


        if (nota_repo.delete_all_notas(confirmacion=confirmacion, usuario_email=email)):
            user_repo.borrar_todas_las_notas_de_usuario(email)
            return (DeleteAll("Notas eliminadas correctamente"))
        else:
            return (DeleteAll("No se han podido borrar las notas"))
        
class ActualizarNota(Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        titulo = graphene.String(required=False)
        texto = graphene.String(required=False)
        isImportante = graphene.Boolean(required=False)
        isTerminado = graphene.Boolean(required=False)
    
    success = graphene.Boolean()
    message = graphene.String()    

    def mutate (self, info, id, titulo=None, texto=None, isImportante=None, isTerminado=None):
        # Validar las credenciales del usuario
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not user_repo.validar_credenciales(email, password):
            return ActualizarNota(success=False, message="Credenciales inválidas")
        
        if nota_repo.actualizar_nota(nota_id=id, email_usuario=email, titulo=titulo, texto=texto, isTerminado=isTerminado, isImportante=isImportante):
            return ActualizarNota(success=True, message="Nota Actualizada")
        else:
            return ActualizarNota(success=False, message="No se ha podido actualizar la nota")


        


class Mutations(graphene.ObjectType):
    CrearNota = CrearNota.Field()
    EliminarNota = EliminarNota.Field()
    DeleteAll = DeleteAll.Field()
    ActualizarNota = ActualizarNota.Field()

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
