from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from zoning.serializers import AreaSerializer
from zoning.models import Area


class ZoningGeoJsonViewList(ListAPIView):
    serializer_class = AreaSerializer
    # because mapentity add globally MapEntityRestPermissions class
    # use must have a 'read' (and not a 'view') permissions.
    # with IsAuthenticated the user must only be logged
    permission_classes = [IsAuthenticated]
    model = Area

    def get_queryset(self):
        area_type = self.kwargs["area_type"]
        return Area.objects.filter(type__code=area_type)
