import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    
    __tablename__ = 'User'
    
    id = Column(Integer,primary_key = True)
    name = Column(String(250),nullable = False)
    password = Column(String(250),nullable = False)
    email_address = Column(String(250),nullable = False)

class Category(Base):
    
    __tablename__ = 'Category'

    id = Column(Integer,primary_key = True)
    name = Column(String(250),nullable = False)
    user_id = Column(Integer,ForeignKey('User.id'))
    user = relationship(User)

class Item(Base):
    
    __tablename__ = 'Item'
    
    id = Column(Integer,primary_key = True)
    name = Column(String(250), nullable = False)
    description = Column(String(500))
    category_id = Column(Integer,ForeignKey('Category.id'))
    category = relationship(Category)

engine = create_engine('sqlite:///projectws.db')
 
Base.metadata.create_all(engine)
    