"""Flask server for Sasha's unnamed Hackbright project."""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import os
import json

from model import Location, CitizenGroup, ElectedRep, Zipcode, connect_to_db

app = Flask(__name__)

# Secret key for Flask session and debug toolbar.
FLASK_KEY = os.environ['FLASK_KEY']

app.secret_key = FLASK_KEY


# app routes
@app.route('/')
def index():
    """Index page."""

    return render_template("base.html")


@app.route('/us-map')
def one_map():
    """Route displaying single U.S. map."""

    return render_template("home.html")


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

    return render_template("us-congress-113.json")


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
