from django.shortcuts import render
import requests
import lxml
from opensky_api import OpenSkyApi
from .models import Flight

TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    Flight.objects.all().delete()
    api = OpenSkyApi('TanaseRadu', '5fYLPthGn@YAxn6')
    states = api.get_states()
    for s in states.states:
        f=Flight(callsign=s.callsign.strip(), longitude=s.longitude, latitude=s.latitude, altitude=s.geo_altitude, on_ground=s.on_ground)
        f.save()
    return render(request, "index.html")


def check_by_callsign(request):
    test = 'XOJ747'
    flights = Flight.objects.all()
    callsign = ''
    latitude = ''
    longitude = ''
    for flight in flights:
        if(flight.callsign==test):
            callsign = flight.callsign
            latitude = flight.latitude
            longitude = flight.longitude
    return render(request, "check_by_callsign.html",{"callsign":callsign, "latitude":latitude ,"longitude":longitude})


