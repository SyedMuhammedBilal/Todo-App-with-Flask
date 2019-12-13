import graphene
from graphene.relay import Node
from models         import Id          as IdModel
from models         import Title       as titleModel
from models         import Description as descriptionModel
from models         import Done        as doneModel
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

class Id(MongoengineObjectType):
	class Meta:
		model = IdModel
		interfaces = (Node,)

class Title(MongoengineObjectType):
	class Meta:
		model = titleModel
		interfaces = (Node,)

class Description(MongoengineObjectType):
	class Meta:
		model = descriptionModel
		interfaces = (Node,)

class Done(MongoengineObjectType):
	class Meta:
		model = doneModel
		interfaces = (Node, )

class Query(graphene.ObjectType):
	node = Node.Field()
	all_id = MongoengineConnectionField(Id)
	all_title = MongoengineConnectionField(Title)
	all_description = MongoengineConnectionField(Description)
	done = graphene.Field(Done)

schema = graphene.Schema(query=Query, types=[Id, Title, Description, Done])