from collections import defaultdict
import django
from django.db import models
from django.contrib.gis.db import models as gis_models
from mapentity.models import MapEntityMixin, BaseMapEntityMixin
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
    id_type = models.ForeignKey(
        NomenclatureType, db_column="id_type", on_delete=models.CASCADE
    )
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    parentId = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.label


# Main Bati model
class Bati(MapEntityMixin, models.Model):
    id = models.AutoField(primary_key=True)  # indexBatiment
    valide = models.BooleanField(
        default=False, null=True, verbose_name="Validé"
    )  # validé

    # code_classe / classe archi
    classe = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        null=False,
        limit_choices_to={"id_type__code": "CL_ARCHI"},
        related_name="batiments_classe",
    )

    # codepem / Implantation
    # TODO : a enlever l'implantion doit être danns ref_geo
    implantation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={"id_type__code": "IMPLA"},
        related_name="batiments_implantation",
    )

    # codefaitage
    faitage = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={"id_type__code": "FAITAGE"},
        related_name="batiments_faitage",
    )

    # @TODO : Commune --> ref Geo

    appelation = models.CharField(max_length=200, blank=True, null=True)  # appellation
    indivision = models.BooleanField(default=False, null=True)  # indivision
    proprietaire = models.CharField(
        max_length=100, blank=True, null=True
    )  # propriétaire
    cadastre = models.CharField(max_length=100, blank=True, null=True)  # cadastre
    lieu_dit = models.CharField(max_length=100, blank=True, null=True)  # lieu-dit
    altitude = models.FloatField(blank=True, null=True)  # altitude
    x = models.FloatField(blank=True, null=True)  # x
    y = models.FloatField(blank=True, null=True)  # y
    situation_geo = models.CharField(
        max_length=200, blank=True, null=True
    )  # description de la situation géographique
    denivelle = models.FloatField(blank=True, null=True)  # dénivellé

    # secteur
    secteur = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={"id_type__code": "SECTEUR"},
        related_name="batiments_secteur",
    )

    # protection = zone coeur
    # TODO a connecter au ref_geo
    protection = models.ManyToManyField(
        Nomenclature,
        limit_choices_to={"id_type__code": "PROT"},
        related_name="batiments_protection",
    )

    # exposition
    exposition = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={"id_type__code": "EXPO"},
        related_name="batiments_exposition",
    )

    pente = models.FloatField(blank=True, null=True)  # pente
    capacite = models.FloatField(blank=True, null=True)  # capacité
    date_insert = models.DateTimeField(
        default=django.utils.timezone.now, blank=True, null=True
    )  # date d'insertion
    date_update = models.DateTimeField(
        default=django.utils.timezone.now, blank=True, null=True
    )  # date de mise à jour
    bat_suppr = models.BooleanField(default=False, null=True)  # bâtiment supprimé

    # notepatri
    notepatri = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={"id_type__code": "NOTE_PAT"},
        related_name="batiments_notepatri",
    )

    patrimonialite = models.CharField(
        max_length=500, blank=True, null=True
    )  # patrimonialité
    ancien_index = models.FloatField(blank=True, null=True)  # ancien_index

    # codeconservation
    conservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={"id_type__code": "CONSERVATION"},
        related_name="batiments_conservation",
    )

    # masques
    masques = models.ManyToManyField(
        Nomenclature,
        limit_choices_to={"id_type__code": "MASQUE"},
        related_name="batiments_info_masque",
    )

    commentaire_masque = models.CharField(
        max_length=500, blank=True, null=True
    )  # info_masque

    # risquenat
    risques_nat = models.ManyToManyField(
        Nomenclature,
        limit_choices_to={"id_type__code": "RISQUE"},
        blank=True,
        related_name="batiments_risquenat",
    )

    remarque_risque = models.CharField(
        max_length=500, blank=True, null=True
    )  # remarque
    geom = gis_models.PointField(blank=True, null=True)  # geom

    remarque_generale = models.TextField(null=True, blank=True)

    perspectives = models.ManyToManyField(Nomenclature, through="Perspective")

    def appelation_link(self):
        return f'<a data-pk="{self.pk}" href="{self.get_detail_url()}" title="{self.appelation}">{self.appelation}</a>'

    @property
    def secteur_label(self):
        return self.secteur.label if self.secteur else ""

    @property
    def dernier_travaux(self):
        from patbati.bati.models import Travaux

        return (
            Travaux.objects.filter(demande__bati=self)
            .order_by('-date')
            .first()
        )

    @property
    def get_structures_with_materials(self):
        structures_with_materials = defaultdict(list)

        for struct in self.structure.all():
            structures_with_materials[struct.type.label].append(struct.materiaux_principal.label)

            for mat_fin in struct.materiaux_fin.all():
                structures_with_materials[struct.type.label].append(mat_fin.label)

        structures_with_materials = {
            struct_type: ', '.join(sorted(set(materials), key=materials.index))
            for struct_type, materials in structures_with_materials.items()
        }

        return structures_with_materials

    def get_detail_url(self):
        from django.urls import reverse

        return reverse("bati:bati_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.appelation if self.appelation else f"Bâtiment {self.id}"


class Enquetes(models.Model):
    idenquete = models.AutoField(primary_key=True)
    personne = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={"id_type__code": "PERSONNES"},
        related_name="batiments_personnes_enquetes",
    )
    bati = models.ForeignKey(
        Bati, db_column="bati", on_delete=models.CASCADE, related_name="enquetes"
    )
    date_enquete = models.DateTimeField(
        default=django.utils.timezone.now, blank=True, null=True
    )
    date_redaction = models.DateTimeField(
        default=django.utils.timezone.now, blank=True, null=True
    )

    def get_list_url(cls):
        from django.urls import reverse

        return reverse("bati:bati_list")

    def get_detail_url(self):
        return self.bati.get_detail_url()

    def __str__(self):
        return (
            f"Enquête {self.idenquete} de "
            f"{self.personne.label if self.personne else 'Inconnu'} "
            f"du {self.date_enquete.strftime('%Y-%m-%d') if self.date_enquete else 'Date inconnue'} "
            f"pour {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"
        )


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

    def __str__(self):
        return f"Demande de travaux du {self.date_demande_permis} pour {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"


