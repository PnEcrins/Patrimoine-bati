import django
from django.db import models

# Create your models here.


from django.contrib.gis.db import models
from mapentity.models import MapEntityMixin

# ancienement table: identification
class Bati(MapEntityMixin, models.Model):
    id = models.AutoField(primary_key=True) # indexBatiment
    codepem = models.ForeignKey('Implantation', on_delete=models.CASCADE, blank=True, null=True) # codepem
    codeclasse = models.ForeignKey('ClasseArchitecturale', on_delete=models.CASCADE, blank=True, null=True) # codeclasse
    codefaitage = models.ForeignKey('Faitage', on_delete=models.CASCADE, blank=True, null=True) # codefaitage
    codeinsee = models.ForeignKey('Commune', on_delete=models.CASCADE, blank=True, null=True) # codeinsee
    appelation = models.CharField(max_length=200, blank=True, null=True) # appellation
    indivision = models.BooleanField(default=False, null=True) # indivision
    proprietaire = models.CharField(max_length=100, blank=True, null=True) # propriétaire
    cadastre = models.CharField(max_length=100, blank=True, null=True) # cadastre
    lieu_dit = models.CharField(max_length=100, blank=True, null=True) # lieu-dit
    altitude = models.FloatField(blank=True, null=True) # altitude
    x = models.FloatField(blank=True, null=True) # x
    y = models.FloatField(blank=True, null=True) # y
    situation_geo = models.CharField(max_length=200, blank=True, null=True) # description de la situation géographique
    denivelle = models.FloatField(blank=True, null=True) # dénivellé
    exposition = models.ForeignKey('Exposition', on_delete=models.CASCADE, blank=True, null=True) # exposition
    pente = models.FloatField(blank=True, null=True) # pente
    capacite = models.FloatField(blank=True, null=True) # capacité
    date_insert = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True) # date d'insertion
    date_update = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True) # date de mise à jour
    bat_suppr = models.BooleanField(default=False, null=True) # bâtiment supprimé
    notepatri = models.ForeignKey('Notepatri', on_delete=models.CASCADE, blank=True, null=True) # notepatri
    patrimonialite = models.CharField(max_length=500, blank=True, null=True) # patrimonialité
    info_risquenat = models.CharField(max_length=500, blank=True, null=True) # info_risquenat
    info_masque = models.CharField(max_length=500, blank=True, null=True) # info_masque
    ancien_index = models.FloatField(blank=True, null=True) # ancien_index
    remarque = models.CharField(max_length=500, blank=True, null=True) # remarque
    codeconservation = models.ForeignKey('CodeConservation', on_delete=models.CASCADE, blank=True, null=True) # codeconservation
    valide = models.BooleanField(default=False, null=True) # validé
    geom = models.PointField(blank=True, null=True) # geom

class Implantation(models.Model):
    __tablename__ = 'bib_codepem'
    codepem = models.AutoField(primary_key=True)
    pem = models.CharField(max_length=80)  

class ClasseArchitecturale(models.Model):
    __tablename__ = 'bib_classe_archi'
    codeclasse = models.AutoField(primary_key=True)
    classe = models.CharField(max_length=100)
    classe_decrite = models.CharField(max_length=300, blank=True, null=True)

class Faitage(models.Model):
    __tablename__ = 'bib_faitage'
    codefaitage = models.AutoField(primary_key=True)
    faitage = models.CharField(max_length=100)

class Commune(models.Model):
    __tablename__ = 'bib_commune'
    codeinsee = models.AutoField(primary_key=True)
    codecanton = models.ForeignKey('Canton', on_delete=models.CASCADE, blank=True, null=True) # codecanton
    codesecteur = models.ForeignKey('Secteur', on_delete=models.CASCADE, blank=True, null=True) # codesecteur
    commune = models.CharField(max_length=100)

class Canton(models.Model):
    __tablename__ = 'bib_canton'
    codecanton = models.AutoField(primary_key=True)
    canton = models.CharField(max_length=80)

class Secteur(models.Model):
    __tablename__ = 'bib_secteur'
    codesecteur = models.AutoField(primary_key=True)
    secteur = models.CharField(max_length=80)

class Exposition(models.Model):
    __tablename__ = 'bib_exposition'
    id = models.AutoField(primary_key=True)
    exposition = models.CharField(max_length=80)

class Notepatri(models.Model):
    __tablename__ = 'bib_notepatri'
    id = models.AutoField(primary_key=True)
    notepatri = models.FloatField(blank=True, null=True)

class CodeConservation(models.Model):
    __tablename__ = 'bib_codeconservation'
    id = models.AutoField(primary_key=True)
    conservation = models.CharField(max_length=80)