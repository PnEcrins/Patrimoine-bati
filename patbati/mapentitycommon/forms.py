from django.core.exceptions import ValidationError
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ChildFormHelper(forms.ModelForm):
    """
        Add a crispy form helper and submit button to form
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enregistrer', css_class='btn-success'))


class FormsetMixin:
    context_name = None
    formset_class = None

    def form_valid(self, form):
        context = self.get_context_data()
        formset_form = context[self.context_name]

        if formset_form.is_valid():
            response = super().form_valid(form)
            formset_form.instance = self.object
            formset_form.save()
        else:
            response = self.form_invalid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            try:
                context[self.context_name] = self.formset_class(
                    self.request.POST, instance=self.object)
            except ValidationError:
                pass
        else:
            context[self.context_name] = self.formset_class(
                instance=self.object)
            print("context", context)
        return context
