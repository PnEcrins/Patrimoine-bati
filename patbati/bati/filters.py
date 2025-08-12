import django_filters
from mapentity.filters import BaseMapEntityFilterSet
from django.db.models import Exists, OuterRef

from django import forms
from patbati.bati.models import Bati
from zoning.models import Area
from zoning.filters import AreaIntersectionFilter


class EmptyLabelChoiceFilterMixin:
    """
    Put empty label = verbose name for ChoiceField
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.base_filters.keys():
            field = self.form.fields[fieldname]
            if isinstance(field, django_filters.fields.ModelChoiceField):
                field.empty_label = field.label

class SiteInscritClassFilter(django_filters.ChoiceFilter):
    def filter(self, qs, value):
        if value:
            matching_areas = Area.objects.filter(geom_4326__intersects=OuterRef("geom")).filter(type__code__in=["SITE_INSC", "SITE_CLASSES"])
            return qs.filter(Exists(matching_areas))
        return qs

class BatiFilterSet(EmptyLabelChoiceFilterMixin, BaseMapEntityFilterSet):
    appelation = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Recherche par nom",
        widget=forms.TextInput(attrs={"placeholder": "Nom du bâtiment"}),
    )

    secteur = AreaIntersectionFilter(
        queryset=Area.objects.filter(type__code="SEC"),
        label="Secteurs",
    )

    communes = AreaIntersectionFilter(
        queryset=Area.objects.filter(type__code="COM", enable=True),
        label="Communes",
    )

    zone_reg = AreaIntersectionFilter(
        queryset=Area.objects.filter(type__code__in=("PPN", "ZC", "PEC"), enable=True),
        label="Zones reglémentées",
    )

    site_inscrits_classse = SiteInscritClassFilter(
        choices=[(True, "Oui")],
        empty_label='Sites inscrit et classé'
    )

    class Meta:
        model = Bati
        fields = [
            "appelation",
            "classe",
            "type_bat",
            "notepatri",
            "conservation",
            "exposition",
            "faitage",
            "implantation",
            "proprietaire",
            "valide",
            "indivision",
            "bat_suppr",
            "masques",
            "risques_nat",
            "perspectives",
        ]
