"""Models and database functions for Sasha's Unnamed Project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################
# Model Definitions


class Location(db.Model):
    """U.S. locations matched by state ID, congressional district, & state name."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(15), nullable=False)
    zipcode = db.relationship("Zipcode", backref=db.backref("location"))
    citizen_groups = db.relationship("CitizenGroup", backref=db.backref("location"))

    # def __repr__(self):
    #     return "<Location: location_id: %s, district_id: %s, state_name: %s>" % (
    #         self.location_id, self.district_id, self.state_name)


class CitizenGroup(db.Model):
    """Employed U.S. citizens grouped by male/female & all jobs/management jobs."""

    __tablename__ = "citizen_groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    female = db.Column(db.String(20), nullable=False)
    manager = db.Column(db.String(20), nullable=False)
    population = db.Column(db.Float, nullable=True)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)

    # @staticmethod
    # def get_chart_employee

    # def __repr__(self):
    #     return "<Citizen: Female: %s, Manager: %s, Population: %r, dist_id: %r, state: %s >" % (
    #         self.female, self.manager, self.population, self.district_id, self.state_name)


class Zipcode(db.Model):

    __tablename__ = "zipcodes"

    z_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zipcode = db.Column(db.Integer, nullable=False)
    district_id = db.Column(db.Integer, nullable=True)
    state_name = db.Column(db.String(20), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)

    # def __repr__(self):
    #     return "<Zipcode: %d, dist_id: %d, state_name: %s>" % (
    #         self.zipcode, self.district_id, self.state_name)


##############################################################################
# Helper functions

