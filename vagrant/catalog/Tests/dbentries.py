from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,User,Category,Item

engine = create_engine('sqlite:///projectws.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name = "peter",password = "peter",email_address ="pit@pit.com")
session.add(user1)
session.commit()
user2 = session.query(User).filter(User.name == 'peter').first()
user2.name = 'Melinita'
session.add(user2)
session.commit()

