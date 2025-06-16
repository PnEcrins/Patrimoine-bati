import django
from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models
from mapentity.models import MapEntityMixin

# Nomenclature models for ref_nomenclatures schema
class NomenclatureType(models.Model):
    id_type = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    definition = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'ref_nomenclatures"."bib_nomenclatures_types'
        managed = False

    def __str__(self):
        return self.label

class Nomenclature(models.Model):
    id_nomenclature = models.AutoField(primary_key=True)
    id_type = models.ForeignKey(NomenclatureType, db_column='id_type', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'ref_nomenclatures"."t_nomenclatures'
        managed = False

    def __str__(self):
        return self.label

# Main Bati model
class Bati(MapEntityMixin, models.Model):
    id = models.AutoField(primary_key=True) # indexBatiment
    valide = models.BooleanField(default=False, null=True) # validé

    # code_classe / classe archi
    code_classe = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'CL_ARCHI'},
        related_name='batiments_classe'
    )

    # codepem / Implantation 
    codepem = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'IMPLA'},
        related_name='batiments_codepem'
    )
    
    # codefaitage
    codefaitage = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'FAITAGE'},
        related_name='batiments_faitage'
    )

    #@TODO : Commune --> ref Geo

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

    # secteur
    secteur = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'SECTEUR'},
        related_name='batiments_secteur'
    )

    # protection
    protection = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'PROT'},
        related_name='batiments_protection'
    )
    
    # exposition
    exposition = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'EXPO'},
        related_name='batiments_exposition'
    ) 
    
    pente = models.FloatField(blank=True, null=True) # pente
    capacite = models.FloatField(blank=True, null=True) # capacité
    date_insert = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True) # date d'insertion
    date_update = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True) # date de mise à jour
    bat_suppr = models.BooleanField(default=False, null=True) # bâtiment supprimé

    # notepatri 
    notepatri = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'NOTE_PAT'},
        related_name='batiments_notepatri'
    )
    
    patrimonialite = models.CharField(max_length=500, blank=True, null=True) # patrimonialité
    ancien_index = models.FloatField(blank=True, null=True) # ancien_index

    # codeconservation
    codeconservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'CONSERVATION'},
        related_name='batiments_conservation'
    ) 

    # masques
    masques = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'MASQUE'},
        related_name='batiments_info_masque'
    )

    commentaire_masque = models.CharField(max_length=500, blank=True, null=True) # info_masque

    # risquenat
    risquenat = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'RISQUE'},
        related_name='batiments_risquenat'
    )

    remarque_risque = models.CharField(max_length=500, blank=True, null=True) # remarque
    geom = gis_models.PointField(blank=True, null=True) # geom

    def appelation_link(self):
        return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" title="{self.appelation}">{self.appelation}</a>'

    @property
    def secteur_label(self):
        return self.secteur.label if self.secteur else ""