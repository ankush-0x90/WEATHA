from WunderWeather import weather
import arrow
import pprint
# setup
api_key = "your api key"
location = 'MA/Boston'
extractor = weather.Extract("a5a9715c2a101a62")

# alerts
response = extractor.alerts(location)
pprint(response.data)

# astronomy
response = extractor.astronomy(location)
pprint(response.data)

# geolookup
response = extractor.geolookup(location)
pprint(response.data)

# history
date = arrow.get("2018/04/05","YYYYMMDD")
response = extractor.date(location,date.format('YYYYMMDD'))
pprint(response.data)

# addl date detail
for observation in response.observations:
    print("Date:",observation.date_pretty)
    print("Temp:",observation.temp_f)