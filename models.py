from app import db

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(30))
    institution = db.Column(db.String(50))
    designation = db.Column(db.String(30))

    def __init__(self, name=None, email=None, mobile=None, institution=None, designation=None):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.institution = institution
        self.designation = designation
    
