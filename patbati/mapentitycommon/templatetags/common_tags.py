from functools import reduce

from django import template
from django.conf import settings

register = template.Library()


def get_from_dict(d: dict, key: str):
    """Iterate nested dictionary"""
    key_as_list = key.split(".")
    return reduce(dict.get, key_as_list, d)


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
