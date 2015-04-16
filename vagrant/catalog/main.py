from flask import Flask,render_template,url_for,redirect,request,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base,Category,Item,ItemPict
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
from sqlalchemy_imageattach.context import store_context


app = Flask(__name__)

engine = create_engine('sqlite:///Catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

fs_store = HttpExposedFileSystemStore('itemimages','images/')
app.wsgi_app = fs_store.wsgi_middleware(app.wsgi_app)



