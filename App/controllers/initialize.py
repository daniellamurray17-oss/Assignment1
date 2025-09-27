from App.controllers.user import create_driver, create_resident
from App.database import db

def initialize():
    db.drop_all()
    db.create_all()
    
    # Example: create a driver and a resident
    create_driver('bob', 'bobpass')
    create_resident('alice', 'alicepass')

