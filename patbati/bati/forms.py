import datetime

from django import forms
from django.forms.models import inlineformset_factory

from mapentity.forms import MapEntityForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from patbati.mapentitycommon.forms import ChildFormHelper
from .models import Enquetes, Bati, DemandeTravaux, MateriauxFinFinitionSecondOeuvre, MateriauxFinFinitionStructure, Perspective, SecondOeuvre, Structure, Travaux


class EnquetesForm(ChildFormHelper):

    class Meta:
        model = Enquetes
        exclude = ['bati']

class PerspectiveForm(ChildFormHelper):
    class Meta:
        model = Perspective
        exclude = ['bati']

    date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )


# class DemandeTravauxForm(forms.ModelForm):
#     class Meta:
#         model = DemandeTravaux
#         fields = ("id", "demande_dep", "autorisation_p", "date_permis")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         # self.helper.layout = Layout('id', 'demande_dep', 'autorisation_p', 'date_permis')

# DemandeTravauxFormSet = inlineformset_factory(Bati, DemandeTravaux, form=DemandeTravauxForm, extra=1)

class DemandeTravauxForm(ChildFormHelper):
    class Meta:
        model = DemandeTravaux
        exclude = ['bati']
        widgets = {
            'date_permis': forms.DateInput(
                attrs={
                    'type': 'date',             
                }
            ),
            'date_demande_permis': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }

class TravauxForm(ChildFormHelper):
    class Meta:
        model = Travaux
        exclude = ['demande']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }
    
class BatiForm(MapEntityForm):
    class Meta():
        model = Bati
        exclude = []
    # TODO : ajouter les champs un par un...
    # fieldslayout = [
    #     Div(
    #         'appelation',
    #         Fieldset("DemandeTravaux")
    #     )
    # ]

class StructureForm(ChildFormHelper):
    class Meta:
        model = Structure
        fields = ['type', 'est_remarquable', 'conservation', 'materiaux_principal', 'mise_en_oeuvre', 'info_structure']

class SecondOeuvreForm(ChildFormHelper):
    class Meta:
        model = SecondOeuvre
        fields = ['type', 'est_remarquable', 'conservation', 'commentaire']

class MateriauFinFinitionStructureForm(ChildFormHelper):
    class Meta:
        model = MateriauxFinFinitionStructure
        fields = ['materiaux_fin', 'finition']

class MateriauFinFinitionSecondOeuvreForm(ChildFormHelper):
    class Meta:
        model = MateriauxFinFinitionSecondOeuvre
        fields = ['materiaux_fin', 'finition']