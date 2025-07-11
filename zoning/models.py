from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models


# Create your models here.


class AreaType(models.Model):
    class Meta:
        db_table = "bib_areas_types"
        managed = False

    id_type = models.AutoField(primary_key=True)
    name = models.CharField(200, db_column="type_name")
    code = models.CharField(50, db_column="type_code")
    desc = models.TextField(db_column="type_desc")
    ref_name = models.CharField(200)
    ref_version = models.IntegerField()
    num_version = models.CharField(50)
    size_hierarchy = models.IntegerField()


class Area(models.Model):
    class Meta:
        db_table = "l_areas"
        managed = False

    id_area = models.AutoField(primary_key=True)
    type = models.ForeignKey(AreaType, on_delete=models.CASCADE, db_column="id_type")
    name = models.CharField(250, db_column="area_name")
    code = models.CharField(25, db_column="area_code")
    geom = gis_models.MultiPolygonField(srid=settings.LOCAL_SRID)
    centroid = gis_models.PointField(srid=settings.LOCAL_SRID)
    source = models.CharField(255)
    comment = models.TextField()
    enable = models.BooleanField()
    geom_4326 = gis_models.MultiPolygonField(srid=4326)
    # description = models.TextField()

    def __str__(self):
        return self.name
