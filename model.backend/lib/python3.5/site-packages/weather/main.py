from argparse import ArgumentParser
from .weather import Weather
import sys


def main():
    pa = ArgumentParser()
    pa.add_argument('location', help='The location to lookup.')
    pa.add_argument('--unit', default='c', nargs='?', choices=['c', 'f'])
    args = pa.parse_args()
    weather = Weather(args.unit)
    loc = weather.lookup_by_location(args.location)
    condition = loc.condition
    print("Weather report for %s, %s" % (loc.location.city, loc.location.country))
    print("Condition: %s " % condition.text)
    print("Temperature: %s" % condition.temp)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