def create_example_data():
    """Create sample data for testing app."""

    # add some sample locations
    loc1 = Location(location_id=101, district_id=1, state_name='Alabama')
    loc2 = Location(location_id=401, district_id=1, state_name='Arizona')
    loc3 = Location(location_id=613, district_id=13, state_name='California')
    loc4 = Location(location_id=5301, district_id=1, state_name='Washington')
    loc5 = Location(location_id=5600, district_id=0, state_name='Wyoming')

    db.session.add(loc1)
    db.session.add(loc2)
    db.session.add(loc3)
    db.session.add(loc4)
    db.session.add(loc5)
    db.session.commit()

    # add sample citizen data

    al1 = CitizenGroup(group_id=1,
                       female=False,
                       manager=False,
                       population=112641,
                       district_id=1,
                       state_name='Alabama',
                       year=2015,
                       location_id=101)

    al2 = CitizenGroup(group_id=436,
                       female=False,
                       manager=True,
                       population=7834,
                       district_id=1,
                       state_name='Alabama',
                       year=2015,
                       location_id=101)

    al3 = CitizenGroup(group_id=871,
                       female=True,
                       manager=False,
                       population=90000,
                       district_id=1,
                       state_name='Alabama',
                       year=2015,
                       location_id=101)

    al4 = CitizenGroup(group_id=1306,
                       female=True,
                       manager=True,
                       population=4600,
                       district_id=1,
                       state_name='Alabama',
                       year=2015,
                       location_id=101)

    db.session.add(al1)
    db.session.add(al2)
    db.session.add(al3)
    db.session.add(al4)
    db.session.commit()

    az1 = CitizenGroup(group_id=9,
                       female=False,
                       manager=False,
                       population=100000,
                       district_id=1,
                       state_name='Arizona',
                       year=2015,
                       location_id=401)

    az2 = CitizenGroup(group_id=444,
                       female=False,
                       manager=True,
                       population=6204,
                       district_id=1,
                       state_name='Arizona',
                       year=2015,
                       location_id=401)

    az3 = CitizenGroup(group_id=879,
                       female=True,
                       manager=False,
                       population=77000,
                       district_id=1,
                       state_name='Arizona',
                       year=2015,
                       location_id=401)

    az4 = CitizenGroup(group_id=1314,
                       female=True,
                       manager=True,
                       population=5000,
                       district_id=1,
                       state_name='Arizona',
                       year=2015,
                       location_id=401)

    db.session.add(az1)
    db.session.add(az2)
    db.session.add(az3)
    db.session.add(az4)
    db.session.commit()

    ca1 = CitizenGroup(group_id=22,
                       female=False,
                       manager=False,
                       population=98000,
                       district_id=1,
                       state_name='California',
                       year=2015,
                       location_id=613)

    ca2 = CitizenGroup(group_id=457,
                       female=False,
                       manager=True,
                       population=6900,
                       district_id=1,
                       state_name='California',
                       year=2015,
                       location_id=613)

    ca3 = CitizenGroup(group_id=892,
                       female=True,
                       manager=False,
                       population=70000,
                       district_id=1,
                       state_name='California',
                       year=2015,
                       location_id=613)

    ca4 = CitizenGroup(group_id=1327,
                       female=True,
                       manager=True,
                       population=5118,
                       district_id=1,
                       state_name='California',
                       year=2015,
                       location_id=613)

    db.session.add(ca1)
    db.session.add(ca2)
    db.session.add(ca3)
    db.session.add(ca4)
    db.session.commit()

    wa1 = CitizenGroup(group_id=414,
                       female=False,
                       manager=False,
                       population=160000,
                       district_id=1,
                       state_name='Washington',
                       year=2015,
                       location_id=5301)

    wa2 = CitizenGroup(group_id=849,
                       female=False,
                       manager=True,
                       population=15000,
                       district_id=1,
                       state_name='California',
                       year=2015,
                       location_id=5301)

    wa3 = CitizenGroup(group_id=1284,
                       female=True,
                       manager=False,
                       population=94000,
                       district_id=1,
                       state_name='Washington',
                       year=2015,
                       location_id=5301)

    wa4 = CitizenGroup(group_id=1719,
                       female=True,
                       manager=True,
                       population=9999,
                       district_id=1,
                       state_name='California',
                       year=2015,
                       location_id=5301)

    db.session.add(wa1)
    db.session.add(wa2)
    db.session.add(wa3)
    db.session.add(wa4)
    db.session.commit()

    wy1 = CitizenGroup(group_id=435,
                       female=False,
                       manager=False,
                       population=142000,
                       district_id=0,
                       state_name='Wyoming',
                       year=2015,
                       location_id=5600)

    wy2 = CitizenGroup(group_id=870,
                       female=False,
                       manager=True,
                       population=7389,
                       district_id=1,
                       state_name='Wyoming',
                       year=2015,
                       location_id=5600)

    wy3 = CitizenGroup(group_id=1305,
                       female=True,
                       manager=False,
                       population=83000,
                       district_id=1,
                       state_name='Wyoming',
                       year=2015,
                       location_id=5600)

    wy4 = CitizenGroup(group_id=1740,
                       female=True,
                       manager=True,
                       population=6130,
                       district_id=1,
                       state_name='Wyoming',
                       year=2015,
                       location_id=5600)

    db.session.add(wy1)
    db.session.add(wy2)
    db.session.add(wy3)
    db.session.add(wy4)
    db.session.commit()

    # add sample zipcode data

    zips_al = Zipcode(z_id=440,
                      zipcode=36033,
                      district_id=1,
                      state_name="Alabama",
                      location_id=101)

    zips_az = Zipcode(z_id=883,
                      zipcode=84154,
                      district_id=1,
                      state_name="Arizona",
                      location_id=401)

    zips_ca = Zipcode(z_id=3232,
                      zipcode=94709,
                      district_id=13,
                      state_name="California",
                      location_id=613)

    zips_wa = Zipcode(z_id=3535,
                      zipcode=98034,
                      district_id=1,
                      state_name="Washington",
                      location_id=5301)

    zips_wy = Zipcode(z_id=3971,
                      zipcode=83414,
                      district_id=0,
                      state_name="Wyoming",
                      location_id=5600)

    db.session.add(zips_al)
    db.session.add(zips_az)
    db.session.add(zips_ca)
    db.session.add(zips_wa)
    db.session.add(zips_wy)
    db.session.commit()


def connect_to_db(app, db_uri="postgresql:///jobs"):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to DB.")
    db.create_all()
