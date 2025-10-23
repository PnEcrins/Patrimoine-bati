import datetime

from django import forms
from django.forms.models import inlineformset_factory

from mapentity.forms import MapEntityForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Fieldset

from patbati.mapentitycommon.forms import ChildFormHelper
from .models import (
    Enquetes,
    Bati,
    DemandeTravaux,
    MateriauxFinFinitionSecondOeuvre,
    MateriauxFinFinitionStructure,
    Perspective,
    SecondOeuvre,
    Structure,
    Travaux,
)


class EnquetesForm(ChildFormHelper):

    class Meta:
        model = Enquetes
        exclude = ["bati"]


class PerspectiveForm(ChildFormHelper):
    class Meta:
        model = Perspective
        exclude = ["bati"]

    date = forms.DateField(
        initial=datetime.date.today,
    )



class DemandeTravauxForm(ChildFormHelper):
    class Meta:
        model = DemandeTravaux
        exclude = ["bati"]



class TravauxForm(ChildFormHelper):
    class Meta:
        model = Travaux
        exclude = ["demande"]


from .widgets import SelectWithTitle
class BatiForm(MapEntityForm):

    fieldslayout = [
        Div(
            "appelation",
            "type_bat"
        ),
        Div(
            Fieldset(
                "Description du batiment",
                "classe",
                "annee_construction",
                "implantation",
                "faitage",
                "surface",
                "conservation",
                "notepatri",
                "patrimonialite",
            )
        ),
        Div(
            Fieldset(
                "Info propriétaire",
                "proprietaire",
                "type_prioprietaire",
                "indivision",
                "periode_utilisation",
                "comment_proprio"
            )
        ),
        Div(
            Fieldset(
                "Localisation",
                "cadastre",
                "lieu_dit",
                "altitude",
                "exposition",
                "masques",
                "commentaire_masque",
                "risques_nat",
                "remarque_risque",
                "situation_geo",
            )
        ),
        Div(
            Fieldset(
                "Autre",
                "perspectives",
                "remarque_generale",
                "valide"
            )
        )
    ]

    
    class Meta:
        model = Bati
        exclude = ["x", "y", "bat_suppr", "date_update"]



class StructureForm(ChildFormHelper):
    class Meta:
        model = Structure
        fields = [
            "type",
            "est_remarquable",
            "conservation",
            "materiaux_principal",
            "mise_en_oeuvre",
            "info_structure",
        ]


class SecondOeuvreForm(ChildFormHelper):
    class Meta:
        model = SecondOeuvre
        fields = ["type", "est_remarquable", "conservation", "commentaire"]


class MateriauFinFinitionStructureForm(ChildFormHelper):
    class Meta:
        model = MateriauxFinFinitionStructure
        fields = ["materiaux_fin", "finition"]


class MateriauFinFinitionSecondOeuvreForm(ChildFormHelper):
    class Meta:
        model = MateriauxFinFinitionSecondOeuvre
        fields = ["materiaux_fin", "finition"]

