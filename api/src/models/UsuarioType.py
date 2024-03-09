import graphene


class UserType(graphene.ObjectType):
    email = graphene.String()
    notas = graphene.List(graphene.ID)