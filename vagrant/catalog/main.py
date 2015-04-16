import os
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base,Category,Item
from werkzeug import secure_filename

UPLOADED_FILES_DEST= os.getcwd()+'/images'
photos = UploadSet('photos',IMAGES)
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
#from sqlalchemy_imageattach.context import store_context

#HttpExposedFileSystemStore(
#    path='fullstack-nanodegree-vm/vagrant/catalog/images',
#    prefix='images/'
#)
app = Flask(__name__)
engine = create_engine('sqlite:///Catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#fs_store = HttpExposedFileSystemStore('itempics','images/')
#app.wsgi_app = fs_store.wsgi_middleware(app.wsgi_app)


@app.route('/')
@app.route('/Item/new/',methods=['GET','POST'])
def addItem():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.form['photo'])
        rec= Photo()
        newitem = Item(name=request.form['name'],description='whatevs')
        session.add(newitem)
        session.commit()
        return redirect(url_for('show_item',id_item=1))
    else:
        return render_template('newitem.html')

@app.route('/Item/<int:id_item>/')
def show_item(id_item):
  

if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1',port = 5000)

