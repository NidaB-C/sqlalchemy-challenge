# Importing required libraries and modules
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

# Setting up the database connection
# The database file is expected to be in the '../Resources/' directory
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflecting an existing database into a new model
# This process makes the database tables accessible as Python classes
Base = automap_base()
Base.prepare(autoload_with=engine, reflect=True)

# Saving references to the 'measurement' and 'station' tables
# These references will be used to access data from these tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask application setup
app = Flask(__name__)

# Defining the home route
# This route displays all available API routes for easy navigation
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation Data for the Last Year<br/>"
        f"/api/v1.0/stations - List of Weather Observation Stations<br/>"
        f"/api/v1.0/tobs - Temperature Observations for the Most Active Station for the Last Year<br/>"
        f"/api/v1.0/&lt;start&gt; - Temperature Summary from a Start Date (format: YYYY-MM-DD)<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; - Temperature Summary between Start and End Dates (format: YYYY-MM-DD)"
    )

# Route for precipitation data
# This route queries the database for the last year of precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Query to find the most recent date in the dataset
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    # Calculating the date one year before the most recent date
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query for precipitation data after the calculated date
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    session.close()

    # Converting query results to a dictionary format
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)

# Route for station data
# This route lists all the weather observation stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    # Converting the list of tuples into a regular list
    stations = list(np.ravel(results))
    return jsonify(stations)

# Route for temperature observations (tobs) data
# This route returns the last year of TOBS data for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_station = 'USC00519281'  # Hardcoded the most active station for the query
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query for TOBS data for the most active station after the calculated date
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Converting query results to a dictionary format
    tobs_data = {date: tobs for date, tobs in results}
    return jsonify(tobs_data)

# Route for temperature summary from a given start date or between start and end dates
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end=None):
    session = Session(engine)

    # Query selections for minimum, average, and maximum temperatures
    sel = [func.min(Measurement.tobs).label("min_temp"),
           func.avg(Measurement.tobs).label("avg_temp"),
           func.max(Measurement.tobs).label("max_temp")]
    
    # Conditional queries based on the presence of an end date
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Constructing the dictionary with keys for min, avg, and max temperatures
    temps = {}
    if results:
        temps["min_temp"] = results[0].min_temp
        temps["avg_temp"] = results[0].avg_temp
        temps["max_temp"] = results[0].max_temp

    return jsonify(temps)

# Main entry point for running the Flask app
if __name__ == '__main__':
    app.run(debug=False)
