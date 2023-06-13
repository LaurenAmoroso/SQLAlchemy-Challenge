# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def home():
    return("/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/2017-01-01<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    results1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    first_dict = list(np.ravel(results1))
    return jsonify(first_dict) 

@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station, Station.name).all()
    sec_dict = list(np.ravel(results2))
    return jsonify(sec_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date>="2016-08-23").\
            filter(Measurement.date<="2017-08-23").all()
    temp_dict = list(np.ravel(results3))
    return jsonify(temp_dict)

@app.route("/api/v1.0/<date>")
def start1(date):

    results4 = session.query((Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
            filter(Measurement.date)>=date).all()
    
    five_dict = []
    for s in results4:
        start_dict = {}
        start_dict["Date"] = s.Date
        start_dict["Avg"] = s.func.avg(Measurement.tobs)
        start_dict["Min"] = s.func.min(Measurement.tobs)
        start_dict["Max"] = s.func.max(Measurement.tobs)
        five_dict.append(start_dict)

        return jsonify(five_dict)
    
    if __name__ == '__main__':
        app.run(debug=True)

#################################################
# Flask Routes
#################################################
