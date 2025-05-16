from django.db import models

# Create your models here.


from django.contrib.gis.db import models
from mapentity.models import MapEntityMixin


class Bati(MapEntityMixin, models.Model):
    geom = models.PointField()
    name = models.CharField(max_length=80)