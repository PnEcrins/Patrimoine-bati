from django.conf import settings
from django.utils.functional import cached_property

from .settings import app_settings

from .models import Area


class AreaPropertyMixin:
    # geom column of l_area table on which make the intersection
    AREA_GEOM_COLUMN = "geom_local"
    # geom column of the join model on which make the intersection
    MODEL_GEOM_COLUMN = "geom"

    @cached_property
    def areas(self):
        # dynamicly build a filter with AREA_GEOM_COLUMN and MODEL_GEOM_COLUMN
        # at the end it looks like this : Area.objects.filter(geom_4326__intersects=self.geom)
        filter = {
            f"{self.AREA_GEOM_COLUMN}__intersects": getattr(
                self, self.MODEL_GEOM_COLUMN
            )
        }
        qs = Area.objects.filter(**filter)
        if app_settings["AREA_TYPE_LIMITED"]:
            qs = qs.filter(type__code__in=settings.ZONING_CONFIG["AREA_TYPE_LIMITED"])
        return qs
