from django.conf import settings
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

from zoning.models import Area

class AreaSerializer(geo_serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Area
        geo_field = 'geom_4326'
        id_field = False
        fields = ["name"]
