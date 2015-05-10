import os
from collections import OrderedDict
import sys
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
#from sqlalchemy_imageattach.entity import Image,image_attachment

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id= Column(Integer,primary_key = True)
    name = Column(String(50),nullable=False)
    email = Column(String(100),nullable=False)

class Category(Base):
    
    __tablename__ = 'Category'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(80),nullable=False)
    description = Column(String(250),nullable=False)
    Items = relationship("Item", backref="Category")
    @property
    def serialize(self):
        CatDict ={
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'Items': [i.serialize for i in self.Items],
        }
        return CatDict
       
    #user_id = Column(Integer,ForeignKey('User.id'))
    #user = relationship('User')
    
class Item(Base):
    __tablename__ = 'Item'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(80),nullable=False)
    description = Column(String(250),nullable=False)
    image_name= Column(String(250),nullable=False)
    category_id = Column(Integer,ForeignKey('Category.id'))
    category = relationship('Category')
    @property
    def serialize(self):
        ItemsDict = {
            'name':self.name,
            'id': self.id,
            'description': self.description,
            'image':self.image_name,
        }
        return ItemsDict

    

engine = create_engine('sqlite:///Catalog.db')
Base.metadata.create_all(engine)
