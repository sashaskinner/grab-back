"""Flask server for Sasha's unnamed Hackbright project."""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, jsonify
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


@app.route('/us-map')
def one_map():
    """Route displaying single U.S. map."""

    return render_template("base.html")


    # query for population information
    # query for location & zipcode information
    # query for election information


@app.route('/two-maps')
def two_maps():
    """Route displaying two side-by-side U.S. maps."""
    pass

    # query for population information
    # query for location & zipcode information
    # query for election information


@app.route('/us.json')
def us_json():
    """JSON file with US map specs."""

    return render_template("us.json")


@app.route('/us-congress-113.json')
def us_congress_113():
    """JSON file with congressional district shapes for us map."""

    return render_template("us-congress-113.json")\



@app.route('/district-pop-info.json')
def get_population_info():
    """Query db for relevant population info."""

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population).filter(CitizenGroup.population.isnot(None))

    data = has_pop.filter_by(female=True, manager=True).all()
    total_data = has_pop.filter_by(female=False, manager=True).all()

    data_dict = {}
    for i in range(len(data)):
        data_dict[data[i][0]] = (data[i][1]/total_data[i][1])

    print data_dict
    return jsonify(data_dict)


# @app.route('/us-congress-district-ids.csv')
# def district_ids():
#     """CSV file with district ids to locate district on map."""

#     return render_template("us-congress-district-ids.csv")


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
