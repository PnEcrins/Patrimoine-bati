from django.conf import settings

app_settings = dict({
    "LOCAL_SRID":  2154,
    "AREA_TYPE_LIMITED": []
}, **getattr(settings, 'ZONING_CONFIG', {}))