"""Flask server for Sasha's unnamed Hackbright project."""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import os
import json
import numpy as np
from sqlalchemy import func

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


@app.route('/about')
def about():
    """About Page"""

    return render_template("about.html")

@app.route('/us.json')
def us_json():
    """JSON file with US map specs."""

    return render_template("us.json")


@app.route('/us-congress-113.json')
def us_congress_113():
    """JSON file with congressional district shapes for us map."""

    return render_template("us-congress-113.json")


@app.route('/district-manager-info.json', methods=['GET'])
def get_manager_info():
    """Query db for population info: Management Employees.

        max-value: 62%, min-value: 28%

    """

    y = request.args.get("year", 2015)
    y = int(y)

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population, CitizenGroup.year).filter(CitizenGroup.population.isnot(None))

    # MANAGERS
    f_data = has_pop.filter_by(female=True, manager=True, year=y).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=True, year=y).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return jsonify(data_dict)


@app.route('/district-employee-info.json', methods=['GET'])
def get_employee_info():
    """Query db for population info: All Employees.

    max-value: 52%, min-value: 33%

    """

    y = request.args.get("year", 2015)
    y = int(y)

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # ALL EMPLOYED PERSONS
    f_data = has_pop.filter_by(female=True, manager=False, year=y).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=False, year=y).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return jsonify(data_dict)


@app.route('/chart-data-employee')
def get_chart_data_employee():
    """Get data from db query to populate chart. """

    y = request.args.get("year", 2015)
    y = int(y)

    data_dict = get_chart_employee(y)
    us_emp_avg = '{:.2f}'.format(get_us_emp_average() * 100)

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=True)
    data_dict_transfer = data_dict_transfer[0:5]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        new_item = item[1] * 100
        new_item = str(new_item)
        new_item = new_item[0:5]
        chart_data.append(float(new_item))

    all_data = []
    all_data.append(chart_labels)
    all_data[0].append("U.S. Average")
    all_data.append(chart_data)
    all_data[1].append(float(us_emp_avg))

    return jsonify(all_data)


@app.route('/chart-data-employee-reverse')
def get_reverse_data_employee():
    """Get data from db query to populate bottom districts chart. """

    y = request.args.get("year", 2015)
    y = int(y)

    data_dict = get_chart_employee(y)
    us_emp_avg = '{:.2f}'.format(get_us_emp_average() * 100)

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=False)
    data_dict_transfer = data_dict_transfer[0:5]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        new_item = item[1] * 100
        new_item = str(new_item)
        new_item = new_item[0:5]
        chart_data.append(float(new_item))

    all_data = []
    all_data.append(chart_labels)
    all_data[0].append("U.S. Average")
    all_data.append(chart_data)
    all_data[1].append(float(us_emp_avg))

    return jsonify(all_data)


@app.route('/chart-data-manager')
def get_chart_data_manager():
    """Get data from db query to populate chart. """

    y = request.args.get("year", 2015)
    y = int(y)

    data_dict = get_chart_manager(y)
    us_manager_avg = '{:.2f}'.format(get_us_manager_average() * 100)

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=True)
    data_dict_transfer = data_dict_transfer[0:5]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        new_item = item[1] * 100
        new_item = str(new_item)
        new_item = new_item[0:5]
        chart_data.append(float(new_item))

    all_data = []
    all_data.append(chart_labels)
    all_data[0].append("U.S. Average")
    all_data.append(chart_data)
    all_data[1].append(float(us_manager_avg))

    return jsonify(all_data)


@app.route('/chart-data-manager-reverse')
def get_reverse_data_manager():
    """Get data from db query to populate bottom districts chart. """

    y = request.args.get("year", 2015)
    y = int(y)

    data_dict = get_chart_manager(y)
    us_manager_avg = '{:.2f}'.format(get_us_manager_average() * 100)

    chart_labels = []
    chart_data = []
    data_dict_transfer = []

    for item in data_dict.items():
        data_dict_transfer.append(item)

    data_dict_transfer = sorted(data_dict_transfer, key=lambda x: x[1], reverse=False)
    data_dict_transfer = data_dict_transfer[0:5]

    chart_labels = []

    for item in data_dict_transfer:
        loc_id = item[0]
        label_info = db.session.query(Location.state_name,
                                      Location.district_id).filter_by(location_id=loc_id).first()

        new_label = str(label_info[0]) + ", District " + str(label_info[1])
        chart_labels.append(new_label)

    for item in data_dict_transfer:
        new_item = item[1] * 100
        new_item = str(new_item)
        new_item = new_item[0:5]
        chart_data.append(float(new_item))

    all_data = []
    all_data.append(chart_labels)
    all_data[0].append("U.S. Average")
    all_data.append(chart_data)
    all_data[1].append(float(us_manager_avg))

    return jsonify(all_data)


