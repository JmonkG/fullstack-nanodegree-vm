from flask import Flask,render_template,url_for,redirect,request,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from flask import session as login_session
import random,string

app = Flask(__name__)
app.secret_key='super_super_secret'

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


@app.route('/login')
def showLogin():
    state =''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')
    
@app.route('/restaurants/JSON')
def RestaurantJSON():
    rest = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.rest_jsonformat for i in rest])
    
@app.route('/restaurants/<int:restaurant_id>/JSON')
def MenusxRestaurantJSON(restaurant_id):
    menuitems = session.query(MenuItem).filter_by(restaurant_id= restaurant_id).all()
    return jsonify(ItemsMenu=[i.item_jsonformat for i in menuitems])
    
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuITemJSON(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(id= menu_id).one()
    return jsonify(Item=item.item_jsonformat)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('Create_menu.html',restaurant= restaurant,items= items)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newitem = MenuItem(name= request.form['name'],restaurant_id= restaurant_id)
        session.add(newitem)
        session.commit()
        flash('you created a brand new menuItem')
        return redirect(url_for('restaurantMenu',restaurant_id= restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id= restaurant_id)
    

#Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        editedItem = session.query(MenuItem).filter_by(id= menu_id).first()
        editedItem.name = request.form['editname']
        session.commit()
        flash('you modified the item %s'% editedItem.name)
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id= restaurant_id).one()
        item = session.query(MenuItem).filter_by(id= menu_id).one()
        return render_template('editmenuitem.html',restaurant=restaurant,item=item)  

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    #if request.method == 'GET':
    menuitem = session.query(MenuItem).filter_by(id= menu_id).first()
    session.delete(menuitem)
    session.commit()
    flash('you just deleted the item')
    return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))    
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1',port = 5000)
    