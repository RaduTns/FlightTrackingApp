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

TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR, "templates"),'
)

@login_required()
def check(request):
    return render(request, "index.html")

def firstpage(request):
    #db_feed()
    return render(request, "home.html")



def db_feed():
    Flight.objects.all().delete()
    api = OpenSkyApi('TanaseRadu', '5fYLPthGn@YAxn6')
    states = api.get_states()
    for s in states.states:
        f=Flight(callsign=s.callsign.strip(), longitude=s.longitude, latitude=s.latitude, altitude=s.geo_altitude, on_ground=s.on_ground)
        f.save()

def index(request):
    Flight.objects.all().delete()
    api = OpenSkyApi('TanaseRadu', '5fYLPthGn@YAxn6')
    states = api.get_states()
    for s in states.states:
        f=Flight(callsign=s.callsign.strip(), longitude=s.longitude, latitude=s.latitude, altitude=s.geo_altitude, on_ground=s.on_ground)
        f.save()
    return render(request, "home.html")


def check_by_callsign(request):
    test = 'CAT318'
    flights = Flight.objects.all()
    callsign = ''
    latitude = 46
    longitude = 25
    for flight in flights:
        if(flight.callsign==test):
            callsign = flight.callsign
            latitude = flight.latitude
            longitude = flight.longitude
    return render(request, "check_by_callsign.html",{"latitude":latitude ,"longitude":longitude})


@csrf_exempt
@login_required
def get_info(request):  
    test = ""
    info = 0
    if 'box_callsign' in request.POST:
        boolean = False
        test=request.POST['box_callsign']
        info = 1
        flights = Flight.objects.all()
        callsign = ''
        latitude = 0
        longitude = 0
        for flight in flights:
            if(flight.callsign==test):
                boolean = True
                callsign = flight.callsign
                latitude = flight.latitude
                longitude = flight.longitude
        
        return render(request, "check_by_callsign.html",{"latitude":latitude ,"longitude":longitude, "boolean":boolean})
    elif 'box_dest_airport' in request.POST:
        test=request.POST['box_dest_airport']
        info = 2
    elif 'box_origin_airport' in request.POST:
        test=request.POST['box_origin_airport']
        info = 3
    elif 'box_airport' in request.POST:
        test=request.POST['box_airport']
        info = 4
    print("Test: ", test)
    return render(request, "flights.html")



