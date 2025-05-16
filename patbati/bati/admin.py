from django.contrib import admin

from patbati.bati.models import Bati
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

admin.site.register(Bati, LeafletGeoAdmin)