########### ZIPCODE LOOKUP QUERIES & ROUTES

@app.route('/zipcode-lookup.json', methods=['GET'])
def get_district_from_zipcode():
    """Get location_id from zipcode entry."""

    z = request.args.get("zipcode-entry")
    z = int(z)

    y = request.args.get("year", 2015)
    y = int(y)

    lookup_id = db.session.query(Zipcode.location_id).filter_by(zipcode=z).first()
    district_lookup = db.session.query(Zipcode.state_name, Zipcode.district_id).filter_by(zipcode=z).first()

    lookup_state = str(district_lookup[0])
    lookup_dist = int(district_lookup[1])

    data_dict = get_chart_employee(y)

    manager_dict = get_chart_manager(y)

    # convert SQLAlchemy search result to int
    lookup_id = np.array(lookup_id)
    lookup_id = lookup_id[0]
    lookup_id = int(lookup_id)

    lookup_percent = '{:.2f}'.format(data_dict[lookup_id]*100)
    manager_lookup_percent = '{:.2f}'.format(manager_dict[lookup_id]*100)

    # now lookup state averages for all & for managers
    all_state_lookup = db.session.query(func.sum(CitizenGroup.population).label(
        'average')).filter_by(manager=False,
                              state_name=lookup_state,
                              year=y).all()

    all_lookup_women = db.session.query(func.sum(CitizenGroup.population).label(
        'average')).filter_by(manager=False,
                              female=True,
                              state_name=lookup_state,
                              year=y).all()

    state_emp_avg = all_lookup_women[0][0]/all_state_lookup[0][0]
    state_emp_percent = '{:.2f}'.format(state_emp_avg * 100)

    # managers
    manager_district_lookup = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager=True,
                              state_name=lookup_state,
                              year=y).all()

    manager_women_lookup = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager=True,
                              female=True,
                              state_name=lookup_state,
                              year=y).all()

    state_manager_avg = manager_women_lookup[0][0]/manager_district_lookup[0][0]
    state_manager_percent = '{:.2f}'.format(state_manager_avg * 100)

    # all us averages
    us_emp_lookup = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager=False, year=y).all()

    us_women_lookup = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager=False, female=True, year=y).all()

    us_emp_avg = us_women_lookup[0][0]/us_emp_lookup[0][0]
    us_emp_percent = '{:.2f}'.format(us_emp_avg * 100)

    # manager us averages
    us_manager_lookup = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager=True, year=y).all()

    us_women_manager_lookup = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager=True, female=True, year=y).all()

    us_manager_avg = us_women_manager_lookup[0][0]/us_manager_lookup[0][0]
    us_manager_percent = '{:.2f}'.format(us_manager_avg * 100)

    return jsonify({'lookup_id': lookup_id,
                    'lookup_percent': lookup_percent,
                    'manager_lookup_percent': manager_lookup_percent,
                    'lookup_state': lookup_state,
                    'lookup_dist': lookup_dist,
                    'state_emp_avg': state_emp_percent,
                    'state_manager_avg': state_manager_percent,
                    'us_emp_avg': us_emp_percent,
                    'us_manager_avg': us_manager_percent
                    })


########### HELPER FUNCTIONS


def get_chart_employee(year):
    """   """
    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # ALL EMPLOYED PERSONS POPULATION & DISTRICT INFO
    f_data = has_pop.filter_by(female=True, manager=False, year=year).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=False, year=year).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return data_dict


def get_chart_manager(year):
    """Get manager data for Chart.js bar graph."""

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # ALL EMPLOYED PERSONS
    f_data = has_pop.filter_by(female=True, manager=True, year=year).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=True, year=year).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return data_dict


def get_us_emp_average():
    """Get US average percentage women"""

    all_district_lookup = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager=False).all()
    all_lookup_women = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager=False, female=True)

    us_emp_avg = all_lookup_women[0][0]/all_district_lookup[0][0]

    return us_emp_avg


def get_us_manager_average():
    """Get US average percentage women"""

    all_district_lookup = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager=True).all()
    all_lookup_women = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager=True, female=True)

    us_manager_avg = all_lookup_women[0][0]/all_district_lookup[0][0]

    return us_manager_avg


def get_state_emp_average():
    """Get US average percentage women"""



    return us_emp_avg


def get_state_manager_average():
    """Get US average percentage women"""

    all_district_lookup = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager=True).all()
    all_lookup_women = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager=True, female=True)

    us_emp_avg = all_lookup_women[0][0]/all_district_lookup[0][0]

    return us_emp_avg



if __name__ == "__main__":

    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
