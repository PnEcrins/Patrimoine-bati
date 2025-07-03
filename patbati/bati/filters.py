import django_filters
from .models import Bati, Nomenclature

class BatiFilterSet(django_filters.FilterSet):
    appelation = django_filters.CharFilter(lookup_expr='icontains', label="Recherche par nom")
    classe = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code='CL_ARCHI'),
        label="Type d'archi"
    )
    equipements = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code='EQUIP'),
        label="Équipement",
        field_name="equipements__type"
    )
    perspectives = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code='PERSP'),
        label="Perspective",
        field_name="perspectives"
    )
    class Meta:
        model = Bati
        fields = ['appelation', 'classe', 'equipements', 'perspectives']