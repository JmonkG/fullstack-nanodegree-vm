from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp/test.db'
db = SQLAlchemy(app)

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key = 'TRUE')
    name = db.Column(db.String(80))
    race = db.Column(db.String(80))
    
    def __init__(self,name,race):
        self.name = name
        self.race = race
    