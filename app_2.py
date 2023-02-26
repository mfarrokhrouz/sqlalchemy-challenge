import numpy as np
import datetime as dt
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
Base.prepare(autoload_with=engine)

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
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/station<br/>"
        f"Use below API starting from a specific date (YYYY-MM-DD): <br/>"
        f"/api/v1.0/<start><br/>"
        f"Use below API for a range of dates (YYYY-MM-DD): <br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )


@app.route("/api/v1.0/prcp")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results_1 = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_precipitations = []
    for date, prcp in results_1:
        precipitation_dict = {}
        precipitation_dict["date"]=date
        precipitation_dict["prcp"]=prcp
        all_precipitations.append(precipitation_dict)
   
    return jsonify(all_precipitations)
    

    # Convert list of tuples into normal list



@app.route("/api/v1.0/station")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results_2 = session.query(Station.station).all()

    session.close()

# Convert list of tuples into normal list
    all_stations = list(np.ravel(results_2))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    results_3 = session.query(Measurement.tobs).\
    filter(Station.station == 'USC00519281').\
    filter(Measurement.date > '2016-08-22').all()
    
   
    all_temps = list(np.ravel(results_3))
    session.close()
    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def date_range(start):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.date(2017, 8, 23)
    data_set = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    start_group_data = list(np.ravel(data_set))
    session.close()
    temp_dict = {}
    temp_dict['Min']=start_group_data[0]
    temp_dict['Average']=round(start_group_data[1],3)
    temp_dict['Max']=start_group_data[2]
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def date_range_2(start,end):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    start_2 = start_date - dt.timedelta(days=1)
    end_2 = end_date + dt.timedelta(days=1)
    data_set = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_2).\
        filter(Measurement.date <= end_2).all()
    start_end_group_data = list(np.ravel(data_set))
    session.close()
    temp_dict_2 = {}
    temp_dict_2['Min']=start_end_group_data[0]
    temp_dict_2['Average']=round(start_end_group_data[1],3)
    temp_dict_2['Max']=start_end_group_data[2]
    return jsonify(temp_dict_2)



if __name__ == '__main__':
    app.run(debug=True)