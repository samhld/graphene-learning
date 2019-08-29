import graphene
#import pysnooper
import json

#create query type
class Query(graphene.ObjectType):
    #specify field and data type
    hello = graphene.String()
    is_admin = graphene.Boolean()
    #resolver function will resolve string "world" from field hello
    #resolver functions are special types of functions specific to GraphQL operations
    #must be prepended with "resolve_" (snake case)
    def resolve_hello(self, info):
        return "world"

    def resolve_is_aadmin(self, info):
        return True

#set Query type to Schema and save to schema variable
schema = graphene.Schema(query=Query)


result = schema.execute(
    #even though graphene requires snake case for the resolver functions, graphql requires camel case
    #note 'is_admin' is called with 'isAdmin'
    '''
    {
        isAdmin
    }
    '''
)

#print odict of items in result
print(result.data.items())
#print result of using the 'hello' operation--the value of the field 'hello', in this case
print(result.data['isAdmin'])
#print the dict of items in json
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2)) #setting an indent makes json much more readable
