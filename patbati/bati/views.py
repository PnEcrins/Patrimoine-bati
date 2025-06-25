from django.http import HttpResponse
from django.views.generic.edit import CreateView
from mapentity.views.generic import (
    MapEntityList, MapEntityDetail,
    MapEntityFormat, MapEntityCreate, MapEntityUpdate, MapEntityDocument,
    MapEntityDelete
)
from mapentity.views.api import MapEntityViewSet
from mapentity.views.mixins import ModelViewMixin
from patbati.bati.forms import EnquetesForm, DemandeTravauxFormSet, BatiForm, PerspectiveForm
from .models import Bati, Enquetes, Perspective
from .serializers import BatiSerializer, BatiGeojsonSerializer
from patbati.mapentitycommon.forms import FormsetMixin
from patbati.mapentitycommon.views import ChildFormViewViewMixin
# Create your views here.


def home(request):
    return HttpResponse("YEP")


class BatiList(MapEntityList):
    model = Bati
    columns = [
        "id",
        "valide",
        "appelation",
        "secteur",
        "notepatri",
        "conservation",
        "date_update"
    ]

class BatiDetail(MapEntityDetail):
    model = Bati


# class BatiCreate(FormsetMixin, MapEntityCreate):
#     model = Bati
#     context_name = 'demande_travaux_formset'
#     form_class = BatiForm
#     formset_class = DemandeTravauxFormSet



class BatiCreate(MapEntityCreate):
    model = Bati
    form_class = BatiForm



class BatiFormat(MapEntityFormat, BatiList):
    pass

class BatiViewSet(MapEntityViewSet):
    model = Bati
    serializer_class = BatiSerializer
    geojson_serializer_class = BatiGeojsonSerializer

    queryset = Bati.objects.all()

class EnquetesCreate(ChildFormViewViewMixin, CreateView):
    model = Enquetes
    parent_model = Bati
    parent_related_name = "bati"
    form_class = EnquetesForm
    template_name = "bati/enquetes_form.html"

class PerspectiveCreate(ChildFormViewViewMixin, CreateView):
    model = Perspective
    parent_model = Bati
    form_class = PerspectiveForm
    parent_related_name = "bati"
    template_name = "bati/perspectives_form.html"




    
    