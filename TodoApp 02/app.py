from flask            import Flask, render_template
from flask_pymongo    import PyMongo 
from flask            import jsonify, redirect, json 
from flask_sqlalchemy import SQLAlchemy
from bson.objectid    import ObjectId 
from flaskext.mysql   import MySQL

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://Syed Bilal:k20k24@localhost/todo-py"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
	__tablename__ = "tasks"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200))
	description = db.Column(db.Text)
	done = db.Column(db.Boolean, default=False)

	def __init__(self, title, description, done=False):
		self.title = title
		self.description = description
		self.done = done

	def __repr__(self):
		return "<id {}>".format(self.id)


@app.route("/")
def index():
	return "<center><h1>Todo App</h1></center>"

@app.route("/todo/api/v1.0/tasks", methods=["GET"])
def get_all_task():
	result = []
	task_db = Todo.query.all()
	if task_db:
		for task in task_db:
			result.append({"id": str(task.id), 
				"title":task.title, 
				"description": task.description, 
				"done": task.done
				})

	return jsonify({"tasks": result})

@app.route("/todo/api/v1.0/tasks/<task_id>", methods=["GET"])
def add_task(task_id):
	result = []
	task = Todo.query.filter_by(id=task_id).first()
	task_db = Todo.query.all()
	if task_db:
		for task in task_db:
			result.append({
				"id": str(task.id),
			    "title": task.title,
			    "description": task.description,
			    "done": task.done
			    })
	
	return jsonify({"tasks": result})

@app.route("/todo/api/v1.0/tasks", methods = ['POST'])
def create_tasks():
	title = request.json.get("title", " ")
	description = request.json.get("description", " ")
	task = Todo(title, description)
	db.session.add(task)
	db.session.commit()

	return jsonify({"id": task.id})

@app.route("/todo/api/v1.0/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
	task_db = Todo.query.all()
	task = Todo.query.filter_by(id=task_id, upsert=False).first()

	title = request.get_json("title", tasks.title)
	description = request.get_json("description", task.description)
	done = bool(request.get_json("done", task.done))

	task.title = title
	task.description = description
	task.done = done
	db.session.commit()
	
	response = {"status": "Success", "status_code": "200", "message": "TASK UPDATED"}
	return jsonify({"response": response})

@app.route("/todo/api/v1.0/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Todo.query.filter_by(id=task_id).first() 
    if task:
    	db.session.delete(task)
    	db.session.commit()
    	result = {"message": "Record Deleted"}
    else:
    	result = {"message": "No Record Found"}
    return jsonify({"result": result})

@app.errorhandler(404)
def not_found(error):
	response = {
	"status": "error", 
	"status_code": "404", 
	"message": "Not Found"
	}
	
	return jsonify({"response": response})

if __name__ == '__main__':
	app.run(debug=True)