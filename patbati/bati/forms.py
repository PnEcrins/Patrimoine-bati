from django import forms
from .models import Enquetes

class EnquetesForm(forms.ModelForm):
    class Meta:
        model = Enquetes
        exclude = ['id_bat']