from functools import total_ordering
import threading
from django.shortcuts import render
import requests
import lxml
from opensky_api import OpenSkyApi
from .models import Flight
from django.views.decorators.csrf import csrf_exempt
#import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import schedule
import time
from bs4 import BeautifulSoup
import re
from django.conf import settings


class UpdateDBThread(threading.Thread):
    def __init__(self):
        #threading.Thread.__init__(self)
        super(UpdateDBThread, self).__init__()
        self._stop_event = threading.Event()
    def run(self):
        try:
            while True:
                print("thread exec started")
                Flight.objects.all().delete()
                api = OpenSkyApi(settings.API_USERNAME, settings.API_PASSWORD)
                flights = api.get_states()
                for s in flights.states:
                    f=Flight(callsign=s.callsign.strip(), longitude=s.longitude, latitude=s.latitude, altitude=s.geo_altitude, on_ground=s.on_ground)
                    f.save()
                print("S a facut update la DB")
                time.sleep(1200)
        except Exception as e:
            print("exception:", e)

        

class UpdateFlight(threading.Thread):
    def __init__(self, flight_callsign):
        threading.Thread.__init__(self)
        self.flight_callsign = flight_callsign
    def run(self):
        try:
            print("thread exec started")
            i=0
            while i<=15:
                i=i+1
                api = OpenSkyApi(settings.API_USERNAME, settings.API_PASSWORD)
                states = api.get_states()
                for s in states.states:
                    if s.callsign.strip()==self.flight_callsign:
                        tracked_flight = Flight.objects.get(pk=self.flight_callsign)
                        tracked_flight.longitude = s.longitude
                        tracked_flight.latitude = s.latitude
                        tracked_flight.save()
                print("S a facut update la zborul ",self.flight_callsign, " iteratia ", i)
                time.sleep(2)
        except Exception as e:
            print("exception")
    

                