from django.http import HttpResponse
from mapentity.views.generic import (
    MapEntityList, MapEntityDetail,
    MapEntityFormat, MapEntityCreate, MapEntityUpdate, MapEntityDocument,
    MapEntityDelete
)
from mapentity.views.api import MapEntityViewSet
from patbati.bati.forms import EnquetesForm
from .models import Bati, Enquetes
from .serializers import BatiSerializer, BatiGeojsonSerializer
from django.views.generic.edit import CreateView

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

class BatiCreate(MapEntityCreate):
    model = Bati

class BatiFormat(MapEntityFormat, BatiList):
    pass

class BatiViewSet(MapEntityViewSet):
    model = Bati
    serializer_class = BatiSerializer
    geojson_serializer_class = BatiGeojsonSerializer
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    # filterset_class = DummyModelFilterSet

    queryset = Bati.objects.all()

class EnquetesCreate(CreateView):
    model = Enquetes
    form_class = EnquetesForm
    template_name = "bati/enquetes_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.bati = Bati.objects.get(pk=kwargs['bati_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.id_bat = self.bati
        return super().form_valid(form)

    def get_success_url(self):
        return self.bati.get_detail_url()