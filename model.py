"""Models and database functions for Sasha's Unnamed Project."""

from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()

###############################################################################
# Model Definitions


class Location(db.Model):
    """U.S. locations matched by state ID, congressional district, & state name."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(15), nullable=False)
    elected_reps = db.relationship("ElectedRep", backref=db.backref("location"))
    zipcode = db.relationship("Zipcode", backref=db.backref("location"))
    citizen_groups = db.relationship("CitizenGroup", backref=db.backref("location"))

    def __repr__(self):
        return "<Location: location_id: %d, district_id: %d, state_name: %s>" % (
            self.location_id, self.district_id, self.state_name)


class CitizenGroup(db.Model):
    """Employed U.S. citizens grouped by male/female & all jobs/management jobs."""

    __tablename__ = "citizen_groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    female = db.Column(db.Boolean, nullable=False)
    manager = db.Column(db.Boolean, nullable=False)
    population = db.Column(db.Float, nullable=True)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)

    # @staticmethod
    # def get_chart_employee

    def __repr__(self):
        return "<Citizen: Female: %s, Manager: %s, Population: %r, dist_id: %r, state: %s >" % (
            self.female, self.manager, self.population, self.district_id, self.state_name)


class ElectedRep(db.Model):

    __tablename__ = "elected_reps"

    official_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rep_type = db.Column(db.String(10), nullable=False)
    female = db.Column(db.Boolean, nullable=False)
    state_name = db.Column(db.String(20), nullable=False)
    district_id = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)

    def __repr__(self):
        return "<ElectedRep: RepType: %s, Female: %s, dist_id: %d, state: %s>" % (
            self.rep_type, self.female, self.district_id, self.state_name)


class Zipcode(db.Model):

    __tablename__ = "zipcodes"

    z_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zipcode = db.Column(db.Integer, nullable=False)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(20), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)

    def __repr__(self):
        return "<Zipcode: %d, dist_id: %d, state_name: %s>" % (
            self.zipcode, self.district_id, self.state_name)


##############################################################################
# Helper functions

def example_data():
    """Create sample data for testing app."""

    # add some sample locations
    loc1 = Location(location_id=101, district_id=1, state_name='Alabama')
    loc2 = Location(location_id=401, district_id=1, state_name='Arizona')
    loc3 = Location(location_id=613, district_id=13, state_name='California')
    loc4 = Location(location_id=5301, district_id=1, state_name='Washington')
    loc5 = Location(location_id=5600, district_id=0, state_name='Wyoming')

    # add sample citizen data

    al1 = CitizenGroup(group_id=1,
                       female=False,
                       manager=False,
                       population=112641,
                       district_id=1,
                       state_name='Alabama',
                       year=2015)

    al2 = CitizenGroup(group_id=436,
                       female=False,
                       manager=True,
                       population=7834,
                       district_id=1,
                       state_name='Alabama',
                       year=2015)

    al3 = CitizenGroup(group_id=871,
                       female=True,
                       manager=False,
                       population=90000,
                       district_id=1,
                       state_name='Alabama',
                       year=2015)

    al4 = CitizenGroup(group_id=1306,
                       female=True,
                       manager=True,
                       population=4600,
                       district_id=1,
                       state_name='Alabama',
                       year=2015)


    az1 = CitizenGroup(group_id=9,
                       female=False,
                       manager=False,
                       population=100000,
                       district_id=1,
                       state_name='Arizona',
                       year=2015)

    az2 = CitizenGroup(group_id=444,
                       female=False,
                       manager=True,
                       population=6204,
                       district_id=1,
                       state_name='Arizona',
                       year=2015)

    az3 = CitizenGroup(group_id=879,
                       female=True,
                       manager=False,
                       population=77000,
                       district_id=1,
                       state_name='Arizona',
                       year=2015)

    az4 = CitizenGroup(group_id=1314,
                       female=True,
                       manager=True,
                       population=5000,
                       district_id=1,
                       state_name='Arizona',
                       year=2015)


    ca1 = CitizenGroup(group_id=22,
                       female=False,
                       manager=False,
                       population=98000,
                       district_id=1,
                       state_name='California',
                       year=2015)

    ca2  = CitizenGroup(group_id=457,
                       female=False,
                       manager=True,
                       population=6900,
                       district_id=1,
                       state_name='California',
                       year=2015)

    ca3 = CitizenGroup(group_id=892,
                       female=True,
                       manager=False,
                       population=70000,
                       district_id=1,
                       state_name='California',
                       year=2015)

    ca4 = CitizenGroup(group_id=1327,
                       female=True,
                       manager=True,
                       population=5118,
                       district_id=1,
                       state_name='California',
                       year=2015)


    wa1 = CitizenGroup(group_id=414,
                       female=False,
                       manager=False,
                       population=160000,
                       district_id=1,
                       state_name='Washington',
                       year=2015)

    wa2 = CitizenGroup(group_id=849,
                       female=False,
                       manager=True,
                       population=15000,
                       district_id=1,
                       state_name='California',
                       year=2015)

    wa3 = CitizenGroup(group_id=1284,
                       female=True,
                       manager=False,
                       population=94000,
                       district_id=1,
                       state_name='Washington',
                       year=2015)

    wa4 = CitizenGroup(group_id=1719,
                       female=True,
                       manager=True,
                       population=9999,
                       district_id=1,
                       state_name='California',
                       year=2015)


    wy1 = CitizenGroup(group_id=435,
                       female=False,
                       manager=False,
                       population=142000,
                       district_id=0,
                       state_name='Wyoming',
                       year=2015)

    wy2 = CitizenGroup(group_id=870,
                       female=False,
                       manager=True,
                       population=7389,
                       district_id=1,
                       state_name='Wyoming',
                       year=2015)

    wy3 = CitizenGroup(group_id=1305,
                       female=True,
                       manager=False,
                       population=83000,
                       district_id=1,
                       state_name='Wyoming',
                       year=2015)

    wy4 = CitizenGroup(group_id=1740,
                       female=True,
                       manager=True,
                       population=6130,
                       district_id=1,
                       state_name='Wyoming',
                       year=2015)

    # add sample zipcode data



def connect_to_db(app, db_uri="postgresql:///jobs"):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."
