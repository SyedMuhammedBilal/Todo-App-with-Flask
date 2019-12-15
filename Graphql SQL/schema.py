import graphene
from graphene            import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database            import db_session, Todo as TodoModel
from sqlalchemy          import and_

class Todo(SQLAlchemyObjectType):
	class Meta:
		model = TodoModel
		interfaces = (relay.Node, )

class createTodo(graphene.Mutation):
	class Input:
		#Id = graphene.String()
		title = graphene.String()
		description = graphene.String()
		done = graphene.String()
	ok = graphene.Boolean()
	todo = graphene.Field(Todo)

	@classmethod
	def mutate(cls, _, context, **kwargs):
			todo = TodoModel(title=kwargs.get("title"), description=kwargs.get("description"), done=kwargs.get("done"))
			db_session.add(todo)
			db_session.commit()
			ok = True
			return createTodo(todo=todo, ok=ok)

class changeTitle(graphene.Mutation):
	class Input:
		title = graphene.String()
		description = graphene.String()

	ok = graphene.Boolean()
	todo = graphene.Field(Todo)

	@classmethod
	def mutate(cls, _, context, **kwargs):
		query = Todo.get_query(context)
		description = kwargs.get("description")
		title = kwargs.get("title")
		todo = query.filter(TodoModel.description == description).first()
		todo.title = title
		ok = True

		return changeTitle(todo=todo, ok=ok)

class Query(graphene.ObjectType):
	node = relay.Node.Field()
	todo = SQLAlchemyConnectionField(Todo)
	find_todo = graphene.Field(lambda: Todo, title=graphene.String())
	all_todos = SQLAlchemyConnectionField(Todo)

	def resolve_find_todo(cls, _, context, **kwargs):
		query = Todo.get_query(context)
		title = kwargs.get("title")
		return query.filter(TodoModel.title == title).first()

class MyMutations(graphene.ObjectType):
	create_todo = createTodo.Field()
	change_title = changeTitle.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Todo])