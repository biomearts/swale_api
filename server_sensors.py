#!/usr/bin/env python3

#import pkg_resources
#pkg_resources.require("requests>=2.10.0")

import sys
sys.path.insert(0, "/usr/local/lib/python3.4/dist-packages/")

import os, sys, json, pymongo, requests, ephem
from housepy import config, log, util, geo
from mongo import db

SOURCE = "server"

try:
    entry = {'source': SOURCE}
    result = list(db.entries.find({'source': "gps"}).sort([("t_utc", pymongo.DESCENDING)]).limit(1))[0]
    lat, lon = result['latitude'], result['longitude']
    entry.update({'latitude': result['latitude'], 'longitude': result['longitude']})
except Exception as e:
    log.info(log.exc(e))
    exit()

# Tarrytown, Hudson River, New York  (Tarrytown)
# Madison Ave. Bridge, New York Current (Bronx)
# Brooklyn Bridge (Brooklyn)

# lat, lon = 41.255873,-73.9676297    # king marine
# # lat, lon = 40.706172,-73.930953     # bushwick
# lat, lon = 40.6901015,-74.0111785   # governor's island
# # lat, lon = 40.8255327,-73.893846    # concrete plant park
# lat, lon = 41.1810336,-73.9069995 # croton
# lat, lon = 40.7055395,-74.0219601

# url = "http://api.wunderground.com/api/%s/geolookup/q/%s,%s.json" % (config['weather'], lat, lon)
# state = requests.get(url).json()['location']['state']
# city = requests.get(url).json()['location']['city'].strip("The ")


def get_tide(entry):

    try:

        stations = {    (40.7033,-73.9883): "Brooklyn",
                        (40.8133,-73.935): "Bronx",
                        (41.0783,-73.87): "Tarrytown"
                        }

        closest_miles = 10000
        closest_city = None
        for location, city in stations.items():
            miles = geo.distance((entry['longitude'], entry['latitude']), (location[1], location[0]))
            if miles < closest_miles:
                closest_miles = miles
                closest_city = city

        response = requests.get("http://api.wunderground.com/api/%s/rawtide/q/NY/%s.json" % (config['weather'], closest_city))
        data = response.json()
        t_utc, height = data['rawtide']['rawTideObs'][0]['epoch'], data['rawtide']['rawTideObs'][0]['height']

        entry.update({'tide_station': city, 'tide_height_ft': height})

    except Exception as e:
        log.error(log.exc(e))

    return entry


def get_sun(entry):
    try:
        observer = ephem.Observer()
        observer.lon = entry['longitude']
        observer.lat = entry['latitude']
        observer.elevation = entry['altitude_m']
        dt = datetime.datetime.utcnow()     # always UTC
        observer.date = dt.strftime("%Y/%m/%d %H:%M:%S")
        sun = ephem.Sun(observer)
        radians = float(sun.alt)        
        degrees = math.degrees(radians)
        entry.update({'sun_deg': degrees})
    except Exception as e:
        log.error(e)
    return entry


entry = get_tide(entry)
entry = get_sun(entry)


try:
    response = requests.post("http://54.235.200.47", json=entry, timeout=5)
    log.info(response.status_code)
except Exception as e:
    log.error(log.exc(e))

