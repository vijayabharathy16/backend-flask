from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:MSfamily@localhost:5432/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
# Model Definition
class Users(db.Model):
    table_name = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, email, address, contact):
        self.name = name
        self.email = email
        self.address = address
        self.contact = contact

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Schema Definition
class FlaskdbSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    address = fields.String()
    contact = fields.String()

# Initialize Schema
flaskdb_schema = FlaskdbSchema()
flaskdbs_schema = FlaskdbSchema(many=True)

# Routes
@app.route('/allusers', methods=['GET'])
def get_all():
    flasks = Users.get_all()
    data = flaskdbs_schema.dump(flasks)
    return jsonify(data)

@app.route('/add', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Users(
        name=data.get('name'),
        email=data.get('email'),
        address=data.get('address'),
        contact=data.get('contact')
    )
    new_user.save()
    serializer=FlaskdbSchema()
    data = serializer.dump(new_user)
    
    return jsonify(data), 201

@app.route('/oneuser/<int:id>',methods=['GET'])
def get_one(id):
    oneUser = Users.get_by_id(id)

    serializer=FlaskdbSchema()

    data=serializer.dump(oneUser)

    return jsonify(
        data
    ),200

@app.route('/editUser/<int:id>',methods=['PUT'])
def update_user(id):
    change_to_update = Users.get_by_id(id)
    
    data = request.get_json()
    
    change_to_update.name = data.get('name')
    change_to_update.email = data.get('email')
    change_to_update.address = data.get('address')
    change_to_update.contact = data.get('contact')

    db.session.commit()
    serializer=FlaskdbSchema()
    update_data=serializer.dump(change_to_update)
    
    return jsonify(update_data),200

@app.route('/deleteUser/<int:id>',methods=['DELETE'])
def delete_user(id):
    delete_to_data = Users.get_by_id(id)
    
    delete_to_data.delete()
    return jsonify({"message":"Delected successfully"}),204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


