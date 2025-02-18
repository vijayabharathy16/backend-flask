from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(200), unique=True, nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(100), unique=True) 
    
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'address':self.address,
            'contact':self.contact  
        }
    
                                                                                                                                        
