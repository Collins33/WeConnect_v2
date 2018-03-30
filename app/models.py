from app import db

class Business(db.Model):
    __tablename__ = 'businesses'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(300))
    description=db.Column(db.String(1000))
    contact=db.Column(db.String(1000))
    category=db.Column(db.String(300))
    location=db.Column(db.String(300))

    

