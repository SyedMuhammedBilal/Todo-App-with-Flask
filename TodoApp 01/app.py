from flask         import Flask, render_template, redirect
from flask_pymongo import PyMongo 
from flask         import jsonify
from bson.objectid import ObjectId 
from flask         import request

app = Flask(__name__)

# Connecting App to a DataBase
app.config["MONGO_DBNAME"] = "cluster0"
app.config["MONGO_URI"] = "mongodb+srv://SyedMuhammed:rb26dettrb30@cluster0-0glm6.gcp.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)
# print(mongo)
# task_id = ObjectId()
# print(task_id)

# Index page
@app.route("/")
def index():
	return "<h1><center>Todo List</center></h1>"


# Getting All Task route
@app.route("/todo/api/v1.0/tasks", methods=["GET"])
def get_all_tasks():
	result = []
	task_db = mongo.db.tasks
	
	if task_db.count_documents({}) > 0:
		for task in task_db.find():
			result.append({
				"id": str(task["_id"]), 
				"title":task["title"], 
				"description": task["description"], 
				"done": task["done"]
				})
	
	return jsonify({"tasks" :result})


# Adding Task route
@app.route("/todo/api/v1.0/tasks/<task_id>", methods=["GET"])
def add_task(task_id):
	result = []
	task = mongo.db.tasks.find_one_or_404({"_id": ObjectId("5dec8e0b0e38d4df6b25be65")})
	result.append({
		"id": str(task["_id"]), 
		"title":task["title"], 
		"description": task["description"], 
		"done": task["done"]
		})
	
	return jsonify({"tasks": result})


# Creating Task route
@app.route("/todo/api/v1.0/tasks", methods=["POST"])
def create_task():
	title = request.json.get("title", " ")
	description = request.json.get("description", " ")
	task_db = mongo.db.tasks
	n_task_id = task_db.insert_one({"title": title, "description": description, "done": False})
	
	return jsonify({"id": str(n_task_id)})


# Updating Task route
@app.route("/todo/api/v1.0/tasks/<ObjectId:task_id>", methods=["PUT"])
def update_task(task_id):
	task_db = mongo.db.tasks
	task = task_db.find_one_and_update({"_id": task_id}, upsert=False)
	
	title = request.get_json("title", tasks["title"])
	description = request.get_json("description", task["description"])
	done = bool(request.get_json("done", 
		                        task["done"]))

	task["title"] = title
	task["description"] = description
	task["done"] = done
	task_db.save(task)
	
	response = {"status": "Success", "status_code": "200", "message": "TASK UPDATED"}
	return jsonify({"response": response})


# Deleting Task route
@app.route("/todo/api/v1.0/tasks/<ObjectId:task_id>", methods=["DELETE"])
def delete_task(task_id):
	task_db = mongo.db.tasks
	response = task.delete_one({"_id": task_id})
	
	if response.deleted_count == 1:
		result = {"message": "Record Deleted"}
	else:
		result = {"message": "No Record Found"}
	
	return jsonify({"result": result})


# Error Handler route
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