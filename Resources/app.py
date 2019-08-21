# 1. import Flask
import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})
#engine = create_engine(os.path.join("sqlite:///","Resources","hawaii.sqlite"),echo=False)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#### Home page 
""" List all routes that are available."""
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'Home' page!</br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date(YYYY-MM-DD)<br/>"
        f"/api/v1.0/start_date(YYYY-MM-DD)/end_date(YYYY-MM-DD)<br/>"
    )

###########################
#### /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precip():
        precip = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).all()
        precipitation = []
        for date, prcp in precip:
                precip_dict ={}
                precip_dict["date"] = date
                precip_dict["prcp"] = prcp
                precipitation.append(precip_dict)
        return jsonify(precipitation)

###########################
#### `/api/v1.0/stations`
"""* Return a JSON list of stations from the dataset."""
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.name,Station.station).order_by(Station.name.desc()).all()
    return jsonify(stations) 

###########################
#### `/api/v1.0/tobs`   
"""query for the dates and temperature observations from a year from the last data point."""
"""Return a JSON list of Temperature Observations (tobs) for the previous year.   """
@app.route("/api/v1.0/tobs")
def tobs():
        temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > "2016-08-23").order_by(Measurement.date.desc()) 
        temperatures = []
        for date, tobs in temps:
                temp_dict ={}
                temp_dict["date"] = date
                temp_dict["tobs"] = tobs
                temperatures.append(temp_dict)
        print(temperatures)
        return jsonify(temperatures)

###########################
####`/api/v1.0/<start>`
@app.route("/api/v1.0/<start_date>")
def start(start_date):
        start_values = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
        start_temps = {"minT": start_values[0][0],
                        "avgT": start_values[0][1],
                        "maxT": start_values[0][2]
        }
        return jsonify(start_temps)
       
###########################
####`/api/v1.0/<start>/<end>`
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
        start_end_values = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        temps = {"minT": start_end_values[0][0],
                "avgT": start_end_values[0][1],
                "maxT": start_end_values[0][2]
        }
        return jsonify (temps)
#################################
if __name__ == "__main__":
        app.run(debug=True)
