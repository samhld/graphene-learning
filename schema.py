import graphene
#import pysnooper
import json
from datetime import datetime
import random
import uuid

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return 'https://cloudinary.com/{}/{}'.format(self.username, self.id)

#create query type
class Query(graphene.ObjectType):
    #specify field and data type
    hello = graphene.String()
    is_admin = graphene.Boolean()
    users = graphene.List(User,limit=graphene.Int())
    #resolver function will resolve string "world" from field hello
    #resolver functions are special types of functions specific to GraphQL operations
    #must be prepended with "resolve_" (snake case)
    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return random.sample([
            User(id="1", username="Fred", created_at=datetime.now()),
            User(id="2", username="Bob", created_at=datetime.now())
        ],limit)

#create a class/type that inherets from Mutation class
class CreateUser(graphene.Mutation):
    user = graphene.Field(User) #inherets from User class to determine user's shape

    #passing in arguments to Mutations requires an inner class of Arguments
    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        if info.context.get('is_anonymous'):
            raise Exception("Not authenticated")
        post = Post(title=title, content=content)
        return CreatePost(post=post)



class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field() # class we define that inherets from this Mutation class
    create_post = CreatePost.Field()

#set schema types to Schema and save to schema variable
schema = graphene.Schema(query=Query, mutation=Mutation)

#graphene.Schema has a method `execute` that runs a query based on a query string you pass it
result = schema.execute(
    #even though graphene requires snake case for the resolver functions, graphql requires camel case
    #note 'create_user' is called with 'createUser'
    '''
    query getUsers ($limit: Int){
        users  (limit: $limit) {
            id
            createdAt
            username
            avatarUrl
        }
    }
    ''',
    #if only want posts created by authenticated users, pass value "context" which can be anything
    #context={'is_anonymous': True},
    variable_values={'limit': 1}
)

#print odict of items in result
#print(result.data.items())
#print result of using the 'hello' operation--the value of the field 'hello', in this case
#print(result.data['users'])
#print the dict of items in json
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2)) #setting an indent makes json much more readable