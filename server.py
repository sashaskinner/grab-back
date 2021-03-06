"""Flask server Grab Back."""

from flask import Flask, request, render_template, jsonify

import os
import numpy as np
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///jobs"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from model import Location, CitizenGroup, Zipcode, connect_to_db, db

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
    """Takes year input and returns manager json data to index. """
    y = request.args.get("year", 2015)
    print(y)
    return jsonify(format_data(y, True))


@app.route('/district-employee-info.json', methods=['GET'])
def get_employee_info():
    """Takes year input and returns employee json data to index. """
    y = request.args.get("year", 2015)
    return jsonify(format_data(y, False))


@app.route('/chart-data-employee')
def get_chart_data_employee():
    """Get data from db query to populate chart. """

    y = request.args.get("year", 2015)
    return jsonify(format_chart_data(y, False))


@app.route('/chart-data-employee-reverse')
def get_reverse_data_employee():
    """Get data from db query to populate bottom districts chart. """

    y = request.args.get("year", 2015)
    return jsonify(format_reverse_chart(y, False))


@app.route('/chart-data-manager')
def get_chart_data_manager():
    """Get data from db query to populate chart. """

    y = request.args.get("year", 2015)
    print(y)
    return jsonify(format_chart_data(y, True))


@app.route('/chart-data-manager-reverse')
def get_reverse_data_manager():
    """Get data from db query to populate bottom districts chart. """

    y = request.args.get("year", 2015)
    return jsonify(format_reverse_chart(y, True))


@app.route('/zipcode-lookup.json', methods=['GET'])
def get_district_from_zipcode():
    """Get location_id from zipcode entry."""

    z = request.args.get("zipcode-entry")
    y = request.args.get("year", 2015)
    return jsonify(get_zipcode_data(z, y))


########### HELPER FUNCTIONS


def format_data(year, manager):
    """
    Query db for population info for either all employees or management employees. Returns data_dict to route.

    format_data(year, manager [True/False])

    >> data_dict

    """
    y = int(year)

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population, CitizenGroup.year).filter(CitizenGroup.population
                                                           .isnot(None))

    f_data = has_pop.filter_by(female="t", manager='t', year=y).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female="f", manager='t', year=y).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return data_dict


def get_chart(year, manager):
    """Get data for chart.js bar graph for either all employees or managers

    Year input should be int and manager should be bool."""
    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    # ALL EMPLOYED PERSONS POPULATION & DISTRICT INFO
    f_data = has_pop.filter_by(female="t", manager='t', year=year).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female="f", manager='t', year=year).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return data_dict


def format_chart_data(year, manager):
    """Query for districts with highest percentage of women in the population specified by the manager argument"""

    y = int(year)

    data_dict = get_chart(y, manager)
    us_avg = '{:.2f}'.format(get_us_average(manager) * 100)

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
    all_data[1].append(float(us_avg))

    return all_data


def format_reverse_chart(year, manager):
    """Query for districts with the lowest percentage of women in the category specified by the manager argument"""
    y = int(year)

    data_dict = get_chart(y, manager)
    us_avg = '{:.2f}'.format(get_us_average(manager) * 100)

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
    all_data[1].append(float(us_avg))

    return all_data


def get_zipcode_data(zipcode, year, manager):
    """Queries for zipcode data in a given year and returns to server route."""

    z = int(zipcode)
    y = int(year)

    lookup_id = db.session.query(Zipcode.location_id).filter_by(zipcode=z).first()
    district_lookup = db.session.query(Zipcode.state_name, Zipcode.district_id).filter_by(zipcode=z).first()

    lookup_state = str(district_lookup[0])
    lookup_dist = int(district_lookup[1])

    data_dict = get_chart(y, manager)

    # manager_dict = get_chart(y, True)

    # convert SQLAlchemy search result to int
    lookup_id = np.array(lookup_id)
    lookup_id = lookup_id[0]
    lookup_id = int(lookup_id)

    lookup_percent = '{:.2f}'.format(data_dict[lookup_id]*100)
    # manager_lookup_percent = '{:.2f}'.format(manager_dict[lookup_id]*100)

    # now lookup state averages for all & for managers
    all_state_lookup = db.session.query(func.sum(CitizenGroup.population).label(
        'average')).filter_by(manager='t',
                              state_name=lookup_state,
                              year=y).all()

    all_state_lookup_women = db.session.query(func.sum(CitizenGroup.population).label(
        'average')).filter_by(manager='t',
                              female="t",
                              state_name=lookup_state,
                              year=y).all()

    state_avg = all_state_lookup_women[0][0]/all_state_lookup[0][0]
    state_percent = '{:.2f}'.format(state_avg * 100)

    # all us averages
    us_lookup_all = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager="t", year=y).all()

    us_lookup_women = db.session.query(func.sum(
        CitizenGroup.population).label(
        'average')).filter_by(manager="t", female="t", year=y).all()

    us_avg = us_lookup_women[0][0]/us_lookup_all[0][0]
    us_percent = '{:.2f}'.format(us_avg * 100)

    data_dict = {'lookup_id': lookup_id,
                 'lookup_percent': lookup_percent,
                 'lookup_state': lookup_state,
                 'lookup_dist': lookup_dist,
                 'state_avg': state_percent,
                 'us_avg': us_percent,
                 }

    return data_dict


# QUERY FOR AND CALCULATE AVERAGES FOR ENTIRE U.S. POPULATIONS
def get_us_average(manager):
    """Get the average percentage of women in either for all employees or for managers.

    manager argument should be bool."""

    all_district_lookup = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager="t").all()
    all_lookup_women = db.session.query(func.sum(CitizenGroup.population).label('average')).filter_by(manager="t", female="t")

    us_avg = all_lookup_women[0][0]/all_district_lookup[0][0]

    return us_avg


if __name__ == "__main__":

    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
