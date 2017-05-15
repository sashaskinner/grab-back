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
    elected_reps = db.relationship("ElectedRep")

    def __repr__(self):
        return "<Location: location_id: %d, district_id: %d, state_name: %s>" % (
            location_id, district_id, state_name)


class CitizenGroup(db.Model):
    """Employed U.S. citizens grouped by male/female & all jobs/management jobs."""

    __tablename__ = "citizen_groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    female = db.Column(db.Boolean, nullable=False)
    manager = db.Column(db.Boolean, nullable=False)
    population = db.Column(db.Integer, nullable=True)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(20), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)
    location = db.relationship("Location", backref=db.backref("citizen_groups"))

    def __repr__(self):
        return "<Citizen: Female: %s, Manager: %s, Population: %d, dist_id: %d, state: %s >" % (
            female, manager, population, district_id, state_name)


class ElectedRep(db.Model):

    __tablename__ = "elected_reps"

    official_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rep_type = db.Column(db.String(10), nullable=False)
    female = db.Column(db.Boolean, nullable=False)
    state_name = db.Column(db.String(20), nullable=False)
    district_id = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)
    location = db.relationship("Location")

    def __repr__(self):
        return "<ElectedRep: RepType: %s, Female: %s, dist_id: %d, state: %s>" % (
            rep_type, female, district_id, state_name)


class Zipcode(db.Model):

    __tablename__ = "zipcodes"

    z_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zipcode = db.Column(db.Integer, nullable=False)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(20), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)
    location = db.relationship("Location", backref=db.backref("zipcode"))

    def __repr__(self):
        return "<Zipcode: %d, dist_id: %d, state_name: %s>" % (
            zipcode, district_id, state_name)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///jobs"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