class Travaux(models.Model):
    date = models.DateField(
        null=False,
        db_comment="Ce champs est non null depuis la v2, remplie avec 1800-01-01 quand l'info était absente",
    )
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
        limit_choices_to={"id_type__code": "USAGE_TRAVAUX"},
        related_name="usage_travaux",
    )
    nature = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "NATURE_TRAVAUX"},
        related_name="nature_travaux",
    )
    autorisation = models.BooleanField(null=True)
    subvention_pne = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Travaux du {self.date} pour {self.demande.bati.appelation if self.demande.bati else 'Bâtiment inconnu'}"


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
        limit_choices_to={"id_type__code": "CONSERVATION"},
        related_name="structure_conservation",
    )
    materiaux_principal = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "MAT_GE"},
        related_name="structure_mat_princip",
        verbose_name="Materiau principal",
    )
    type = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "STRUCT"},
        related_name="structure_struct",
        verbose_name="Type de structure",
    )
    mise_en_oeuvre = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "MEOEUVRE"},
        related_name="structure_me",
        verbose_name="Mise en oeuvre",
    )
    info_structure = models.TextField(null=True)
    est_remarquable = models.BooleanField(
        null=False, default=False, verbose_name="Structure remarquable"
    )

    materiaux_fin = models.ManyToManyField(
        Nomenclature,
        through="MateriauxFinFinitionStructure",
        through_fields=["structure", "materiaux_fin"],
    )

    def get_detail_url(self):
        return self.bati.get_detail_url()

    def __str__(self):
        return (
            f"Structure de {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"
        )


class MateriauxFinFinitionStructure(models.Model):
    structure = models.ForeignKey(
        "Structure",
        on_delete=models.CASCADE,
        null=False,
        related_name="finitions",
    )
    materiaux_fin = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "MAT_FIN"},
        related_name="materiaux_fin_rel",
        verbose_name="Materiaux fin",   
    )
    finition = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "FIN"},
        related_name="finition_mat_fin_rel",
        verbose_name="Finition",
    )

    def __str__(self):
        return f"Finition de structure pour {self.structure.bati.appelation if self.structure.bati else 'Bâtiment inconnu'}"

    def get_detail_url(self):
        return self.structure.get_detail_url()


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
        limit_choices_to={"id_type__code": "SO"},
        related_name="structure_second_oeuvre",
        verbose_name="Type de second oeuvre",
    )
    conservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Etat de conservation",
        limit_choices_to={'id_type__code': 'CONSERVATION'},
        related_name="second_oeuvre_conservation"
    )
    commentaire = models.TextField(null=True, verbose_name="Commentaire")
    est_remarquable = models.BooleanField(
        null=False, default=False, verbose_name="Remarquable"
    )
    materiaux_fin = models.ManyToManyField(
        Nomenclature,
        through="MateriauxFinFinitionSecondOeuvre",
        through_fields=["second_oeuvre", "materiaux_fin"],
    )

    def get_detail_url(self):
        return self.bati.get_detail_url()

    def __str__(self):
        return (
            f"Structure de {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"
        )


