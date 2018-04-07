from app import db
from flask_bcrypt import Bcrypt

class User(db.Model):
    __tablename__= 'users'

    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(300), nullable=False, unique=True)
    password=db.Column(db.String(300),nullable=False)
    confirm_password=db.Column(db.String(300),nullable=False)
    """one to many relationship with business"""
    businesses=db.relationship("Businesses",order_by='Business.id',cascade="all,delete-orphan") 

class Business(db.Model):
    __tablename__ = 'businesses'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(300))
    description=db.Column(db.String(1000))
    contact=db.Column(db.String(1000))
    category=db.Column(db.String(300))
    location=db.Column(db.String(300))
    business_owner=db.Column(db.Integer,db.ForeignKey(User.id))

    def __init__(self,name,description,contact,category,location,business_owner):

        """initialize with the business owner"""
        self.business_owner=business_owner
        self.name=name
        self.description=description
        self.contact=contact
        self.category=category
        self.location=location


    def save(self):
        """save business to database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """returns all businesses"""
        return Business.query.all()

    @staticmethod
    def get(owner):
        """this gets all the business for a particular user"""
        return Business.query.filter_by(business_owner=owner)    

    def delete_business(self):
        """deletes a business"""
        db.session.delete(self)
        db.session.commit() 

    def __repr__(self):
        return "<Business: {}>".format(self.name)

    @staticmethod
    def get_business_location(location):
        """returns businesses that match the location"""
        """will return list of businesses"""

        return Business.query.filter_by(location=location)

    @staticmethod
    def get_business_category(category):
        """return businesses that match the category"""
        return Business.query.filter_by(category=category)


              



