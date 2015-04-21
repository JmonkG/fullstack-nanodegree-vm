import os
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
    user_id = Column(Integer,ForeignKey('User.id'))
    user = relationship('User')
    
class Item(Base):
    __tablename__ = 'Item'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(80),nullable=False)
    description = Column(String(250),nullable=False)
    image_name= Column(String(250),nullable=False)
    category_id = Column(Integer,ForeignKey('Category.id'))
    category = relationship('Category')

'''class ItemPict(Base,Image):    
    __tablename__ = 'ItemPicture'
    
    item_id = Column(Integer,ForeignKey('Item.id'),primary_key = True)
    item = relationship('Item')'''
    

engine = create_engine('sqlite:///Catalog.db')
Base.metadata.create_all(engine)
