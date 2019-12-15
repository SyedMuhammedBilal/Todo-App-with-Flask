from sqlalchemy                 import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import scoped_session, sessionmaker
from sqlalchemy                 import Column, DateTime, ForeignKey, Integer, Text, func, String

engine = create_engine("mysql://root:@localhost/todoapp")
db_session = scoped_session(sessionmaker(autocommit=False,
	                                     autoflush=False,
	                                     bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Todo(Base):
	__tablename__ = "todo"
	id = Column(Integer, primary_key=True)
	title = Column(String(Text))
	description = Column(Text)
	done = Column(String(255))