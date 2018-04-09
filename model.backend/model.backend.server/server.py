#coded by asprazz https://github.com/asprazz/WEATHA/model.backend/model.backend.server
# imports
import requests
from flask import Flask,render_template,jsonify
import pprint 
import datetime
import boto3
from boto3.session import Session
from weather import Weather, Unit
#           ENDING IMPORT EXPORTS           #
#           Global Functionalities          #
app = Flask(__name__)
weather = Weather(unit=Unit.CELSIUS)
#global Variable 
predictedTemp = 0
conds = ""
#routing on slash



#route home routing
@app.route('/')
def render_home():
   return render_template("index.html")



#routes for REST APIs
@app.route('/api/<city>')
def api_route(city):
    
    return jsonify(city)

#root to analytics
@app.route('/analytics/')
def render_analytics():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('analytics.html', values=values, labels=labels)


#analytics?radar
@app.route('/analytics/radar')
def render_radar():
    return render_template('analytics_radar.html')



#approute for graphical city
@app.route('/<city>')
def render_cityWeather(city):
    if(city!="favicon.ico"):
        record = {}
        print("Predicting For this city")
        print(city)
        location = weather.lookup_by_location(city)
        forecasts = location.forecast

        j_hum = location.atmosphere['humidity']
        print(j_hum)
        j_pressurem = location.atmosphere['pressure']
        j_vism = location.atmosphere['visibility']
        j_dewptm = 11
        j_tempm = forecasts[0].high
        #print(j_tempm)
        j_wspdm=location.wind.speed
        #record['datetime_utc'] = 

        #generating record for machine prediction
        now=datetime.datetime.now()
        now=str(now.strftime("%Y%m%d-%H:%M"))

        record['datetime_utc']=now
        record['j_conds']=""
        record['j_dewptm']=str(j_dewptm)
        record['j_fog']=str(0)
        record['j_hail']=str(0)
        record['j_heatindex']=""
        record['j_hum']=str(35)
        record['j_precipm']=""
        record['j_pressurem']=j_pressurem
        record['j_rain']=str(0)
        record['j_snow']=str(0)
        record['j_tempm']=j_tempm
        record['j_thunder']=str(0)
        record['j_tornado']=str(0)
        record['j_vism']=j_vism
        record['j_wdird']=""
        record['j_wdire']=""
        record['j_wgustm']=""
        record['j_windchillm']=""
        record['j_wspdm']=j_wspdm


        #print(record)
        predictedTemp=float(predict_weather(record))
        print("Predicted temprature is ")
        print(predictedTemp)
        predictedT =(predictedTemp)
        
        nextSeven = location.forecast
        conds = location.condition.text

        print(conds)

    return render_template("cityWeather.html",city=city,predictedTemp=predictedT,nextSeven=nextSeven,conds=conds)






def predict_weather(record):
    
    session = Session(aws_access_key_id='', aws_secret_access_key='')
    machinelearning = session.client('machinelearning', region_name='eu-west-1')
    model_id = ''
    
    try:
        #dynamically retrieve model and prediction endpoint
        model = machinelearning.get_ml_model(MLModelId=model_id)
        prediction_endpoint = model.get('EndpointInfo').get('EndpointUrl')
        #print(prediction_endpoint)

        response = machinelearning.predict(MLModelId=model_id, Record=record, PredictEndpoint=prediction_endpoint)
        #label = response.get('Prediction').get('predictedLabel')    
        predictedTemp = response.get('Prediction').get('predictedValue')
        
        return predictedTemp

    except Exception as e:
        print(e)



    
#testing route
@app.route('/testing')
def xxxxx():    
    nextSeven = {
        "30" : "CLEAR",
        "35" : "CLOUDY",
        "33" : "SUNNY",
        "32" : "SUNNY",
        "31" : "CLEAR",
        "25" : "SUNNY",
        "33" : "CLOUDY"
    }
    return render_template("index.html",tempC="30",conds="CLEAR",nextSeven=nextSeven)

# LETS HOPE FOR GOOD MAIN
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)