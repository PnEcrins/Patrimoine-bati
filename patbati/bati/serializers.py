from rest_framework import serializers
from mapentity.serializers import MapentityGeojsonModelSerializer

from .models import Bati

class BatiSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Bati

class BatiGeojsonSerializer(MapentityGeojsonModelSerializer):
    class Meta(MapentityGeojsonModelSerializer.Meta):
        fields = ["id", "appelation"]
        model = Bati