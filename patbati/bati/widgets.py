from django.forms.widgets import Select

class SelectWithTitle(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(Select, self).create_option(name, value, label, selected, index, subindex, attrs)
        print("LAAAAAAAAAAAAAAAAAAAAAa", self)
        option['attrs']['title'] = "SUPER TITLE"
        return option