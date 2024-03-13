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

base.prepare(engine, reflect=True)

# Save references to each table

measurement = base.classes.measurement

station = base.classes.station

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
    return (f"Welcome Hawaii's Climate API<br/>"
            f"--------------------------------------<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitaton -- The precipiattion data over the past year <br/>"
            f"/api/v1.0/stations ------ A list of all observation stations<br/>"
            f"/api/v1.0/tobs --- The dates and temperature observations of the most-active station for the previous year of data<br/>"
            f"/api/v1.0/datesearch/2015-05-30  ------------ Low, High, and Average Temp <br/>"
            f"/api/v1.0/datesearch/2015-05-30/2016-01-30 -- Low, High, and Average Temp, including end date<br/>"
            f"--------------------------------------")


@app.route("/api/v1.0/precipitation")
def percipitation():
    print("Percipitation Data")
    
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date>=one_year_ago).all()

    session.close()

    
    prcpData = []
    
    for result in results:
        prcpDict = {result.date: result.prcp, "Station": result.station}
        prcpData.append(precipDict)

    return jsonify(prcpData)
    
@app.route("//api/v1.0/stations")
def stations():
    print("Stations Data")

    # A query to find the most active stations
    station_results = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).all()

    session.close()
    
    
    statData = [] 
    
    for result in station_results:
        statDict = {result.date: result.tobs, "Station": result.station}
        statData.append(precipDict)
       
        
    return jsonify(statData)
    
    

@app.route("/api/v1.0/tobs")
def tobs():
    print("The dates and temperature observations of the most-active station for the previous year of data")
    
    # Query the last 12 months of temperature observation data for this station 
    results_2 = session.query(measurement.tobs).filter(measurement.date>=one_year_ago).\
    filter(measurement.station == "USC00519281").all()
    
    tobsData=[]
    
    for tobs,date in results_2:
        tobsDict={}
        tobsDict['date']=date
        tobsDict['tobs']=tobs
        tobsData.append(tobsDict)
        
    return jsonify(tobsData)

@app.route("/api/v1.0/<start>")
def climate_start():
    print("Low, High, and Average Temp For a specified start")
    
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).all()
    
    session.close()
    
    startData={}
    startData["Min_Temp"]=results[0][0]
    startData["avg_Temp"]=results[0][1]
    startData["max_Temp"]=results[0][2]

    return jsonify(startData)



@app.route("/api/v1.0/<start>/<end>")
def climate_start_end():
    print("Low, High, and Average Temp For a specified start date and end date")

    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()
    
    startEndData={}
    startEndData["Min_Temp"]=results[0][0]
    startEndData["avg_Temp"]=results[0][1]
    startEndData["max_Temp"]=results[0][2]
        
    return jsonify(startEndData)

if __name__ == "__main__":
    app.run(debug=True)
