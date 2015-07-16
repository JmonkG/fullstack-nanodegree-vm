import os
from lxml import etree
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,Response,make_response
from flask.ext.uploads import UploadSet,IMAGES,configure_uploads
from flask.ext.xmlrpc import XMLRPCHandler
from sqlalchemy import create_engine,desc,and_
from sqlalchemy.orm import sessionmaker
from db_setup import Base,User,Category,Item
#from werkzeug import secure_filename

#for OAUTH2 authorization
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError,AccessTokenCredentials
import httplib2
import json
import requests

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

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

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/')
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    login_session['credentials']= credentials.access_token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token #IMPORTANT CHANGE
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    #user_id = session.query(User).filter_by(email = data["email"]).one()
    #if not user_id:
    #        newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    #        session.add(newUser)
    #        session.commit()
    #login_session['user_id'] = newUser.id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session['credentials']
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status']=='200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/catalog.xml',methods=['GET'])
def CatalogXML():
 Catalog = session.query(Category).all()
 for i in Catalog:
    items = session.query(Item).filter_by(category_id= i.id).all()
    i.Items = items
 catalog_xml = render_template('catalog.xml',Categories=Catalog)
 resp = Response(catalog_xml,status=200,mimetype='text/xml')
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
