from database import init_db
from flask import Flask 
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True

default_query = """
{
  allTodo {
    edges {
      node {
        id,
        title,
        description,
        done
      }
    }
  }
}""".strip()

app.add_url_rule("/graph-ql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

if __name__ == '__main__':
	init_db()
	app.run()