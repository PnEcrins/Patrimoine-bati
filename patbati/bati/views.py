from django.http import HttpResponse
from mapentity.views.generic import (
    MapEntityList, MapEntityDetail,
    MapEntityFormat, MapEntityCreate, MapEntityUpdate, MapEntityDocument,
    MapEntityDelete
)
from mapentity.views.api import MapEntityViewSet
from .models import Bati
from .serializers import BatiSerializer, BatiGeojsonSerializer

# Create your views here.


def home(request):
    return HttpResponse("YEP")

class BatiList(MapEntityList):
    model = Bati
    columns = ["id", "appelation"]

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
