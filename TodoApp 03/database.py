from mongoengine import connect
from models import Id, Title, Description, Done

connect(host="mongodb+srv://SyedMuhammed:rb26dettrb30@cluster0-0glm6.gcp.mongodb.net/test?retryWrites=true&w=majority")

def init_db():

	identity = Id(name="5dec8e0b0e38d4df6b25be65")
	identity.save()

	title = Title(name="HomeWork")
	title.save()

	desc = Description(name="do today's HomeWork")
	desc.save()

	store = Done(name="done")
	store.save