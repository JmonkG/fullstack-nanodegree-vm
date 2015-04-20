import os
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify
from flask.ext.uploads import UploadSet,IMAGES,configure_uploads
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base,Category,Item
from werkzeug import secure_filename



app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST']= os.getcwd()+'/images'
photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)

#OPEN DB PARAMETERS
engine = create_engine('sqlite:///Catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/Items/')
def Items():
    items = session.query(Item).all()
    return render_template('items.html',items=items)


@app.route('/Items/new/',methods=['GET','POST'])
def addItem():
    if request.method == 'POST':
        filename =photos.save(request.files['picture'])
        newitem = Item(name=request.form['name'],description=request.form['description'],image_name=filename)
        session.add(newitem)
        session.commit()
        return redirect(url_for('show_item',id_item=newitem.id))
    else:
        return render_template('newitem.html')
    
@app.route('/')
@app.route('/Items/edit/<int:id_item>/',methods=['GET','POST'])
def editItem(id_item):
    if request.method == 'POST':
        filename = photos.save(request.files['picture'])
        name = request.form['name']
        description = request.form['description']
        item = session.query(Item).filter_by(id=id_item).one()
        item.name = name
        item.description = description
        item.image_name = filename
        session.add(item)
        session.commit()
        return redirect(url_for('Items'))
    else:
        item_edit = session.query(Item).filter_by(id=id_item).one()
        url = photos.url(item_edit.image_name)
        return render_template('editItem.html',item=item_edit,url=url)
    
  
@app.route('/Items/delete/<int:id_item>/')
def deleteItem(id_item):
    item = session.query(Item).filter_by(id=id_item).one()
    session.delete(item)
    session.commit()
    return redirect('Items')

@app.route('/Items/<int:id_item>/')
def show_item(id_item):
    ex_item = session.query(Item).filter_by(id=id_item).one()
    url = photos.url(ex_item.image_name)
    return render_template("showitem.html",item=ex_item,direc=url)
  

if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1',port = 5000)

