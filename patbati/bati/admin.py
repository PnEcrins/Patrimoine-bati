from django.contrib import admin
from patbati.bati.models import Bati, Nomenclature, NomenclatureType
from leaflet.admin import LeafletGeoAdmin

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