from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import sys
import os
from flask_sqlalchemy import SQLAlchemy
from wtforms import ValidationError
from flask import make_response
import jwt
import datetime
from functools import wraps
from flask_pymongo import PyMongo


app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'jwtdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/jwtdb'
app.config['SECRET_KEY'] = 'secretkey'

app.url_map.strict_slashes = False

mongo = PyMongo(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({"message" : "Token is missing"}) , 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : token}) , 403
        
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['GET','POST'])
@token_required
def register_user():
    name = request.args.get('name')
    email = request.args.get('email')
    contact = request.args.get('contact')
    institution = request.args.get('institution')
    designation = request.args.get('designation')
    
    ref = mongo.db.USER
    user = ref.find_one({'email' : email})
    if user:
        return jsonify({'status': 'Email already taken'})
    else:
        token  = jwt.encode({'email' : email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        res = make_response("Registration Successful")
        res.set_cookie('token' , token)
        ref.insert({'name' : name,'email' : email,'contact' : contact,'institution' : institution,'designation' : designation})
        #return render_template('confirm.html',name= name , email= email)
        return res
    

@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    print('Creating tables.')
    db.create_all()
    print('Shiny!')


if __name__ == "__main__":
    app.run(debug=True)
