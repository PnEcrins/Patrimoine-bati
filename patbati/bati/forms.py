from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from .models import Enquetes, Bati, DemandeTravaux

class EnquetesForm(forms.ModelForm):
    class Meta:
        model = Enquetes
        exclude = ['id_bat']

class DemandeTravauxForm(forms.ModelForm):
    class Meta:
        model = DemandeTravaux
        fields = ("id", "demande_dep", "autorisation_p", "date_permis")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.layout = Layout('id', 'demande_dep', 'autorisation_p', 'date_permis')

DemandeTravauxFormSet = inlineformset_factory(Bati, DemandeTravaux, form=DemandeTravauxForm, extra=1)

from mapentity.forms import MapEntityForm
from django.forms import FloatField, ModelChoiceField
from crispy_forms.layout import Div, Fieldset, Layout

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