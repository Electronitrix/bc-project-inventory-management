from app import db


class Staff(db.Model):
    """Defines fields in the staff table."""

    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=False, 
        nullable=False)
    lastname = db.Column(db.String(64), index=True, unique=False, 
        nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    staffno = db.Column(db.String(64), index=True, unique=True, 
        nullable=False)
    dept = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    assets = db.relationship('Asset', backref='author', lazy='dynamic')

    # def __init__(self, firstname, lastname, email, staffno, dept, role, 
    #     password, assets=[]):
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.email = email
    #     self.staffno = staffno
    #     self.dept = dept
    #     self.role = role
    #     self.password = password
    #     self.assets = assets
   
    def __repr__(self):
        return '<name {} {} >'.format(self.firstname, self.lastname)

class Asset(db.Model):
    """Defines fields in the assets table."""

    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    serialno = db.Column(db.String(120), index=True, unique=True,
     nullable=False)
    assetno = db.Column(db.String(120), index=True, unique=True, 
        nullable=False)
    reclaim_on = db.Column(db.String(64))
    is_missing = db.Column(db.Boolean, unique=False, default=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    
    # def __init__(self, name, serialno, assetno, reclaim_on, user_id, \
    #     is_missing):
    #     self.name = name
    #     self.serialno = serialno
    #     self.assetno = assetno
    #     self.reclaim_on = reclaim_on
    #     self.is_missing = is_missing
    #     self.user_id = user_id

    def __repr__(self):
        return '<Asset {}>'.format(self.name)
