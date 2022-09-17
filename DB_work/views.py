from django.shortcuts import render
import requests
import lxml
from opensky_api import OpenSkyApi
from .models import Flight, OriginAirports, DestinationAirports
from django.views.decorators.csrf import csrf_exempt
#import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import schedule
import time
from bs4 import BeautifulSoup
import re
from django.conf import settings
from .thread import UpdateFlight, UpdateDBThread
from json import dumps

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

updateDBThread = UpdateDBThread()
updateDBThread.start()

callsign = ''

@login_required()
def check(request):
    return render(request, "index.html")

def about_page(request):
    return render(request, "about.html")

def firstpage(request):
    return render(request, "home.html")
    

def flight_not_tracked(request):
    return render(request, "flight_not_tracked.html")

def statistic(request):
    dest_info = []
    orig_info = []
    orig_JSON = []
    dest_JSON = []
    for item in OriginAirports.objects.all():
        if len(item.airport) !=0 :
            dest_info.append({"airport": item.airport, "tracked_flights":item.number_of_tracked_flights})
    for item in DestinationAirports.objects.all():
        if len(item.airport) !=0 :
            orig_info.append({"airport": item.airport, "tracked_flights":item.number_of_tracked_flights})
    orig_JSON = dumps(orig_info)
    dest_JSON = dumps(dest_info)
    return render(request, "statistic.html", {"origJSON": orig_JSON, "destJSON": dest_JSON})

def check_by_callsign(request):
    test = ''
    flights = Flight.objects.all()
    callsign = ''
    latitude = 46
    longitude = 25
    for flight in flights:
        if (flight.callsign == test):
            callsign = flight.callsign
            latitude = flight.latitude
            longitude = flight.longitude
    return render(request, "check_by_callsign.html", {"latitude": latitude, "longitude": longitude})


def get_flight_by_callsign(request):
    # de adaugat fiecare comanda din if uri intr o functie pe care sa o apelam in if
    input_callsign = request.POST['box_callsign']
    airports = []
    is_in_db = False
    flights = Flight.objects.all()
    altitude = 0
    callsign = ''
    latitude = 0
    longitude = 0
    origin = ''
    destination = ''
    flight_info = []
    dataJSON = []
    for flight in flights:
        if (flight.callsign == input_callsign):
            is_in_db = True
            altitude = flight.altitude
            callsign = flight.callsign
            latitude = flight.latitude
            longitude = flight.longitude
            airports = extractairports(callsign)
            origin = airports[0]
            destination = airports[1]
            flight.origin = origin
            flight.destination = destination
            flight.save()
            flight_info.append({"callsign": callsign, "altitude": altitude, "latitude": latitude,
                                "longitude": longitude, "origin": origin, "destination": destination})
            dataJSON = dumps(flight_info)
            print(dataJSON)
            return render(request, "check_by_callsign.html", {"dataJSON": dataJSON, "is_in_db": is_in_db})
   
    if is_in_db == False:
        return flight_not_tracked(request)

def get_flight_by_origin_airport(request):
    tracked_flights = 0
    is_in_db = False
    dataJSON = []
    input_airport = request.POST['box_origin_airport']
    # Extragere un numar de zboruri ce vor decola/au decolat de pe aeroport
    selected_flights = extractflightsbyorigin(input_airport)
    print("Numere de zbor: ", selected_flights)
    callsign_list = []
    for i in selected_flights:
        # Transformam flight number in callsign
        callsign_to_append = extractcallsign(i)
        if len(callsign_to_append) != 0:
            callsign_list.append(callsign_to_append)
    print("Zboruri de pe aeroport, callsign: ", callsign_list)
    flights_db = Flight.objects.all()
    returned_flights = []
    origin = ''
    destination = ''
    airports = []
    callsign = ''
    for flight in flights_db:
        callsign = ''
        airports = []
        if flight.callsign in callsign_list:  # Cautam in lista de callsign uri obtinuta precedent doar avioanele al caror callsign este prezent si in baza de date
            tracked_flights = tracked_flights + 1
            is_in_db = True
            altitude = flight.altitude
            callsign = flight.callsign
            print("callsign: ", callsign)
            latitude = flight.latitude
            longitude = flight.longitude
            airports = extractairports(callsign)
            print(airports)
            origin = airports[0]
            destination = airports[1]
            flight.origin = origin
            flight.destination = destination
            flight.save()
            returned_flights.append({"latitude": latitude, "longitude": longitude, "origin": origin,"destination": destination, "altitude": altitude, "callsign": callsign})
    o = OriginAirports(airport = input_airport, number_of_tracked_flights = tracked_flights)
    o.save()
    dataJSON = dumps(returned_flights)
    print("aeroporturi: ", dataJSON)
    print("Numar zboruri urmarite care decoleaza de pe aeroportul ", origin, ": ", tracked_flights)
    if is_in_db == False:
        return flight_not_tracked(request)
    else:
        return render(request, "check_by_airports.html", {"dataJSON": dataJSON, "is_in_db": is_in_db})

