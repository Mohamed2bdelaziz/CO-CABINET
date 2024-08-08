import urllib
import sqlalchemy
from sqlalchemy import func, create_engine, inspect, MetaData
from sqlalchemy import Table, Column, DateTime, String, Integer,Float
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
import urllib

Model = declarative_base(name='Model')

def get_azure_connection_engin():
  load_dotenv('.env')
  cnxn_str = os.getenv('CONNECTION_STRING')
  params = urllib.parse.quote_plus(cnxn_str)
  cnxn_str = 'mssql+pyodbc:///?odbc_connect={}?charset=utf8mb4'.format(params)
  try:
    engine_azure = create_engine(cnxn_str,echo=True)
  except sqlalchemy.Error as e:
    print(f"Error connecting to azure engin:\n{'='*10}\n{e}")
  
  return engine_azure

def connect_to_azure_db(engine_azure):
  return engine_azure.connect()

def end_azure_connection(connection, engine_azure):
  connection.close()
  engine_azure.dispose()

def create_session(engine_azure):
    Session = sessionmaker(bind=engine_azure) 
    return Session() 

def connect():
   engine_azure = get_azure_connection_engin()
   connection = connect_to_azure_db(engine_azure)
   session = create_session(engine_azure)

   inspector = inspect(engine_azure)
   if "Complaints" not in inspector.get_table_names():
      Model.metadata.create_all(engine_azure) 

   return engine_azure, connection, session

class Complaints(Model):
    __tablename__ = "Complaints"
    id= Column(Integer, autoincrement=True, primary_key=True)
    name= Column(String(80))
    national_id=Column(String(14))
    governorate= Column(String(80))
    phone=Column(String(80))
    Complaint=Column(String(1000),  nullable=False)
    summary=Column(String(1000))
    complaint_time=Column(DateTime,default=func.now())
    email= Column(String(120))
    files= Column(String(80),  nullable=True)
    tfidf = Column(Integer)
    sen_analysis = Column(Float)
    def __repr__(self):
        return f'<Complaints {self.id}>'


def add_complaint(
      session,
      name,
      national_id,
      governorate,
      phone,
      Complaint,
      email):
  new_com = Complaints(
      name = name,
      national_id = national_id,
      governorate = governorate,
      phone = phone,
      Complaint = Complaint,
      email = email) 
  session.add(new_com)
  session.commit()