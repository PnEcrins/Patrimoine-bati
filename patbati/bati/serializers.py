from rest_framework import serializers
from mapentity.serializers import MapentityGeojsonModelSerializer

from .models import Bati

class BatiSerializer(serializers.ModelSerializer):
    appelation = serializers.CharField(source='appelation_link')
    type_bat = serializers.CharField(source='type_bat_label')
    conservation = serializers.CharField()
    notepatri = serializers.CharField()
    class Meta:
        fields = "__all__"
        model = Bati

class BatiGeojsonSerializer(MapentityGeojsonModelSerializer):
    color = serializers.SerializerMethodField()

    def get_color(self, obj):
        if obj.valide: 
            return "#48EE15"
        return "#EE2E15"
    
    class Meta(MapentityGeojsonModelSerializer.Meta):
        fields = ["id", "appelation", "color"]
        model = Bati