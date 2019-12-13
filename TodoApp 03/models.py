from datetime import datetime
from mongoengine import Document
from mongoengine.fields import DateTimeField, ReferenceField, StringField

class Id(Document):
	meta = {"todo": "id"}
	name = StringField()

class Title(Document):
	meta = {"todo": "tile"}
	name = StringField()

class Description(Document):
	meta = {"todo": "description"}
	name = StringField()

class Done(Document):
	meta = {"todo": "done"}
	name = StringField()
	done_on = DateTimeField(default=datetime.now)