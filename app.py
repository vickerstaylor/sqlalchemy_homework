import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation by date:<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<br/>"
        f"List of stations:<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<br/>"
        f"Temperature observations by date:<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<br/>"
        f"Temperature stats for trip:<br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/start'>/api/v1.0/start</a><br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/start/end'>/api/v1.0/start/end</a><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_query = session.query(Measurement.date, Measurement.prcp, Measurement.station).\
                                 filter(Measurement.date >= last_year).order_by(Measurement.date).all()

    return jsonify(precip_query)


@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)

    return jsonify(stations.to_dict())


@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_query = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
                               filter(Measurement.date >= last_year).order_by(Measurement.date).all()

    return jsonify(tobs_query)


@app.route("/api/v1.0/<start>")
def trip1(start):
    start_date = dt.date(2017, 2, 14)
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    trip = list(np.ravel(trip_data))

    return jsonify(trip)


@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):
    start_date = dt.date(2017, 2, 14)
    end_date = dt.date(2017, 2, 20)
    last_year = dt.timedelta(days=365)
    start = (start_date - last_year)
    end = (end_date - last_year)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip2 = list(np.ravel(trip_data))

    return jsonify(trip2)

if __name__ == "__main__":
    app.run(debug=True)