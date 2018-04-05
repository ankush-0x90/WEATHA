import requests
import pprint
from .objects.weather_obj import WeatherObject
from .unit import Unit


class Weather(object):
    URL = 'http://query.yahooapis.com/v1/public/yql'

    def __init__(self, unit=Unit.CELSIUS):
        self.unit = unit

    def lookup(self, woeid):
        url = "%s?q=select * from weather.forecast where woeid = '%s' and u='%s' &format=json" % (
            self.URL, woeid, self.unit)
        results = self._call(url)
        return results

    def lookup_by_location(self, location):
        url = "%s?q=select* from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='%s') and u='%s' &format=json" % (
                  self.URL, location, self.unit)
        results = self._call(url)
        return results

    def lookup_by_latlng(self, lat, lng):
        url = "%s?q=select* from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='(%s,%s)') and u='%s' &format=json" % (
                  self.URL, lat, lng, self.unit)
        results = self._call(url)
        return results

    @staticmethod
    def _call(url):
        req = requests.get(url)

        if not req.ok:
            req.raise_for_status()

        results = req.json()
        if int(results['query']['count']) > 0:
            wo = WeatherObject(results['query']['results']['channel'])
            return wo
        else:
            pprint.pprint(results)
