"""Flask server for Sasha's unnamed Hackbright project."""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import os
import json
import numpy as np

from model import Location, CitizenGroup, ElectedRep, Zipcode, connect_to_db, db

app = Flask(__name__)

# Secret key for Flask session and debug toolbar.
FLASK_KEY = os.environ['FLASK_KEY']

app.secret_key = FLASK_KEY


# app routes
@app.route('/')
def index():
    """Index page."""

    return render_template("home.html")


@app.route('/us.json')
def us_json():
    """JSON file with US map specs."""

    return render_template("us.json")


@app.route('/us-congress-113.json')
def us_congress_113():
    """JSON file with congressional district shapes for us map."""

    return render_template("us-congress-113.json")


@app.route('/district-manager-info.json')
def get_manager_info():
    """Query db for population info: Management Employees.

        max-value: 62%, min-value: 28%

    """

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # MANAGERS
    f_data = has_pop.filter_by(female=True, manager=True).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=True).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return jsonify(data_dict)


@app.route('/district-employee-info.json')
def get_employee_info():
    """Query db for population info: All Employees.

    max-value: 52%, min-value: 33%

    """

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # ALL EMPLOYED PERSONS
    f_data = has_pop.filter_by(female=True, manager=False).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=False).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return jsonify(data_dict)

@app.route('/district-congress-info.json')
def get_congress_info():
    """Query db for population info: Congress Reps

        max-value: 100%, min-value: 0%
    """

    rep_q = db.session.query(
        ElectedRep.location_id,
        ElectedRep.state_name,
        ElectedRep.rep_type,
        ElectedRep.female)

    # U.S. CONGRESS REPS
    all_reps = rep_q.all()
    all_senate = rep_q.filter_by(rep_type="senate").all()
    all_house = rep_q.filter_by(rep_type="house").all()

    total_reps = int(rep_q.count())
    f_reps = int(rep_q.filter_by(female=True).count())
    m_reps = int(rep_q.filter_by(female=False).count())

    rep_lst = []
    senate_lst = []
    house_lst = []

    rep_types = [all_reps, all_senate, all_house]
    for this_list in rep_types:
        for item in this_list:
            item_lst = []
            for i in range(len(item)):
                item_lst.append(item[i])

            if this_list == all_reps:
                rep_lst.append(item_lst)
                rep_types[0] = rep_lst
            elif this_list == all_senate:
                senate_lst.append(item_lst)
                rep_types[1] = senate_lst
            elif this_list == all_house:
                house_lst.append(item_lst)
                rep_types[2] = house_lst

    for item in senate_lst:
        if item[3] == True:
            item[3] = 1
        else:
            item[3] = 0

    for item in house_lst:
        if item[3] == True:
            item[3] = 1
        else:
            item[3] = 0

    # create dict with number all congress members and number female by district
    district_dict = {}
    for dist in house_lst:
        district_dict[dist[0]] = {'women': 0, 'all': 0}

    # add house members to district dict
    for rep in house_lst:
        for key in district_dict:
            if rep[0] == key:
                district_dict[key]['all'] += 1
                district_dict[key]['women'] += rep[3]

    # add states to district dict to map senators to districts
    for item in rep_lst:
        for key in district_dict:
            if item[0] == key:
                district_dict[key]['state'] = item[1]

    # add senators to district dict
    for rep in senate_lst:
        for key in district_dict:
            if rep[1] == district_dict[key]['state']:
                district_dict[key]['all'] += 1
                district_dict[key]['women'] += rep[3]

    # create dict to hold dist id and percentage of women us congress reps
    data_dict = {}
    for key in district_dict:
        data_dict[key] = district_dict[key]['women']/float(district_dict[key]['all'])

    return jsonify(data_dict)


@app.route('/chart-data-employee')
def get_chart_data_employee():
    """Get data from db query to populate chart. """

    data_dict = get_chart_employee()

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=True)
    data_dict_transfer = data_dict_transfer[0:6]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        chart_data.append(item[1])

    all_data = []
    all_data.append(chart_labels)
    all_data.append(chart_data)

    return jsonify(all_data)


@app.route('/chart-data-employee-reverse')
def get_reverse_data_employee():
    """Get data from db query to populate bottom districts chart. """

    data_dict = get_chart_employee()

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=False)
    data_dict_transfer = data_dict_transfer[0:6]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        chart_data.append(item[1])

    all_data = []
    all_data.append(chart_labels)
    all_data.append(chart_data)

    return jsonify(all_data)


@app.route('/chart-data-manager')
def get_chart_data_manager():
    """Get data from db query to populate chart. """

    data_dict = get_chart_manager()

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=True)
    data_dict_transfer = data_dict_transfer[0:6]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        chart_data.append(item[1])

    all_data = []
    all_data.append(chart_labels)
    all_data.append(chart_data)

    return jsonify(all_data)


@app.route('/chart-data-manager-reverse')
def get_reverse_data_manager():
    """Get data from db query to populate bottom districts chart. """

    data_dict = get_chart_manager()

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=False)
    data_dict_transfer = data_dict_transfer[0:6]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        chart_data.append(item[1])

    all_data = []
    all_data.append(chart_labels)
    all_data.append(chart_data)

    return jsonify(all_data)


########### ZIPCODE LOOKUP QUERIES & ROUTES

@app.route('/zipcode-lookup.json', methods=['GET'])
def get_district_from_zipcode():
    """Get location_id from zipcode entry."""

    z = request.args.get("zipcode-entry")
    z = int(z)

    lookup_id = db.session.query(Zipcode.location_id).filter_by(zipcode=z).first()
    district_lookup = db.session.query(Zipcode.state_name, Zipcode.district_id).filter_by(zipcode=z).first()

    lookup_state = str(district_lookup[0])
    lookup_dist = int(district_lookup[1])

    data_dict = get_chart_employee()

    # convert SQLAlchemy search result to int
    lookup_id = np.array(lookup_id)
    lookup_id = lookup_id[0]
    lookup_id = int(lookup_id)

    lookup_percent = data_dict[lookup_id] * 100

    lookup_percent = str(lookup_percent) + '%'

    return jsonify({'lookup_id': lookup_id, 'lookup_percent': lookup_percent,
                    'lookup_state': lookup_state, 'lookup_dist': lookup_dist})


########### HELPER FUNCTIONS

def get_location_details():
    """Get state name and district ID for a location ID. """

    location_deets = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.state_name,
        CitizenGroup.district_id).filter(CitizenGroup.population.isnot(None))




def get_chart_employee():
    """   """
    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # ALL EMPLOYED PERSONS POPULATION & DISTRICT INFO
    f_data = has_pop.filter_by(female=True, manager=False).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=False).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return data_dict


def get_chart_manager():
    """Get manager data for Chart.js bar graph."""

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # ALL EMPLOYED PERSONS
    f_data = has_pop.filter_by(female=True, manager=True).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=True).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return data_dict


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
