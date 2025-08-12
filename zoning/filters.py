import django_filters
from django import forms
from django.db.models import Q

from .models import Area


class AreaIntersectionFilter(django_filters.ModelMultipleChoiceFilter):
    model = Area

    def filter(self, qs, value):
        q = Q()
        for subvalue in value:
            q |= Q(geom__intersects=subvalue.geom_4326)
        return qs.filter(q)
