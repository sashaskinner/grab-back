from model import Location
from model import CitizenGroup
from model import Zipcode

from model import connect_to_db, db
from server import app

import csv


def load_locations():
    """Load data from locations.csv into locations table in db."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Location.query.delete()

    with file('seed_data/location.csv', 'rb') as f:
        reader = csv.reader(f)
        location_list = list(reader)
        del location_list[0]

    # Read location list and insert data

    d = {}

    for row in location_list:
        location_id, district_id, state_name = row

        d[location_id] = [district_id, state_name]

        if district_id == '':
            loc = Location(location_id=location_id,
                           district_id=None,
                           state_name=state_name)
        else:
            loc = Location(location_id=location_id,
                           district_id=district_id,
                           state_name=state_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(loc)

    # Once we're done, we should commit our work
    db.session.commit()


def load_citizen_groups():
    """Load data from citizens.csv into CitizenGroup table in db."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    CitizenGroup.query.delete()

    with file('seed_data/citizens-2014.csv', 'rb') as f:
        reader = csv.reader(f)
        citizens_list = list(reader)
        del citizens_list[0]

    # Read location list and insert data
    for row in citizens_list:

        group_id, female, manager, population, district_id, state_name, year = row

        q = db.session.query(Location.location_id).filter_by(district_id=district_id,
                                                             state_name=state_name).one()

        if population == '':
            cit = CitizenGroup(group_id=group_id,
                               female=female,
                               manager=manager,
                               population=None,
                               district_id=district_id,
                               state_name=state_name,
                               year=year,
                               location_id=q)

        else:
            cit = CitizenGroup(group_id=group_id,
                               female=female,
                               manager=manager,
                               population=population,
                               district_id=district_id,
                               state_name=state_name,
                               year=year,
                               location_id=q)

        # We need to add to the session or it won't ever be stored
        db.session.add(cit)

    # Once we're done, we should commit our work
    db.session.commit()


def load_zipcodes():

    with file('seed_data/zipcode.csv', 'rb') as f:
        reader = csv.reader(f)
        zip_list = list(reader)
        del zip_list[0]

    for row in zip_list:

        z_id, zipcode, district_id, state_name = row

        q = db.session.query(Location.location_id).filter_by(district_id=int(district_id), state_name=state_name).first()

        zips = Zipcode(z_id=z_id,
                       zipcode=zipcode,
                       district_id=district_id,
                       state_name=state_name,
                       location_id=q)

        db.session.add(zips)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    #In case tables haven't been created, create them
    db.create_all()

    # # Import different types of data
    load_locations()
    load_citizen_groups()
    load_zipcodes()
