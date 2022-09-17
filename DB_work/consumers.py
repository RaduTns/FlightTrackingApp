from channels.generic.websocket import WebsocketConsumer
import json
from time import sleep
from random import randint
from DB_work.models import Flight
from DB_work import views

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(15):
            callsign = views.callsign
            print(callsign)
            flight = Flight.objects.get(pk=callsign)
            latitude = flight.latitude
            longitude = flight.longitude
            self.send(json.dumps({'message': [latitude,longitude]} ))    
            sleep(2)
        self.close()