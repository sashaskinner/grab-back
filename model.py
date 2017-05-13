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
    # elected_reps = db.relationship("ElectedRep")

    def __repr__(self):
        return "<Location: location_id=%s, district_id=%s, state_name=%s>" % (
            str(location_id), str(district_id), state_name)


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
        return "<Citizen: Type things here later.>"

# class ElectedRep(db.Model):

#     __tablename__ = "elected_reps"

#     official_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)
#     rep_type = db.Column(db.String(10), nullable=False)
#     female = db.Column(db.Boolean, nullable=False)
#     state_name = db.Column(db.String(15), nullable=False)
#     year = db.Column(db.Integer)

#     def __repr__(self):
#         return "<ElectedRep: Type things here later.>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///jobs"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
