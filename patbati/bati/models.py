from django.db import models

# Create your models here.


from django.contrib.gis.db import models
from mapentity.models import MapEntityMixin


class Bati(MapEntityMixin, models.Model):
    id = models.AutoField(primary_key=True)
    geom = models.PointField()
    name = models.CharField(max_length=80)
    altitude = models.FloatField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    proprietaire = models.ForeignKey('Proprietaire', on_delete=models.CASCADE, blank=True, null=True) # propriétaire
    patrimonialite = models.ForeignKey('Patrimonialite', on_delete=models.CASCADE, blank=True, null=True) # patrimoinalité
    cadastre = models.ForeignKey('Cadastre', on_delete=models.CASCADE, blank=True, null=True) # référence cadastrale
    situation_geo = models.CharField(max_length=200, blank=True, null=True) # description de la situation géographique

class Proprietaire(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    def __str__(self):
        return self.name

class Patrimonialite(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name    

class Cadastre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name