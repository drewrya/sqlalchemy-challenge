import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value
    dates_and_precips =   session.query(Measurement.date, Measurement.prcp).all()

    # Convert to list of dictionaries to jsonify
    dicts = []

    for date, prcp in results:
        dict = {}
        dict[date] = prcp
        dicts.append(dict)

    session.close()

return jsonify(dicts)

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    stations = []
    for station, name in results:
        station_dict = {}
        station_dict["name"] = name
        stations.append(station_dict)
 
return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    last_data_point = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    #Convert date string to date object
    format = '%Y-%m-%d'  # The format 
    last_data_point_object = dt.datetime.strptime(last_data_point[0],format)

    year_of_data = last_data_point_object - dt.timedelta(days=365)

    # Query for the dates and temperature values of the most active station 'USC00519281'
    results =   session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date >= year_of_data).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of stations
    tobs_data = []
    for date, tobs in results:
        tob = {}
        tob[date] = tobs
        tobs_data.append(tob)

return jsonify(tobs_data)


# @app.route("/api/v1.0/<start>")
# def temp_range_start(start):
#     """TMIN, TAVG, and TMAX per date starting from a starting date.
    
#     Args:
#         start (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """

#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     return_list = []

#     results =   session.query(  Measurement.date,\
#                                 func.min(Measurement.tobs), \
#                                 func.avg(Measurement.tobs), \
#                                 func.max(Measurement.tobs)).\
#                         filter(Measurement.date >= start).\
#                         group_by(Measurement.date).all()

#     for date, min, avg, max in results:
#         new_dict = {}
#         new_dict["Date"] = date
#         new_dict["TMIN"] = min
#         new_dict["TAVG"] = avg
#         new_dict["TMAX"] = max
#         return_list.append(new_dict)

#     session.close()    

#     return jsonify(return_list)

# @app.route("/api/v1.0/<start>/<end>")
# def temp_range_start_end(start,end):
#     """TMIN, TAVG, and TMAX per date for a date range.
    
#     Args:
#         start (string): A date string in the format %Y-%m-%d
#         end (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """

#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     return_list = []

#     results =   session.query(  Measurement.date,\
#                                 func.min(Measurement.tobs), \
#                                 func.avg(Measurement.tobs), \
#                                 func.max(Measurement.tobs)).\
#                         filter(and_(Measurement.date >= start, Measurement.date <= end)).\
#                         group_by(Measurement.date).all()

#     for date, min, avg, max in results:
#         new_dict = {}
#         new_dict["Date"] = date
#         new_dict["TMIN"] = min
#         new_dict["TAVG"] = avg
#         new_dict["TMAX"] = max
#         return_list.append(new_dict)

#     session.close()    

#     return jsonify(return_list)

# if __name__ == '__main__':
#     app.run(debug=True)