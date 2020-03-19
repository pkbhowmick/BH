from flask import Flask, redirect, url_for, render_template, request
import json
import sys
import os
from flask_sqlalchemy import SQLAlchemy
from models import *
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
POSTGRES_PW = "dbpw" 
#POSTGRES_DB = get_env_variable("POSTGRES_DB")
POSTGRES_DB = "test"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

@app.route('/')
def signup():
        return render_template('signup.html')

@app.route('/register', methods=['GET','POST'])
def register_guest():
    name = request.form.get('name')
    email = request.form.get('email')
    contact = request.form.get('contact')
    institution = request.form.get('institution')
    designation = request.form.get('designation')

    user = User(name, email,contact,institution,designation)
    db.session.add(user)
    db.session.commit()

    return render_template('confirm.html', name=name, email=email)

if __name__ == "__main__":
    app.run(debug=True)
