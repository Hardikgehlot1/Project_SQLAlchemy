import numpy as np
import datetime as dt

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
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all the availables api routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Query
    months_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query( Measurement.date,Measurement.prcp).\
        filter(Measurement.date > months_ago).\
        order_by(Measurement.date).all()
    session.close()

    Precipitation_data = []
    for date, prcp in results:
        Precipitation_dict = {}
        Precipitation_dict["date"] = date
        Precipitation_dict["prcp"] = prcp
        
        Precipitation_data.append(Precipitation_dict)

    return jsonify(Precipitation_data)




@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results1 = session.query(Measurement.station)
    session.close()

    return jsonify(results1)


if __name__ == '__main__':
    app.run(debug=True)
