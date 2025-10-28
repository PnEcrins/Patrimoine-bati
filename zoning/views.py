from rest_framework.generics import ListAPIView

from zoning.serializers import AreaSerializer
from zoning.models import Area


class ZoningGeoJsonViewList(ListAPIView):
    serializer_class = AreaSerializer
    model = Area

    def get_queryset(self):
        area_type = self.kwargs["area_type"]
        return Area.objects.filter(type__code=area_type)
