import json
from django import template
from django.conf import settings
from django.urls import reverse


from zoning.models import AreaType
register = template.Library()


@register.simple_tag
def areas_type():
    filtered_area_type = AreaType.objects.filter(
        code__in=settings.ZONING_CONFIG["REGULATORY_AREAS"] + settings.ZONING_CONFIG["ADMINISTRATIVE_AREAS"]
    )
    areas_list = []
    for area_type in filtered_area_type:
        url = reverse('zoning:zoning_layer',
                                kwargs={'area_type': area_type.code})
        areas_list.append({
            "name": area_type.name,
            "url": url,
            "id": area_type.id_type,
            "isActive": False
        })
    return json.dumps(areas_list)
