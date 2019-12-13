from app import app
import unittest
import json

class FlaskTestCase(unittest.TestCase):

	def app(self):
		print("Setting Up App")
		app.config["TESTING"] = True
		self.app = app.test_client()

	def tearDown(self):
		print("Tearing Down")

	def test_index(self):
		tester = app.test_client(self)
		response = tester.get("/", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_index_load(self):
		tester = app.test_client(self)
		response = tester.get("/", content_type="html/text")
		self.assertIn(b"/", response.data)

	def create_task(self, desc):
		tester = app.test_client(self)
		response = tester.get("/todo/api/v1.0/tasks", content_type="application/json",
			                   data=json.dumps({"title": "App Testing", 
			                   "description": "Test Description from: " +desc}))
		return json.loads(response.get_data(as_text=True))

	def delete_task(self, task_id):
		tester = app.test_client(self)
		response = tester.delete('/todo/api/v1.0/tasks/'+str(task_id), content_type='application/json')
		json_response = json.loads(response.get_data(as_text=True))
		return json_response["result"]

	def test_create_tasks(self):
		tester = app.test_client(self)
		json_response = self.create_task("create")
		task_id = json_response["tasks"]
		self.assertIsNotNone(task_id)
	
	def test_delete_task(self):
		tester = app.test_client(self)
		json_response = self.create_task("delete")
		task_id = json_response["tasks"]
		self.assertIsNotNone(task_id)

	def get_all_task(self):
		tester = app.test_client(self)
		response = tester.get('/todo/api/v1.0/tasks', content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Testing App", response.data)

	def test_get_all_task(self):
		tester = app.test_client(self)
		json_response = self.create_task("get all")
		task_id = json_response["tasks"]
		self.assertIsNotNone(task_id)

		json_response = self.delete_task(task_id)
		self.assertIsNotNone(json_response["message"], "success")

	def add_task(self):
		tester = app.test_client(self)
		response = tester.get('/todo/api/v1.0/tasks/'+task_id, content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Testing App", response.data)
		json_response = json.loads(response.get_data(as_text=True))
		self.assertEqual(json_response["tasks"][0]["done"], False)

	def test_add_task(self):
		tester = app.test_client(self)
		json_response = self.create_task("get")
		task_id = json_response["tasks"]
		self.assertIsNotNone(task_id)

		json_response = self.delete_task(task_id)
		self.assertIsNotNone(json_response["message"], "success")

	def update_task(self):
		tester = app.test_client(self)
		response = tester.put("/todo/api/v1.0/tasks"+task_id, content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Testing App", response.data)
		json_response = json.loads(response.get_data(as_text=True))
		self.assertEqual(json_response["result"]["message"], "success")

	def test_update_tasl(self):
		tester = app.test_client(self)
		json_response = self.create_task("updated")
		task_id = json_response["tasks"]
		self.assertIsNotNone(task_id)

		json_response = self.delete_task(task_id)
		self.assertIsNotNone(json_response["message"], "success")

if __name__ == '__main__':
	unittest.main()