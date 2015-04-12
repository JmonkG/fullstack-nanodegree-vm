import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    
    __tablename__ = 'Restaurant'
    id = Column(Integer,primary_key = True)
    name = Column(String(80),nullable =  False)
    
engine = create_engine('sqlite:///Restaurant.db')
Base.metadata.create_all(engine)