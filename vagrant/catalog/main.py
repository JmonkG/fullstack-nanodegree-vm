import os
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify
from flask.ext.uploads import UploadSet,IMAGES,configure_uploads
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base,Category,Item
from werkzeug import secure_filename



app = Flask(__name__)
#Configuration of Flask Uploads
app.config['UPLOADED_PHOTOS_DEST']= os.getcwd()+'/images'
photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)

#OPEN DB PARAMETERS
engine = create_engine('sqlite:///Catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/Categories/')
def categories():
    categories = session.query(Category).all()
    return render_template('categories.html',categories=categories)

@app.route('/Categories/new',methods=['GET','POST'])
def addCategory():
    if request.method == 'POST':
        new_category = Item(name=request.form['name'],description=request.form['description'])
        session.add(new_category)
        session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template('newcategory.html')
    
@app.route('/Categories/edit/<int:id_category>/',methods=['GET','POST'])
def editCategory(id_category):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = session.query(Category).filter_by(id=id_category).one()
        category.name = name
        category.description = description
        session.add(category)
        session.commit()
        return redirect(url_for('categories'))
    else:
        category_edit = session.query(Category).filter_by(id=id_category).one()
        return render_template('editCategory.html',category = category_edit)
    
@app.route('/Categories/delete/<int:id_category>', methods=['GET','POST'])
def deleteCategory(id_category):
    category = session.query(Category).filter_by(id=id_category).one()
    session.delete(category)
    session.commit()
    return redirect('Categories')

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