def get_flight_by_destination_airport(request):
    test = request.POST['box_dest_airport']
    tracked_flights = 0
    is_in_db = False
    dataJSON = []
    input_airport = request.POST['box_dest_airport']
    # Extragere un numar de zboruri ce vor decola/au decolat de pe aeroport
    selected_flights = extractflightsbydestination(input_airport)
    print("Numere de zbor: ", selected_flights)
    callsign_list = []
    for i in selected_flights:
        # Transformam flight number in callsign
        callsign_to_append = extractcallsign(i)
        if len(callsign_to_append) != 0:
            callsign_list.append(callsign_to_append)
    print("Zboruri de pe aeroport, callsign: ", callsign_list)
    flights_db = Flight.objects.all()
    returned_flights = []
    origin = ''
    destination = ''
    airports = []
    callsign = ''
    for flight in flights_db:
        callsign = ''
        airports = []
        if flight.callsign in callsign_list:  # Cautam in lista de callsign uri obtinuta precedent doar avioanele al caror callsign este prezent si in baza de date
            tracked_flights = tracked_flights + 1
            is_in_db = True
            altitude = flight.altitude
            callsign = flight.callsign
            print("callsign: ", callsign)
            latitude = flight.latitude
            longitude = flight.longitude
            airports = extractairports(callsign)
            print(airports)
            origin = airports[0]
            destination = airports[1]
            flight.origin = origin
            flight.destination = destination
            flight.save()
            returned_flights.append({"latitude": latitude, "longitude": longitude, "origin": origin, "destination": destination, "altitude": altitude, "callsign": callsign})
    dataJSON = dumps(returned_flights)
    print("aeroporturi: ", dataJSON)
    print("Numar zboruri urmarite care aterizeaza pe aeroportul ", destination, ": ", tracked_flights)
    o = DestinationAirports(airport = input_airport, number_of_tracked_flights = tracked_flights)
    o.save()
    if is_in_db == False:
        return flight_not_tracked(request)
    else:
        return render(request, "check_by_airports.html", {"dataJSON": dataJSON, "is_in_db": is_in_db})

def extractairports(callsign):  # functie pentru obtinerea aeroporturilor
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://www.radarbox.com/data/flights/" + callsign 
    f = requests.get(url, headers=agent)
    soup = BeautifulSoup(f.content, "html.parser")
    try:
        airports = soup.find_all("div", {"id": "code"})
        origin = str(airports[0].text)
        destination = str(airports[1].text)
        origin = origin.replace(' ', '').replace('(', '').replace(')', '')
        destination = destination.replace(
            ' ', '').replace('(', '').replace(')', '')
        print("Origin airport: ", origin)
        print("Destination airport: ", destination)
        return [origin, destination]
    except:
        return ["invalid", "invalid"]


# functie pentru obtinerea zborurilor cu aeroportul de origine predefinit
def extractflightsbyorigin(airport):
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://www.radarbox.com/data/airports/"+airport+"?tab=departures"
    f = requests.get(url, headers=agent)
    soup = BeautifulSoup(f.content, "html.parser")
    test = soup.find_all("td", {"id": "fn"})
    list = []
    for i in test:
        list.append(i.text)
    return list


# functie pentru obtinerea zborurilor cu aeroportul destinatie  predefinit
def extractflightsbydestination(airport):
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://www.radarbox.com/data/airports/"+airport+"?tab=arrivals"
    f = requests.get(url, headers=agent)
    soup = BeautifulSoup(f.content, "html.parser")
    test = soup.find_all("td", {"id": "fn"})
    list = []
    for i in test:
        list.append(i.text)
    return list


# Functie pentru transformarea flight-number ului in callsign
def extractcallsign(flight_number):
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://www.radarbox.com/data/flights/" + flight_number
    callsign = ""
    try:
        f = requests.get(url, headers=agent)
        soup = BeautifulSoup(f.content, "html.parser")
        test = soup.find("div", {"id": "secondary"})
        callsign = test.text
        print(callsign)
    except:
        print("Callsign ul nu a putut fi obtinut")
    return callsign


@csrf_exempt
@login_required
def get_info(request):

    if 'box_callsign' in request.POST:
        global callsign
        callsign = return_callsign(request.POST['box_callsign'])
        updateFlightThread=UpdateFlight(request.POST['box_callsign'])
        updateFlightThread.start()
        return get_flight_by_callsign(request)
    elif 'box_dest_airport' in request.POST:  # zboruri care pleaca de pe un anumit aeroport
        return get_flight_by_destination_airport(request)
    elif 'box_origin_airport' in request.POST:
        return get_flight_by_origin_airport(request)
    elif 'box_airport' in request.POST:
        test = request.POST['box_airport']
    return render(request, "flights.html", context={})


def return_callsign(callsign):
    return callsign