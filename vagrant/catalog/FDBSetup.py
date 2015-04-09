from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)
        
class User(db.Model):
    
    __tablename__ = 'User'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(250),nullable = False)
    password = db.Column(db.String(250),nullable = False)
    email_address = db.Column(db.String(250),nullable = False)
    
    def __init__(self,name,password,email):
        self.name = name
        self.password = password
        self.email_address = email

class Category(db.Model):
    
    __tablename__ = 'Category'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(250),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    user = db.relationship('User')
    
    def __init__(self,name,user):
        self.name = name
        self.user = user

class Item(db.Model):
    
    __tablename__ = 'Item'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(250), nullable = False)
    description = db.Column(db.String(500))
    category_id = db.Column(db.Integer,db.ForeignKey('Category.id'))
    category = db.relationship('Category',backref=db.backref('items',lazy='dynamic'))
    
    def __init__(self,name,description,category):
        self.name = name
        self.description = description
        self.category = category