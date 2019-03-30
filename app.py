import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")

def prcp():
    # Query for the dates and temperature observations from the last year.
    query_date = dt.date(2017, 8, 23) + dt.timedelta(days=-365)

    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date).\
    filter(Measurement.date <= dt.date.today()).all()

    #Convert the query results to a Dictionary using date as the key and tobs as the value.
    temp_data = []
    for data in results:
        temp_dict = {}
        temp_dict["date"] = data.date
        temp_dict["temperature"] = data.tobs
        temp_data.append(temp_dict)

    #Return the JSON representation of your dictionary.
    return jsonify(temp_data)


@app.route("/api/v1.0/stations")
def station():
    #Return a JSON list of stations from the dataset.
    station_num = session.query(Station.station).all()

    stations = []
    for station in station_num:
        stations.append(station)

    return jasonify(stations)

@app.route("/api/v1.0/tobs")
def temp():
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    query_date = dt.date(2017, 8, 23) + dt.timedelta(days=-365)

    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= query_date).\
    filter(Measurement.date <= dt.date.today()).all()

    temperatures = []
    for temp in results:
        temperatures.append(temp)

    return jasonify(temperatures)

@app.route("/api/v1.0/<start>") 
def start_func(start):
    results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= f"{start}").all()
    
    return jsonify({f"Tmin: {results[0]}, Tavg: {results[1]}, Tmax: {results[2]}"})

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= f"{start}").filter(Measurement.date <= f"{end}").all()
    
    return jsonify({f"Tmin: {results[0]}, Tavg: {results[1]}, Tmax: {results[2]}"})


if __name__ == '__main__':
    app.run(debug=True)