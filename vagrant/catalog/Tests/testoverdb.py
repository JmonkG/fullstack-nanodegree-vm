from FDBSetup import db,User,Category,Item

cat = Category.query.filter_by(name = 'Futbol').first()
'''list_items = Item.query.filter(Category.name == cat.name).all()
for i in list_items:
    print i.name'''
list_items = cat.items.all()
for i in list_items:
    print i.name
    