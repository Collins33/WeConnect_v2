from app import db

class Business(db.Model):
    __tablename__ = 'businesses'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(300))
    description=db.Column(db.String(1000))
    contact=db.Column(db.String(1000))
    category=db.Column(db.String(300))
    location=db.Column(db.String(300))

    def __init__(self,name,description,contact,category,location):
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



