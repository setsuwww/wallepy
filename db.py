from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///example.db', echo=False)
Session = sessionmaker(bind=engine)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    description = Column(String)
    amount = Column(Float)
    date = Column(Date, default=datetime.datetime.today)

Base.metadata.create_all(engine)