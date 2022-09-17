from django.contrib import admin
from .models import DestinationAirports, Flight, OriginAirports
# Register your models here.

admin.site.register(Flight)
admin.site.register(OriginAirports)
admin.site.register(DestinationAirports)