from flask import Flask
from flask import render_template
from FDBSetup import db,User,Category,Item

db.create_all()

user = User('josue','josue','josue@josue.com')
cat = Category('Futbol',user)
item1 = Item('Fevernova','balon de futbol',cat)
item2 = Item('Guantes','guantes para tapar',cat)
item3 = Item('Tiza','demarcacion de la cancha',cat)
item4 = Item('Gradas','asientos para el publico',cat)

db.session.add(user)
db.session.add(cat)
db.session.add(item1)
db.session.add(item2)
db.session.add(item3)
db.session.add(item4)
db.session.commit()


list_items = Item.query.filter(category.name == cat.name).all()
for i in list_items:
    print i.name