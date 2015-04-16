import os
import sys
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_imageattach.entity import Image,image_attachment

Base = declarative_base()

class Category(Base):
    
    __tablename__ = 'Category'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(80),nullable=False)
    description = Column(String(250),nullable=False)

class Item(Base):
    __tablename__ = 'Item'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(80),nullable=False)
    description = Column(String(250),nullable=False)
    image = image_attachment('ItemPict')
    category_id = Column(Integer,ForeignKey('Category.id'))
    category = relationship('Category')

class ItemPict(Base):    
    __tablename__ = 'ItemPicture'
    
    item_id = Column(Integer,ForeignKey('Item.id'),primary_key = True)
    item = relationship('Item')
    

engine = create_engine('sqlite:///Catalog.db')
Base.metadata.create_all(engine)
