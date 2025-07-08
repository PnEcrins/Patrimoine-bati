from mapentity.filters import BaseMapEntityFilterSet

from attr import field
import django_filters
from django import forms
from .models import Bati, Nomenclature

class EmptyLabelChoiceFilterMixin:
    """
    Put empty label = verbose name for ChoiceField
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.base_filters.keys():
            field = self.form.fields[fieldname]
            if isinstance(field, forms.ChoiceField):
                field.empty_label = field.label


class BatiFilterSet(EmptyLabelChoiceFilterMixin, BaseMapEntityFilterSet):
    appelation = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Recherche par nom",
        widget=forms.TextInput(attrs={'placeholder': 'Nom du bâtiment'})
    )

    # # @TODO: ref_geo --> zone geopgraphique sur carte
    # # secteur = django_filters.ModelChoiceFilter(
    # #     queryset=Nomenclature.objects.filter(id_type__code='SECTEUR'),
    # #     label="Secteur",
    # #     empty_label="Secteur"
    # # )

    class Meta:
        model = Bati
        fields = [
            'appelation', 'classe',
            # 'secteur',
            'notepatri', 'conservation', 'exposition',
            'faitage', 'implantation', 'proprietaire', 'valide', 'indivision', 'bat_suppr', 'protection', 'masques',
            'risques_nat', 'perspectives'
        ]