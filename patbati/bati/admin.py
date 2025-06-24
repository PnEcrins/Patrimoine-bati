from django.contrib import admin
from patbati.bati.models import Bati, Nomenclature, NomenclatureType
from leaflet.admin import LeafletGeoAdmin

@admin.register(Bati)
class BatiAdmin(LeafletGeoAdmin):
    list_display = (
        "id",
        "valide",
        "appelation",
        "secteur",
        "conservation",
        "notepatri",
        "classe",
        "date_insert",
        "date_update",
    )
    search_fields = ("appelation", "proprietaire", "cadastre", "lieu_dit")
    list_filter = ("secteur", "conservation", "classe", "valide", "bat_suppr")

@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = (
        "id_nomenclature",
        "id_type",
        "label",
        "description",
        "parentId",
    )
    search_fields = ("label", "description")
    list_filter = ("id_type",)

@admin.register(NomenclatureType)
class NomenclatureTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id_type",
        "label",
        "definition",
        "code",
    )
    search_fields = ("label", "code")