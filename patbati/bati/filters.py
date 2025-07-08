from attr import field
import django_filters
from django import forms
from .models import Bati, Nomenclature


class BatiFilterSet(django_filters.FilterSet):
    appelation = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Recherche par nom",
        widget=forms.TextInput(attrs={"placeholder": "Nom du bâtiment"}),
    )
    classe = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="CL_ARCHI"),
        label="Type d'archi",
        empty_label="Type d'architecture",
    )
    # @TODO: ref_geo --> zone geopgraphique sur carte
    # secteur = django_filters.ModelChoiceFilter(
    #     queryset=Nomenclature.objects.filter(id_type__code='SECTEUR'),
    #     label="Secteur",
    #     empty_label="Secteur"
    # )
    notepatri = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="NOTE_PAT"),
        label="Note patrimoniale",
        empty_label="Note patrimoniale",
    )
    conservation = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="CONSERVATION"),
        label="Conservation",
        empty_label="Conservation",
    )
    exposition = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="EXPO"),
        label="Exposition",
        empty_label="Exposition",
    )
    faitage = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="FAITAGE"),
        label="Faitage",
        empty_label="Faitage",
    )
    implantation = django_filters.ModelChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="IMPLA"),
        label="Implantation",
        empty_label="Implantation",
    )
    proprietaire = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Propriétaire",
        widget=forms.TextInput(attrs={"placeholder": "Nom du propriétaire"}),
    )
    valide = django_filters.BooleanFilter(
        label="Validé",
        widget=forms.Select(choices=[("", "Validé"), (True, "Oui"), (False, "Non")]),
    )
    indivision = django_filters.BooleanFilter(
        label="Indivision",
        widget=forms.Select(
            choices=[("", "Indivision"), (True, "Oui"), (False, "Non")]
        ),
    )
    bat_suppr = django_filters.BooleanFilter(
        label="Bâtiment supprimé",
        widget=forms.Select(
            choices=[("", "Batiment supprimé"), (True, "Oui"), (False, "Non")]
        ),
    )
    protection = django_filters.ModelMultipleChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="PROT"),
        label="Protection",
    )
    masques = django_filters.ModelMultipleChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="MASQUE"),
        label="Masques",
    )
    risques_nat = django_filters.ModelMultipleChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="RISQUE"),
        label="Risques naturels",
    )
    perspectives = django_filters.ModelMultipleChoiceFilter(
        queryset=Nomenclature.objects.filter(id_type__code="PERSP"),
        label="Perspectives",
    )

    class Meta:
        model = Bati
        fields = [
            "appelation",
            "classe",
            # 'secteur',
            "notepatri",
            "conservation",
            "exposition",
            "faitage",
            "implantation",
            "proprietaire",
            "valide",
            "indivision",
            "bat_suppr",
            "protection",
            "masques",
            "risques_nat",
            "perspectives",
        ]
