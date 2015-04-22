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
        new_category = Category(name=request.form['name'],description=request.form['description'])
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
        category= session.query(Category).filter_by(id=id_category).one()
        return render_template('editCategory.html',category=category)
    
@app.route('/Categories/delete/<int:id_category>', methods=['GET','POST'])
def deleteCategory(id_category):
    category = session.query(Category).filter_by(id=id_category).one()
    session.delete(category)
    session.commit()
    return redirect('Categories')

@app.route('/Categories/<int:id_category>/Items/')
def Items(id_category):
    items = session.query(Item).filter_by(category_id=id_category).all()
    return render_template('items.html',items=items,id_category=id_category)

@app.route('/Categories/<int:id_category>/Items/new/',methods=['GET','POST'])
def addItem(id_category):
    if request.method == 'POST':
        filename =photos.save(request.files['picture'])
        newitem = Item(name=request.form['name'],description=request.form['description'],image_name=filename,category_id=id_category)
        session.add(newitem)
        session.commit()
        return redirect(url_for('Items',id_category=id_category))
    else:
        return render_template('newitem.html',id_category=id_category)
    
@app.route('/')
@app.route('/Categories/<int:id_category>/Items/edit/<int:id_item>/',methods=['GET','POST'])
def editItem(id_item,id_category):
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
        return redirect(url_for('Items',id_category=id_category))
    else:
        item_edit = session.query(Item).filter_by(id=id_item).one()
        url = photos.url(item_edit.image_name)
        return render_template('editItem.html',item=item_edit,url=url,id_category=id_category)
    
  
@app.route('/Categories/<int:id_category>/Items/delete/<int:id_item>/')
def deleteItem(id_item,id_category):
    item = session.query(Item).filter_by(id=id_item).one()
    session.delete(item)
    session.commit()
    return redirect(url_for('Items',id_category=id_category))

@app.route('/Items/<int:id_item>/')
def show_item(id_item):
    ex_item = session.query(Item).filter_by(id=id_item).one()
    url = photos.url(ex_item.image_name)
    return render_template("showitem.html",item=ex_item,direc=url)
  

if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1',port = 5000)

