import datetime

from django import forms
from django.forms.models import inlineformset_factory

from mapentity.forms import MapEntityForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from patbati.mapentitycommon.forms import ChildFormHelper
from .models import Enquetes, Bati, DemandeTravaux, Perspective


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