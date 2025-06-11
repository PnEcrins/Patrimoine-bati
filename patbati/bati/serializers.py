from rest_framework import serializers
from mapentity.serializers import MapentityGeojsonModelSerializer

from .models import Bati

class BatiSerializer(serializers.ModelSerializer):
    appelation = serializers.CharField(source='appelation_link')
    code_classe = serializers.CharField(source='code_classe_label')
    notepatri = serializers.CharField(source='notepatri_label')
    codeconservation = serializers.CharField(source='codeconservation_label')
    secteur = serializers.CharField(source='secteur_label')
    class Meta:
        fields = "__all__"
        model = Bati

class BatiGeojsonSerializer(MapentityGeojsonModelSerializer):
    class Meta(MapentityGeojsonModelSerializer.Meta):
        fields = ["id", "appelation"]
        model = Bati