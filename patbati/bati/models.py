import django
from django.db import models
from django.contrib.gis.db import models as gis_models
from mapentity.models import MapEntityMixin
from django.contrib.auth.models import User

# Nomenclature models for ref_nomenclatures schema
class NomenclatureType(models.Model):
    id_type = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    definition = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.label

class Nomenclature(models.Model):
    id_nomenclature = models.AutoField(primary_key=True)
    id_type = models.ForeignKey(NomenclatureType, db_column='id_type', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label

# Main Bati model
class Bati(MapEntityMixin, models.Model):
    id = models.AutoField(primary_key=True) # indexBatiment
    valide = models.BooleanField(default=False, null=True) # validé

    # code_classe / classe archi
    classe = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'CL_ARCHI'},
        related_name='batiments_classe'
    )

    # codepem / Implantation 
    implantation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'IMPLA'},
        related_name='batiments_codepem'
    )
    
    # codefaitage
    faitage = models.ForeignKey(
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
    conservation = models.ForeignKey(
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

    remarque_generale = models.TextField(null=True)

    def appelation_link(self):
        return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" title="{self.appelation}">{self.appelation}</a>'

    @property
    def secteur_label(self):
        return self.secteur.label if self.secteur else "" 

class Enquetes(models.Model):
    idenquete = models.AutoField(primary_key=True)
    personne = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'id_type__code': 'PERSONNES'},
        related_name='batiments_personnes_enquetes'
    )
    bati = models.ForeignKey(
        Bati,
        db_column='id_bat',
        on_delete=models.CASCADE,
        related_name='enquetes'
    )
    date_enquete = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True)
    date_redaction = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True)

    def get_list_url(cls):
        from django.urls import reverse
        return reverse('bati:bati_list')

    def get_detail_url(self):
        # Return the detail page of the related Bati
        return self.id_bat.get_detail_url()

class DemandeTravaux(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="demandes_travaux",
    )
    demande_dep = models.BooleanField(null=False, default=False)
    autorisation_p = models.BooleanField(null=True, default=False)
    date_permis = models.DateField(null=True)
    date_demande_permis = models.DateField(null=True)
    num_permis = models.CharField()

class Travaux(models.Model):
    date = models.DateField()
    demande = models.ForeignKey(
        DemandeTravaux,
        null=False,
        related_name="travaux",
        on_delete=models.CASCADE,
    )
    usage = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'USAGE_TRAVAUX'},
        related_name="usage_travaux"
    )
    nature = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'NATURE_TRAVAUX'},
        related_name="nature_travaux"

    )
    autorisation = models.BooleanField(null=True)
    subvention_pne = models.IntegerField(null=True)

class Structure(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="structure",
    )
    conservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'CONSERVATION'},
        related_name="structure_conservation"
    )
    materiaux_principal = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'MAT_GE'},
        related_name="structure_mat_princip",
        verbose_name="Materiau principal"

    )
    type = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'STRUCT'},
        related_name="structure_struct",
        verbose_name="Type de structure"
    )
    mise_en_oeuvre = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'MEOEUVRE'},
        related_name="structure_me",
        verbose_name="Mise en oeuvre"
    )
    info_structure = models.TextField(null=True)
    est_remarquable = models.BooleanField(null=False, default=False, verbose_name="Structure remarquable")

    

class SecondOeuvre(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="second_oeuvre",
    )
    type = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'TYPE_SO'},
        related_name="structure_second_oeuvre",
        verbose_name="Type de second oeuvre"
    )
    conservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'CONSERVATION'},
        related_name="second_oeuvre_conservation"
    )
    commentaire = models.TextField(null=True, verbose_name="Commentaire")
    est_remarquable = models.BooleanField(null=False, default=False, verbose_name="Remarquable")


class Equipement(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="equipements",
    )
    type = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'TYPE_EQUIP'},
        related_name="equipement_type",
        verbose_name="Type d'équipement"
    )
    conservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'CONSERVATION'},
        related_name="equipement_conservation"
    )
    commentaire = models.TextField(null=True, verbose_name="Commentaire")
    est_remarquable = models.BooleanField(null=False, default=False, verbose_name="Remarquable")

class ElementPaysager(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="elements_paysagers",
    )
    conservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={'id_type__code': 'CONSERVATION'},
        related_name="elem_paysager_conservation"
    )
    commentaire = models.TextField(null=True, verbose_name="Commentaire")
    est_remarquable = models.BooleanField(null=False, default=False, verbose_name="Remarquable")

class Illustrations(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="illustrations",
    )
    type_illustration = models.ForeignKey(
        "Nomenclature",
        on_delete=models.PROTECT,
        null=True,
        limit_choices_to={'id_type__code': 'TYPE_ILLUSTRATION'},
        related_name="illustration_type",
    )
    auteur = models.ForeignKey (
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="ilustration_auteur"
    ) 
    fichier_src = models.ImageField(null=False, verbose_name="fichier source")
    date = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    indexjaris = models.IntegerField(null=True, verbose_name="index photothèque")

class DocumentAttache(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="documents_attaches",
    )
    fichier_src = models.FileField(null=False, verbose_name="document")
    date = models.DateField(default=django.utils.timezone.now, blank=True, null=True)