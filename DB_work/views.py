from django.shortcuts import render
import requests
import lxml
from opensky_api import OpenSkyApi
from .models import Flight
from django.views.decorators.csrf import csrf_exempt
import re
from django.contrib.auth.decorators import login_required

TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR, "templates"),'
)


def firstpage(request):
    return render(request, "home.html")

def index(request):
    Flight.objects.all().delete()
    api = OpenSkyApi('TanaseRadu', '5fYLPthGn@YAxn6')
    states = api.get_states()
    for s in states.states:
        f=Flight(callsign=s.callsign.strip(), longitude=s.longitude, latitude=s.latitude, altitude=s.geo_altitude, on_ground=s.on_ground)
        f.save()
    return render(request, "index.html")


def check_by_callsign(request):
    test = 'VVC460'
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
def get_info(request):  
    test = ""
    info = 0
    if 'box_callsign' in request.POST:
        test=request.POST['box_callsign']
        info = 1
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
