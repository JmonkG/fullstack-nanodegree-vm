import os
from lxml import etree
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,Response
from flask.ext.uploads import UploadSet,IMAGES,configure_uploads
from flask.ext.xmlrpc import XMLRPCHandler
from sqlalchemy import create_engine,desc,and_
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

app.config["JSON_SORT_KEYS"] = False




@app.route('/catalog/catalog.xml',methods=['GET'])
def sitemapXML():
 Catalog = session.query(Category).all()
 for i in Catalog:
    items = session.query(Item).filter_by(category_id= i.id).all()
    i.Items = items
 sitemap_xml = render_template('sitemap.xml',Categories=Catalog)
 resp = Response(sitemap_xml,status=200,mimetype='text/xml')
 return resp
 
@app.route('/catalog/catalog.json',methods=['GET'])
def CatalogJSON():
 Catalog = session.query(Category).all()
 for i in Catalog:
    items = session.query(Item).filter_by(category_id= i.id).all()
    i.Items = items
 return jsonify(Catalog=[a.serialize for a in Catalog])    

@app.route('/catalog/')
def categories():
    categories = session.query(Category).all()
    return render_template('categories.html',categories=categories)

@app.route('/catalog/<category_name>/Items/')
def Items(category_name):
    cat = session.query(Category).filter_by(name=category_name).one();
    items = session.query(Item).filter_by(category_id=cat.id).all()
    return render_template('items.html',items=items,category_name=category_name)

@app.route('/catalog/<category_name>/Items/new/',methods=['GET','POST'])
def addItem(category_name):
    if request.method == 'POST':
        cat = session.query(Category).filter_by(name=category_name).one()
        filename =photos.save(request.files['picture'])
        newitem = Item(name=request.form['name'],description=request.form['description'],image_name=filename,category_id=cat.id)
        session.add(newitem)
        session.commit()
        return redirect(url_for('Items',category_name=category_name))
    else:
        cat = session.query(Category).filter_by(name=category_name).one()
        return render_template('newitem.html',id_category=cat.id,category_name=category_name)
    
@app.route('/')
@app.route('/catalog/<category_name>/Items/edit/<item_name>/',methods=['GET','POST'])
def editItem(item_name,category_name):
    if request.method == 'POST':
        cat = session.query(Category).filter_by(name=category_name).one()
        name = request.form['name']
        description = request.form['description']
        item = session.query(Item).filter(and_(Item.name==item_name,Item.category_id==cat.id)).one()
        item.name = name
        item.description = description
        if request.files['picture']:
            filename = photos.save(request.files['picture'])
            item.image_name = filename
        session.add(item)
        session.commit()
        return redirect(url_for('Items',category_name=category_name))
    else:
        cat = session.query(Category).filter_by(name=category_name).one()
        item_edit = session.query(Item).filter_by(name=item_name).one()
        url = photos.url(item_edit.image_name)
        return render_template('editItem.html',item=item_edit,url=url,category_name=category_name)
    
  
@app.route('/catalog/<category_name>/Items/delete/<item_name>/')
def deleteItem(item_name,category_name):
    cat = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter(and_(Item.name==item_name,Item.category_id==cat.id)).one()
    session.delete(item)
    session.commit()
    return redirect(url_for('Items',category_name=category_name))

def select_last_items():
    tuples =[]
    items = session.query(Item).order_by(desc(Item.id)).all()
    for i in items:
        category = session.query(Category).filter_by(id=i.category_id).one()
        tup = (i.name,category.name)
        tuples.append(tup)
    return tuples

if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1',port = 8000)

