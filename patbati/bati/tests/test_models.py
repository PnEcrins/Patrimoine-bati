import datetime

from itertools import pairwise
from django.test import TestCase
from django.contrib.gis.geos import Point
from django.urls import reverse
from patbati.bati.models import (
    Bati, Nomenclature, NomenclatureType,
    Enquetes, DemandeTravaux, Travaux, Structure,
    MateriauxFinFinitionStructure, SecondOeuvre,
    MateriauxFinFinitionSecondOeuvre, Equipement,
    ElementPaysager, Perspective
)
from . import factories

class BatiModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bati1 = factories.BatiFactory.create(
            appelation="Bâtiment A",
        )
        cls.bati2 = factories.BatiFactory.create(
            appelation="Bâtiment B",

        )
        cls.bati3 = factories.BatiFactory.create(
            appelation="Bâtiment C",
            # masque=[models.Nomenclature.objects.get(pk=130), models.Nomenclature.objects.get(pk=131)]
        )
        cls.enquete = factories.EnqueteFactory(bati=cls.bati1)

    def test_bati_count(self):
        self.assertEqual(Bati.objects.count(), 3)


    # __str__ methods

    def test_bati_str(self):
        a = Bati.objects.get(appelation="Bâtiment A")
        self.assertEqual(str(a), "Bâtiment A")

    # enquetes
    def test_enquetes_str(self):
        self.assertIn("Enquête", str(self.enquete))

    def test_enquetes_get_list_url(self):
        self.assertEqual(self.enquete.get_list_url(), reverse("bati:bati_list"))

    def test_enquetes_get_detail_url(self):
        enquete = self.enquete
        self.assertEqual(enquete.get_detail_url(), enquete.bati.get_detail_url())

    def test_demande_travaux_str(self):
        demande = self.bati1.demandes_travaux.first()
        self.assertIn("Demande de travaux", str(demande))

    def test_travaux_str(self):
        demande = self.bati1.demandes_travaux.first()
        self.assertIn("Travaux du", str(demande.travaux.first()))

    def test_structure_str(self):
        self.assertEqual(f"Structure de {self.bati1.appelation}", str(self.bati1.structure.first()))

    def test_mff_structure_str(self):
        structure = self.bati1.structure.first()
        self.assertEqual(f"Finition de structure pour {self.bati1.appelation}", str(structure.finitions.first()))

    def test_mff_structure_get_detail_url(self):
        structure = self.bati1.structure.first()
        finition = structure.finitions.first()
        self.assertEqual(finition.get_detail_url(), structure.get_detail_url())

    def test_second_oeuvre_str(self):

        self.assertEqual(f"Structure de {self.bati1.appelation}", str(self.bati1.second_oeuvre.first()))

    def test_mff_second_oeuvre_str(self):
        # TODO fix it
        pass
        # MYSTERE ??
        #second_oeuvre = self.bati1.second_oeuvre.first()

        # self.assertIn("Finition de second oeuvre", str(second_oeuvre.materiaux_fin.first()))

    # def test_mff_second_oeuvre_get_detail_url(self):
    #     mff_so = self.mff_second_oeuvre
    #     self.assertEqual(mff_so.get_detail_url(), mff_so.second_oeuvre.get_detail_url())

    def test_equipement_str(self):
        self.assertEqual(f"Equipement de {self.bati1.appelation}", str(self.bati1.equipements.first()))

    def test_element_paysager_str(self):
        self.assertEqual(f"Élément paysager de {self.bati1.appelation}", str(self.bati1.elements_paysagers.first()))

    def test_perspective_str(self):
        persp = factories.PerspectiveFactory(bati=self.bati1)
        self.assertIn("Perspective", str(persp))

    def test_bati_type_bat_label_property(self):
        self.assertEqual(self.bati1.type_bat_label, "refuge")

    def test_bati_dernier_travaux_property(self):
        dernier_travaux = self.bati1.dernier_travaux.date
        self.assertEqual(dernier_travaux, datetime.date(2025, 1, 1))

    def test_bati_get_structures_with_materials_property(self):
        b = self.bati1
        self.assertIn("Escalier", b.get_structures_with_materials.keys())
        self.assertIn("Liants", b.get_structures_with_materials["Escalier"])

    def test_bati_appelation_link(self):
        b = self.bati1
        self.assertIn("href", b.appelation_link())
        self.assertIn(b.appelation, b.appelation_link())

    def test_bati_order_demande_travaux(self):
        bati = Bati.objects.first()
        demandes = bati.demandes_travaux.all()
        date_list = map(lambda dem: dem.date_demande_permis, demandes)
        self.assertTrue(all(dem1 >= dem2 for dem1, dem2 in pairwise(date_list)))

        for dem in demandes:
            travaux = dem.travaux.all()
            date_list = map(lambda tra: tra.date, travaux)
            self.assertTrue(all(trav1 >= trav2 for trav1, trav2 in pairwise(date_list)))


class NomenclatureModelTest(TestCase):
    # test __str__
    def test_nomenclaturetype_str(self):
        ntype = NomenclatureType.objects.first()
        self.assertEqual(str(ntype), ntype.label)

    def test_nomenclature_str(self):
        nom = Nomenclature.objects.first()
        self.assertEqual(str(nom), nom.label)