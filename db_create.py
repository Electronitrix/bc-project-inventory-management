from app import db
from models import Staff, Asset

# create the database and the db talbes
db.create_all()

# insert
#no_asset = db.session.add(Asset("--", "--", "--", "--"))

astaff = Staff(firstname="chukwuerika", lastname="dike", email="chukwuerikadike@gmail.com", staffno="3719", dept="ops and facilities", role="super-admin",  password="master")
bstaff = Staff(firstname="erika", lastname="dike", email="rikkydyke@yahoo.co.uk", staffno="4077", dept="technical", role="user", password="master")
cstaff = Staff(firstname="rikky", lastname="dyke", email="rikkydyke@live.co.uk", staffno="2933", dept="ops and facilities", role="admin", password="master")

db.session.add(astaff)
db.session.add(bstaff)
db.session.add(cstaff)

db.session.add(Asset(name="laptop", serialno="hgemreb", assetno="and/ff/c007", reclaim_on="29/02/2016", is_missing=False, author=astaff))
db.session.add(Asset(name="projector", serialno="tcexde", assetno="and/ff/c008", reclaim_on="29/02/2016", is_missing=False, author=astaff))
db.session.add(Asset(name="network switch", serialno="h82-123", assetno="and/ff/c010", reclaim_on="29/02/2016", is_missing=False, author=bstaff))
db.session.add(Asset(name="bluetooth speakers", serialno="873-trg-1", assetno="and/ff/c001", reclaim_on="29/02/2016", is_missing=False, author=bstaff))

db.session.add(Asset(name="usb flash", serialno="ymdrj-1j", assetno="and/ef/b101", reclaim_on="--/--/----", is_missing=False, author=bstaff))
db.session.add(Asset(name="pen drive", serialno="jkml-1st", assetno="and/ef/b102", reclaim_on="--/--/----", is_missing=True, author=bstaff))
db.session.add(Asset(name="ipad", serialno="hfem734-1", assetno="and/ff/c0902", reclaim_on="--/--/----", is_missing=True, author=cstaff))

# commit the changes
db.session.commit()