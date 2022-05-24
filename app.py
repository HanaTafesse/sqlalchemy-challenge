import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<br/>" 
        f"<h1>Welcome to Hawaii Climate Page!!</h1>"
        f"<br/>" 
        f" <img width='600' src='https://www.surfertoday.com/images/stories/surfingsport.jpg'/ >"
        f"<h3>These Are All Available Routes for Hawaii Weather Data</h3>"
        f"-- Daily Precipitation Totals for Last Year: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
         f"-- Active Weather Stations: <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"-- Daily Temperature Observations for Station USC00519281 for Last Year: <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg' target='_blank'>/api/v1.0/min_max_avg</a>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data"""
    # Query all date and prcp values
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_prcp.append(measurement_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Station.name, Station.station).all()
    
    session.close()

    """Return a list of all stations"""
    # Query all stations
    all_stations = []
    for name, station in results:
        station_dict = {}
        station_dict["station id"] = station
        station_dict["station name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    sel = [Measurement.date, Measurement.tobs]
    
    results = session.query(*sel).filter\
               (func.strftime(Measurement.date) > '2016-08-23')\
               .order_by(Measurement.date).all()
    
    session.close()
    
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temp"] = tobs
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs) 



@app.route("/api/v1.0/<start>")
def start(start):
    """Fetch the temperatures whose date is greater than or equal to
       the path variable supplied by the user, or a 404 if not."""

    session = Session(engine)
    sel = [Measurement.date, Measurement.tobs]
    
    results = session.query(*sel).filter\
               (func.strftime(Measurement.date) >= start)\
               .order_by(Measurement.date).all()
    
    session.close()
    
    start_tobs = []
    
    for date, tmin, tavg, tmax in results:
        
        tmin = results.tobs.min()
        tmin = results.tobs.avg()
        tmin = results.tobs.max()
        start_tobs["date"] = date
        start_tobs["TMIN"] = tmin
        start_tobs["TAVG"] = tavg
        start_tobs['TMAX'] = tmax
        
        start_tobs.append(start_tobs)
        
        return jsonify(start_tobs)

    return jsonify({"error": f"Dates after {start} not found."}), 404

@app.route("/api/v1.0/<start>/<end>")
def startend(startend):
    """Fetch the temperatures whose dates are between
       the path variables supplied by the user, or a 404 if not."""

    session = Session(engine)
    sel = [Measurement.date, Measurement.tobs]
    
    results = session.query(*sel).filter\
               (func.strftime(Measurement.date) >= start & func.strftime(Measurement.date) <= end)\
               .order_by(Measurement.date).all()
    
    session.close()
    
    startend_tobs = []
    
    for date, tmin, tavg, tmax in results:
        
        tmin = results.tobs.min()
        tmin = results.tobs.avg()
        tmin = results.tobs.max()
        startend_tobs["date"] = date
        startend_tobs["TMIN"] = tmin
        startend_tobs["TAVG"] = tavg
        startend_tobs['TMAX'] = tmax
        
        startend_tobs.append(startend_tobs)
        
        return jsonify(startend_tobs)

    return jsonify({"error": f"Dates between {startend} not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)