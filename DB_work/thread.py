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

class updateDB(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        try:
            while True:
                print("thread exec started")
                Flight.objects.all().delete()
                api = OpenSkyApi(settings.API_USERNAME, settings.API_PASSWORD)
                states = api.get_states()
                for s in states.states:
                    callsign = s.callsign.strip()
                    f=Flight(callsign=s.callsign.strip(), longitude=s.longitude, latitude=s.latitude, altitude=s.geo_altitude, on_ground=s.on_ground)
                    f.save()
                print("S a facut update la DB")
                time.sleep(600)
        except Exception as e:
            print("exception")

                