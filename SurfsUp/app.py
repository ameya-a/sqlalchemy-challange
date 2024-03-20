# Import the dependencies.

from flask import Flask, jsonify



import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text, inspect

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

base = automap_base()

# reflect the tables

base.prepare(autoload_with=engine)

# Save references to each table

measurement = base.classes.measurement

s = base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)


#################################################
# Flask Setup
#################################################

app = Flask(__name__) # the name of the file & the object (double usage)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(f"Welcome!<br/>"
            f"--------------------------------------<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitaton -- The precipiattion data over the past year <br/>"
            f"/api/v1.0/stations ------ A list of all observation stations<br/>"
            f"/api/v1.0/tobs --- The dates and temperature observations of the most-active station for the previous year <br/>"
            f"/api/v1.0/temp/start  ------------ Low, High, and Average Temp <br/>"
            f"/api/v1.0/temp/start/end -- Low, High, and Average Temp, including end date<br/>"
            f"--------------------------------------")


# @app.route("/api/v1.0/precipitation")
# def precipitation():
    
#     session = Session(engine)

#     # Perform a query to retrieve the data and precipitation scores
#     results = (session.query(measurement.date, measurement.prcp)
#         .filter(measurement.date > "2017-08-23")
#         .order_by(measurement.date)
#         .all())

#     session.close()
    
#     prcpData =[]
    
#     for data in results:
#         prcpData.append(result)
#     prcp=dict(prcpData)
#     return jsonify(prcp)

    # Perform a query to retrieve the data and precipitation scores
@app.route("/api/v1.0/precipitation")
def precipitation():
    
 #   session = Session(engine)
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()
             
#                order_by(measurement.date).\ 
#                all()
    
 #   session.close()
    
    prcpData = {}
    
    for date, prcp in results:
        prcpData[date] = prcp
    
    return jsonify(prcpData)
    
@app.route("/api/v1.0/stations")
def stations():
    print("Stations Data")    
    session = Session(engine)
    sel = [s.station,s.name,s.latitude,s.longitude,s.elevation]
    queryresult = session.query(*sel).all()
    session.close()

    stations = []
    for station,name,lat,lon,el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("The dates and temperature observations of the most-active station for the previous year of data")
#     session = Session(engine)
    
    # Query the last 12 months of temperature observation data for the most active station
    tobss = session.query(measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date >= dt.date(2016,8,23)).all()
    
#     tobsData = [tobs[0] for tobs in tobss]  # Extract temperature values from the query results
    
#     session.close()
    
    # Create a dictionary with temperature observations
#     tobs_temp_data = {"tobs": tobsData}
    temperature_data = list(np.ravel(tobss))
    
    return jsonify(temperatures=temperature_data)

# @app.route("/api/v1.0/<start>")
# def climate_start(start=None):
#     session = Session(engine)
    
#     results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#                 filter(measurement.date >= start).all()
    
#     session.close()
    
#     startData=[]
#     for min,avg,max in results:
#         tobs_dict = {}
#         tobs_dict["Min"] = min
#         tobs_dict["Average"] = avg
#         tobs_dict["Max"] = max
#         startData.append(tobs_dict)

#     return jsonify(startData)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def climate_start_end(start=None, end=None):
#     session = Session(engine)
    select = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    
    if not end:
        start = dt.datetime.strptime(start, "%Y-%m-%d")  
        results = session.query(*select).\
            filter(measurement.date >= start).all()
    else:
        start = dt.datetime.strptime(start, "%Y-%m-%d") 
        end = dt.datetime.strptime(end, "%Y-%m-%d")    
        results = session.query(*select).\
            filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()
    temps = list(np.ravel(results))
    
    return jsonify(temps)
      
     #return jsonify(temps =
          
       
    
  #  startEndData=[]
#     for min,avg,max in results:
#         tobs_dict = {}
#         tobs_dict["Min"] = min
#         tobs_dict["Average"] = avg
#         tobs_dict["Max"] = max
#         startEndData.append(tobs_dict)
        
    return jsonify(temps=temps)

if __name__ == "__main__":
    app.run(debug=True)
