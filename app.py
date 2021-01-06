from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://walysjiyxzfazn:1b6117eda79b010c624e9213c8f398dc3540039971cd87da0a3e95330785593c@ec2-23-20-205-19.compute-1.amazonaws.com:5432/d59hsjiri0tl1"


db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

CORS(app)
Heroku(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class userSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")


user_schema = userSchema()
multiple_user_schema = userSchema(many=True) 


@app.route("/user/add", methods=["POST"])
def create_user():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    

        
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    record = User(username,password_hash)
    db.session.add(record)
    db.session.commit()

    return jsonify("User added successfully")

@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))

@app.route("/user/authentication", methods=["POST"])
def user_authentication():
     if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

     post_data = request.get_json()
     username = post_data.get("username")
     password = post_data.get("password")

     user = db.session.query(User).filter(User.username == username).first()

     if user is None:
         return jsonify("FAILED")

     if bcrypt.check_password_hash(user.password, password) != True:
        return jsonify("FAILED")

     return jsonify("SUCCESS")

     

     











if __name__ =="__main__":
    app.run(debug=True)