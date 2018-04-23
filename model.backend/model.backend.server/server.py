#coded by asprazz https://github.com/asprazz/WEATHA/model.backend/model.backend.server
# imports
import requests
from flask import Flask,render_template,jsonify
import pprint 
import json
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
@app.route('/sarya')
def sarang():
    return "Chutya"     


#route home routing
@app.route('/')
def render_home():

    jLocation = weather.lookup_by_location("Jalgaon")
    dLocation = weather.lookup_by_location("dhule")
    mLocation = weather.lookup_by_location("muktainagar")
    bLocation = weather.lookup_by_location("bhusaval")
    nLocation = weather.lookup_by_location("nadhurbar")
    conds = []
    conds.append(jLocation.condition.text)
    conds.append(dLocation.condition.text)
    conds.append(mLocation.condition.text)
    conds.append(bLocation.condition.text)
    conds.append(nLocation.condition.text)

    temp = []
    temp.append(jLocation.condition.temp)
    temp.append(dLocation.condition.temp)
    temp.append(mLocation.condition.temp)
    temp.append(bLocation.condition.temp)
    temp.append(nLocation.condition.temp)


    temp = ['30','100','120','20']
    return render_template("index.html",conds=conds,temp=temp)



#routes for REST APIs
@app.route('/api/<city>')
def api_route(city):
    return jsonify(city)

#root to analytics
@app.route('/analytics/')
def render_analytics():
    
    cities = ['Jalgaon']
    DIR = "data/India"
    dates = []
    today = datetime.date.today()
    DAYS=1800

    for d in range(DAYS, 0, -1):
        dates.append(datetime.date.strftime(today - datetime.timedelta(days=d), \
            "%Y%m%d"))
    dates.append(datetime.date.strftime(today,"%Y%m%d"))
    for c in cities:
        avg = 1
        i=0
        thirteen_fourteen = []
        for d in dates:
            i+=1
            if(i==365):
                avg = float(avg/i)
                thirteen_fourteen.append(avg)
                break
            try:
                path = DIR+'/'+c+'/'+d+'.json'
               # print(path)
                with open(path) as json_data:
                    try:
                       print("")
                       tempT=d["history"]["observations"][0]["tempm"]
                       avg += tempT
                    except:
                        continue
            except:
                continue    

    # print(path)
    ''' normal example with thesis    
    
    path = DIR+'/Asoda/'+'20171116'+'.json'
    with open(path) as json_data:
        d = json.load(json_data)
        t=d["history"]["observations"][0]["tempm"])  
    '''
    thirteen_fourteen=parseAverages(thirteen_fourteen)
    return render_template('analytics.html',thirteen_fourteen=thirteen_fourteen)


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
        #not active

        #predictedTemp=float(predict_weather(record))
        
        predictedTemp=59
        print("Predicted temprature is ")
        print(predictedTemp)

        predictedT = (predictedTemp)
        
        nextSeven = location.forecast
        conds = location.condition.text
        print(conds)
        minTemp=[]
        maxTemp=[]
        dates = []

        for i in nextSeven:
            minTemp.append(int(i.low))
            maxTemp.append(int(i.high))
            dates.append(i.date)
        print(dates)

    return render_template("cityWeather.html",city=city,predictedTemp=predictedT,minTemp=minTemp,maxTemp=maxTemp,dates=dates,conds=conds)




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


def parseAverages(x):
    return [40,32,36,0]
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