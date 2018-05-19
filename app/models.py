from app import db
from flask_bcrypt import Bcrypt
import jwt
from flask import current_app
from datetime import datetime, timedelta
import re

class Access_token(db.Model):
    __tablename__= 'access_tokens'
    id=db.Column(db.Integer,primary_key=True)
    token=db.Column(db.String(1000),nullable=False,unique=True)

    def __init__(self,token):
        self.token=token

    def save(self):
        db.session.add(self)
        db.session.commit()

class User(db.Model):
    __tablename__= 'users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(300), nullable=False, unique=True)
    password=db.Column(db.String(300),nullable=False)
    #one to many relationship with business
    businesses=db.relationship("Business",order_by='Business.id',cascade="all,delete-orphan")

    def __init__(self,email,password):
        self.email=email
        self.password=Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self,password):
        """compare password against its hash version"""
        """will return true if they match"""
        return Bcrypt().check_password_hash(self.password,password)

    def save(self):
        """save a user to the database"""
        db.session.add(self)
        db.session.commit()

    def generate_token(self,user_id):
        """this method generates the user token
        using the user_id"""
        try:
            #first create the payload
            payload={
                'exp':datetime.utcnow() + timedelta(minutes=100),
                'iat':datetime.utcnow(),
                'sub':user_id
            }
            #create the byte string token
            jwt_string=jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """this method takes token as argument
        and checks if it is valid"""
        try:
            #decode using secret key
            payload=jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
        #if the token is expired
            return "Expired token. Login to get a new token"
        except jwt.InvalidTokenError:
            #if token is invalid
            return "Invalid token. Please register or login"

    @staticmethod
    def validate_email(email):
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return True
        return False

    @staticmethod
    def validate_password_length(password):
        if len(password) > 6:
            return True
        return False

    @staticmethod
    def validate_password_format(password):
        if re.match(r"^[A-Za-z0-9\.\+_-]*$",password):
            return True
        return False    

class Business(db.Model):
    __tablename__ = 'businesses'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(300))
    description=db.Column(db.String(1000))
    contact=db.Column(db.String(1000))
    category=db.Column(db.String(300))
    location=db.Column(db.String(300))
    business_owner=db.Column(db.Integer,db.ForeignKey(User.id))
    review=db.relationship('Review',order_by="Review.id", cascade="all, delete-orphan")

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

    @staticmethod
    def get_business_by_name(name):
        """this method should return list with business that matches the name"""
        return Business.query.filter_by(name=name).first()    

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

    @staticmethod
    def validate_business_details(detail):
        if re.match(r"^[A-Za-z0-9\.\+_-]*$",detail):
            return True
        return False

    @staticmethod
    def check_business_exists(id):
        return Business.query.filter_by(id=id)
         
class Review(db.Model):
    __tablename__ = 'reviews'
    id=db.Column(db.Integer,primary_key=True)
    opinion=db.Column(db.String(300))
    rating=db.Column(db.Integer)
    business_main=db.Column(db.Integer,db.ForeignKey(Business.id))

    def __init__(self,opinion,rating,business_main):
        self.business_main=business_main
        self.opinion=opinion
        self.rating = rating

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all_reviews():
        """return all reviews"""
        return Review.query.all()

    @staticmethod
    def get_business_review(id):
        #get reviews for a particular business
        return Review.query.filter_by(business_main=id)    





              



