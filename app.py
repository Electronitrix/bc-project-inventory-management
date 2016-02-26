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
            session["username"] = staff_object.firstname.capitalize() + \
                " " + staff_object.lastname.capitalize()
            
            staff_assets = staff_object.assets.all()
            return render_template('home.html',
                                    staff=staff_object,
                                    assets=staff_assets)

        error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/assets')
@login_required  # require login
def assets():
    all_assets = Asset.query.all()
    staff = []
    for asset in all_assets:
        astaff = Staff.query.filter_by(id=asset.staff_id).first()
        staff_name = astaff.firstname.capitalize() + " " + astaff.lastname.capitalize()
        posessor.append(staff_name)

    return render_template('assets.html',
                            staff=staff,
                            assets=all_assets)

@app.route('/assign_asset', methods=['GET', 'POST'])
@login_required  # require login
def assign_asset():
    """Assign asset to a staff"""
    error = None
    if request.method = 'POST':
        asset_object = Asset.query.filter_by(name=request.form['asset']) \
                        .first()
        staff_firstname = request.form['staff'].split()[].lower()  # get firstname and make lowercase
        staff_object = User.query.filter_by(firstname=request.form['name']) \
                        .first()
        asset_object.author = staff_object
        db.session.commit()

    return redirect(url_for('assets'))

@app.route('/reclaim_asset', methods=['GET', 'POST'])
@login_required  # require login
def reclaim_asset():
    """Reclaim asset from a staff and return to storage"""
    error = None
    if request.method == 'POST':
        asset_object = Asset.query.filter_by(name=request.form['asset']) \
                        .first()
        staff_object = User.query.filter_by(firstname="storage").first()
        asset_object.author = staff_object
        db.session.commit()

    return redirect(url_for('assets'))

@app.route('/lost')
@login_required  # require login
def lost():
    """
    Searches database for lost assets 
    then renders html to display them

    Return:
    assets - a list of all missing assets
    """
    lost_assets = Asset.query.filter_by(is_missing=True).all()
    
    return render_template('assets.html',
                            assets=all_assets)

@app.route('create_asset', methods=['GET', 'POST'])
@login_required  # require login
def create_asset():
    """Update database with new asset record"""
    error = None
    if request.method == 'POST':
        storage_object = Staff.query.filter_by(firstname="storage").first()
        new_asset = Asset(name=request.form['name'], serialno=request.form['serial_no'], 
                            assetno=request.form['asset_no'], reclaim_on="--/--/----", 
                            is_missing=False, author=storage_object)
        db.session.add(new_asset)
        db.session.commit()

        return redirect(url_for('assets'))

@app.route('mark_as_found', methods=['GET', 'POST'])
@login_required  # require login
def mark_as_found():
    """Updates is_missing field on database to False"""
    error = None
    if request.method == 'POST':
        is_selected = request.form.getlist('is_selected')
        if bool(is_selected):
            asset_object = Asset.query.filter_by(
                            serialno=request.form['asset_serial_no']).first()
            asset_object.is_missing = False
            db.session.commit()
        return redirect(url_for('lost'))

@app.route('report_found', methods=['GET', 'POST'])
@login_required # require login
def report_found():
    """
    Logs users reports that an asset has been found to found_reports table
    """
    error = None
    if request.method == 'POST':
        asset_object = Asset.query.filter_by(id=request.form['id']) \
                        first()
        new_found = FoundReport(name=asset_object.name, 
                                serialno=asset_object.serialno, 
                                assetno=asset_object.assetno)
        db.session.add(new_found)
        db.seesion.commit()

        return redirect(url_for('home'))

@app.route('report_missing', methods=['GET', 'POST'])
@login_required # require login
def report_missing():
    """
    Logs users reports that an asset is missing to missing_reports table
    """
    error = None
    if request.method == 'POST':
        asset_object = Asset.query.filter_by(id=request.form['id']) \
                        first()
        new_missing = FoundReport(name=asset_object.name, 
                                serialno=asset_object.serialno, 
                                assetno=asset_object.assetno)
        db.session.add(new_missing)
        db.seesion.commit()

        return redirect(url_for('home'))

@app.route

@app.route('change_role', methods=['GET', 'POST'])
@login_required  # require login
def change_role():
    """
    Changes role of a staff to either user, admin or super-admin
    """
    error = None
    if request.method == 'POST':
        asset_object = Asset.query.filter_by(id=request.form['id']) \
                        .first()
        asset_object.role = request.form['role']
        db.session.commit()
        return redirect(url_for('staff'))

@app.route('/logout')
@login_required  # require login
def logout():
    session.pop("logged_in", None)
    return redirect(url_for('login'))

# start the server with the 'run()' method
if __name__ == "__main__":
    app.run()