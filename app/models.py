from . import db

class Property(db.Model):

    __tablename__ = 'property'

    propertyID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(150))
    rooms = db.Column(db.String(10))
    bathrooms = db.Column(db.String(10))
    price = db.Column(db.String(20))
    property_type = db.Column(db.String(20))
    location = db.Column(db.String(150))
    photo = db.Column(db.String(255)) 

    def __init__(self, title, description, rooms, bathrooms, price, property_type, location, photo):
        self.title = title
        self.description = description
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.price = price
        self.property_type = property_type
        self.location = location
        self.photo = photo
        

