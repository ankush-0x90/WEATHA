from weather import Weather, Unit
import json

weather = Weather(unit=Unit.CELSIUS)


location = weather.lookup_by_location('jalgaon')


print(location.atmosphere['humidity'])


# next saven days forecast
forecasts = location.forecast



for forecast in forecasts:
    print(forecast.text)
    print(forecast.date)
    print(forecast.high)
    print(forecast.low)