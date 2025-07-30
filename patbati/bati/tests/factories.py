import datetime

from django.contrib.gis.geos import Point

import factory
from .. import models


class MateriauxFinFinitionStructureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MateriauxFinFinitionStructure

    materiaux_fin = models.Nomenclature.objects.get(pk=308)  # Chanvre
    finition = models.Nomenclature.objects.get(pk=107)  # Gros


class StructureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Structure

    conservation = models.Nomenclature.objects.get(pk=58)  # Mauvais état
    materiaux_principal = models.Nomenclature.objects.get(pk=144)  # Liants
    type = models.Nomenclature.objects.get(pk=230)  # escalier
    mise_en_oeuvre = models.Nomenclature.objects.get(pk=185)  # Dallage
    info_structure = "Info"
    est_remarquable = True

    @factory.post_generation
    def finitions(obj, create, finitions):
        if finitions:
            obj.finitions.set(finitions)
            return
        MateriauxFinFinitionStructureFactory.create(structure=obj)
        MateriauxFinFinitionStructureFactory.create(structure=obj)


class MateriauxFinFinitionSecondOeuvreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MateriauxFinFinitionSecondOeuvre

    materiaux_fin = models.Nomenclature.objects.get(pk=308)  # Chanvre
    finition = models.Nomenclature.objects.get(pk=107)  # Gros


class SecondOeuvreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SecondOeuvre

    type = models.Nomenclature.objects.get(pk=462)  # 462 materiaux synthese
    conservation = models.Nomenclature.objects.get(pk=58)  # Mauvais état
    commentaire = "Commentaire"
    est_remarquable = True

    @factory.post_generation
    def materiaux_fin(obj, create, materiaux_fin):
        if materiaux_fin:
            obj.materiaux_fin.set(materiaux_fin)
            return
        MateriauxFinFinitionSecondOeuvreFactory.create(second_oeuvre=obj)
        MateriauxFinFinitionSecondOeuvreFactory.create(second_oeuvre=obj)


class TravauxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Travaux

    date = "2025-02-01"
    usage = models.Nomenclature.objects.get(pk=246)  # abri a sel
    nature = models.Nomenclature.objects.get(pk=191)  # entretien
    autorisation = True
    subvention_pne = 1000


class DemandeTravauxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DemandeTravaux

    demande_dep = True
    autorisation_p = True
    date_permis = "2025-01-01"
    date_demande_permis = "2024-12-01"
    num_permis = "12345"

    @factory.post_generation
    def travaux(obj, create, travaux):
        if travaux:
            obj.travaux.set(travaux)
            return
        TravauxFactory.create(demande=obj, date='2025-01-01')
        TravauxFactory.create(demande=obj, date="1900-01-01")


class EquipementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Equipement

    type = models.Nomenclature.objects.get(pk=261)  # Eolien
    conservation = models.Nomenclature.objects.get(pk=57)  # Bon Etat
    commentaire = "Equipement"
    est_remarquable = True

class PerspectiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Perspective

    perspective = models.Nomenclature.objects.get(pk=208)  # Réhabilitation
    date = "2025-03-01"

class ElementPaysagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ElementPaysager

    conservation = models.Nomenclature.objects.get(pk=57)  # Bon Etat
    type = models.Nomenclature.objects.get(pk=283)  # Lac
    commentaire = "Paysager"
    est_remarquable = True

class EnqueteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Enquetes

    personne = models.Nomenclature.objects.get(pk=194)  # Yves Baret
    date_enquete = datetime.datetime(2025, 4, 1)
    date_redaction = datetime.datetime(2025, 4, 2)

class BatiFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Bati

    type_bat = models.Nomenclature.objects.get(pk=610) #refuge
    classe = models.Nomenclature.objects.get(pk=32)
    implantation = models.Nomenclature.objects.get(pk=128)
    faitage = models.Nomenclature.objects.get(pk=71)
    proprietaire = "toto"
    cadastre = "1ABE"
    lieu_dit = "ici"
    altitude = 1500
    indivision = False
    situation_geo = "ici"
    bat_suppr = False
    geom=Point(1, 2)
    exposition = models.Nomenclature.objects.get(pk=77)
    notepatri = models.Nomenclature.objects.get(pk=86)
    conservation = models.Nomenclature.objects.get(pk=58)
    remarque_generale = "remarque"

    @factory.post_generation
    def masque(obj, create, masque):
        if masque:
            obj.masques.set(masque)
            return
        # foret + arbre
        obj.masques.set(
            [
                models.Nomenclature.objects.get(pk=130),
                models.Nomenclature.objects.get(pk=131),
            ]
        )

    @factory.post_generation
    def risques_nat(obj, create, risques_nat):
        if risques_nat:
            obj.risques_nat.set(risques_nat)
            return
        # avalanche + chute de pierre
        obj.risques_nat.set(
            [
                models.Nomenclature.objects.get(pk=222),
                models.Nomenclature.objects.get(pk=223),
            ]
        )

    @factory.post_generation
    def perspectives(obj, create, perspectives):
        if perspectives:
            obj.perspectives.set(perspectives)
            return
        # Restauration + Construction neuve
        obj.perspectives.set(
            [
                models.Nomenclature.objects.get(pk=210),
                models.Nomenclature.objects.get(pk=211),
            ]
        )

    @factory.post_generation
    def demandes_travaux(obj, create, demandes_travaux):
        if demandes_travaux:
            obj.demandes_travaux.set(demandes_travaux)
            return
        DemandeTravauxFactory.create(bati=obj)
        DemandeTravauxFactory.create(bati=obj)

    @factory.post_generation
    def structure(obj, create, structure):
        if structure:
            obj.structure.set(structure)
            return
        StructureFactory.create(bati=obj)
        StructureFactory.create(bati=obj)

    @factory.post_generation
    def second_oeuvre(obj, create, second_oeuvre):
        if second_oeuvre:
            obj.second_oeuvre.set(second_oeuvre)
            return
        SecondOeuvreFactory.create(bati=obj)
        SecondOeuvreFactory.create(bati=obj)

    @factory.post_generation
    def equipements(obj, create, equipements):
        if equipements:
            obj.equipements.set(equipements)
            return
        EquipementFactory.create(bati=obj)

    @factory.post_generation
    def elements_paysagers(obj, create, elements_paysagers):
        if elements_paysagers:
            obj.elements_paysagers.set(elements_paysagers)
            return
        ElementPaysagerFactory.create(bati=obj)

    @factory.post_generation
    def perspective_bati(obj, create, perspective_bati):
        if perspective_bati:
            obj.perspective_bati.set(perspective_bati)
            return
        PerspectiveFactory.create(bati=obj)

    @factory.post_generation
    def batiments_personnes_enquetes(obj, create, batiments_personnes_enquetes):
        if batiments_personnes_enquetes:
            obj.batiments_personnes_enquetes.set(batiments_personnes_enquetes)
            return
        EnqueteFactory.create(bati=obj)


