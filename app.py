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

# Save references to the tables
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Hawaiian Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/*start* <br/>"
        f"*start* must be a date entered in YYYY-MM-DD format<br/>"
        f"/api/v1.0/*start*/*end* <br/>"
        f"*start* and *end* must be dates entered in YYYY-MM-DD format<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = list(session.query(measurement.station).distinct())

    session.close()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(measurement.tobs).\
    filter(measurement.date >= '2016-08-23').\
    filter_by(station='USC00519281').all()

    session.close()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)

    min = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date ).all()
    max = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date ).all()
    avg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date ).all()
    session.close()

    results= (max, avg, min)

    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    session = Session(engine)

    min = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    max = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    avg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    results= (max, avg, min)

    all_results = list(np.ravel(results))

    return jsonify(all_results)

if __name__ == "__main__":
    app.run(debug=True)
