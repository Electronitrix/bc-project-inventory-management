from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

# create the application object
app = Flask(__name__)
bcrypt = Bcrypt(app)

# config
app.config.from_object('config.BaseConfig')

# create the sqlalchemy object
db = SQLAlchemy(app)

# import db schema
from models import *

def login_required(f):
    """Login required decorator"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required  # require login
def index():
    return render_template("index.html")

@app.route('/home')
@login_required  # require login
def home():
    return render_template("home.html")

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        staff_object = Staff.query.filter_by(email=request.form['username'])\
                    .first()
        if staff_object.password == request.form['password']:
            session["logged_in"] = True
            flash('You were just logged in!')
            
            if staff_object.role == "user":
                staff_assets = staff_object.assets.all()
                return render_template('home.html',
                                        staff=staff_object,
                                        assets=staff_assets)


        error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required  # require login
def logout():
    session.pop("logged_in", None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

# start the server with the 'run()' method
if __name__ == "__main__":
    app.run()