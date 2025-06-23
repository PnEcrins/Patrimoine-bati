from django.contrib import admin

from patbati.bati.models import Bati, Nomenclature, NomenclatureType
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

admin.site.register(Bati, LeafletGeoAdmin)
admin.site.register(Nomenclature)
admin.site.register(NomenclatureType)
