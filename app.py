from flask import Flask, redirect, url_for, render_template, request
import json
import sys
import os
from flask_sqlalchemy import SQLAlchemy
from wtforms import ValidationError

app = Flask(__name__)

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

# the values of those depend on your setup
POSTGRES_URL = get_env_variable("POSTGRES_URL")
#POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_USER = "postgres"
#POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_PW = "zxcvbnm" 
#POSTGRES_DB = get_env_variable("POSTGRES_DB")
POSTGRES_DB = "test"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)



class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(30))
    institution = db.Column(db.String(50))
    designation = db.Column(db.String(30))

    def __init__(self, name, email, contact, institution, designation):
        self.name = name
        self.email = email
        self.contact = contact
        self.institution = institution
        self.designation = designation



@app.route('/')
def signup():
        return render_template('signup.html')


@app.route('/register', methods=['GET','POST'])
def register_user():
    name = request.args.get('name')
    email = request.args.get('email')
    contact = request.args.get('contact')
    institution = request.args.get('institution')
    designation = request.args.get('designation')

    check = User.query.filter_by(email=email).first()

    if not check:
        user = User(name,email,contact,institution,designation)
        db.session.add(user)
        db.session.commit()
    else:
        return json.dumps({'status': 'Email already taken'})

    return render_template('confirm.html',name= name , email= email)

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