class MateriauxFinFinitionSecondOeuvre(models.Model):
    second_oeuvre = models.ForeignKey(
        "SecondOeuvre",
        on_delete=models.CASCADE,
        null=False,
        related_name="second_oeuvre",
    )
    materiaux_fin = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "MAT_FIN"},
        related_name="materiaux_fin_rel_sec",
        verbose_name="Materiaux fins",
    )
    finition = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "FIN"},
        related_name="finition_mat_fin_rel_soc",
        verbose_name="Finition",
    )

    def get_detail_url(self):
        return self.second_oeuvre.get_detail_url()

    def __str__(self):
        return f"Finition de second oeuvre pour {self.second_oeuvre.bati.appelation if self.second_oeuvre.bati else 'Bâtiment inconnu'}"


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
        limit_choices_to={"id_type__code": "EQUIP"},
        related_name="equipement_type",
        verbose_name="Type d'équipement",
    )
    conservation = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "CONSERVATION"},
        related_name="equipement_conservation",
    )
    commentaire = models.TextField(null=True, verbose_name="Commentaire")
    est_remarquable = models.BooleanField(
        null=False, default=False, verbose_name="Remarquable"
    )

    def __str__(self):
        return (
            f"Equipement de {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"
        )


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
        limit_choices_to={"id_type__code": "CONSERVATION"},
        related_name="elem_paysager_conservation",
    )
    type = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "ELEM_PAYS"},
        related_name="elem_paysager_type",
    )
    commentaire = models.TextField(null=True, verbose_name="Commentaire")
    est_remarquable = models.BooleanField(
        null=False, default=False, verbose_name="Remarquable"
    )

    def __str__(self):
        return f"Élément paysager de {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"


class AuteurPhoto(models.Model):
    nom = models.CharField(100)
    prenom = models.CharField(100)
    descriptif = models.TextField(100)


# TODO aggreger AuteurPhoto + User pour la liste des auteur des illustrations


class Illustration(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="illustrations",
    )
    type = models.ForeignKey(
        "Nomenclature",
        on_delete=models.PROTECT,
        null=True,
        limit_choices_to={"id_type__code": "TYPE_ILLUSTRATION"},
        related_name="illustration_type",
    )
    auteur = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="ilustration_auteur"
    )
    fichier_src = models.ImageField(null=False, verbose_name="fichier source")
    date = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    indexajaris = models.IntegerField(null=True, verbose_name="index photothèque")

    def __str__(self):
        return f"Illustration {self.id} pour {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"


class DocumentAttache(models.Model):
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
        null=False,
        related_name="documents_attaches",
    )
    fichier_src = models.FileField(null=False, verbose_name="document")
    date = models.DateField(default=django.utils.timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Document attaché {self.id} pour {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"


class Perspective(models.Model):
    """_summary_

    Perspectives associé à un batiment (rénovation, entretien)
    Dans la v2 on ajoute une date à chaque "perspective"
    """

    perspective = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={"id_type__code": "PERSP"},
        related_name="perspective_bati",
    )
    date = models.DateField(null=True)
    bati = models.ForeignKey(
        "Bati",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Perspective {self.perspective.label if self.perspective else 'Inconnue'} pour {self.bati.appelation if self.bati else 'Bâtiment inconnu'}"


class MateriauxFinFinition(models.Model):
    """_summary_

    rel_matfins_finition
    """

    materiaux_fin = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "MAT_FIN"},
        related_name="materiaux_fin_finition",
    )
    finition = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "FIN"},
        related_name="finition_materiaux_fin",
    )


class MateriauGeMiseEnOeuvre(models.Model):
    """_summary_

    rel_matge_meo
    """

    materiaux_ge = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "MAT_GE"},
        related_name="materiaux_ge_mise_en_oeuvre",
    )
    mise_en_oeuvre = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        limit_choices_to={"id_type__code": "MEOEUVRE"},
        related_name="mise_en_oeuvre_materiaux_ge",
    )
