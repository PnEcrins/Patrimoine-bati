import datetime
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

class BatiModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create all needed NomenclatureTypes
        types = {}
        for code in [
            "TYPE_BAT", "CL_ARCHI", "IMPLA", "FAITAGE", "EXPO", "NOTE_PAT",
            "CONSERVATION", "STRUCT", "MAT_GE", "MEOEUVRE", "MASQUE", "RISQUE",
            "PERSONNES", "USAGE_TRAVAUX", "NATURE_TRAVAUX", "MAT_FIN", "FIN",
            "SO", "EQUIP", "ELEM_PAYS", "PERSP"
        ]:
            types[code], _ = NomenclatureType.objects.get_or_create(label=code, code=code)

        # Create Nomenclatures for each type
        noms = {}
        for code, typ in types.items():
            noms[code] = Nomenclature.objects.create(id_type=typ, label=f"{code}_label")

        # Create Bati objects with all fields filled
        cls.bati1 = Bati.objects.create(
            appelation="Bâtiment A",
            type_bat=noms["TYPE_BAT"],
            classe=noms["CL_ARCHI"],
            implantation=noms["IMPLA"],
            faitage=noms["FAITAGE"],
            indivision=True,
            proprietaire="Alice",
            cadastre="CadA",
            lieu_dit="LieuA",
            altitude=123.4,
            x=1.1,
            y=2.2,
            situation_geo="SituA",
            denivelle=10.5,
            exposition=noms["EXPO"],
            pente=15.0,
            capacite=100.0,
            bat_suppr=False,
            notepatri=noms["NOTE_PAT"],
            patrimonialite="PatriA",
            ancien_index=1.23,
            conservation=noms["CONSERVATION"],
            commentaire_masque="MasqueA",
            remarque_risque="RisqueA",
            geom=Point(1, 2),
            remarque_generale="RemarqueA",
        )
        cls.bati2 = Bati.objects.create(
            appelation="Bâtiment B",
            type_bat=noms["TYPE_BAT"],
            classe=noms["CL_ARCHI"],
            implantation=noms["IMPLA"],
            faitage=noms["FAITAGE"],
            indivision=False,
            proprietaire="Bob",
            cadastre="CadB",
            lieu_dit="LieuB",
            altitude=234.5,
            x=3.3,
            y=4.4,
            situation_geo="SituB",
            denivelle=20.5,
            exposition=noms["EXPO"],
            pente=25.0,
            capacite=200.0,
            bat_suppr=True,
            notepatri=noms["NOTE_PAT"],
            patrimonialite="PatriB",
            ancien_index=2.34,
            conservation=noms["CONSERVATION"],
            commentaire_masque="MasqueB",
            remarque_risque="RisqueB",
            geom=Point(3, 4),
            remarque_generale="RemarqueB",
        )
        cls.bati3 = Bati.objects.create(
            appelation="Bâtiment C",
            type_bat=noms["TYPE_BAT"],
            classe=noms["CL_ARCHI"],
            implantation=noms["IMPLA"],
            faitage=noms["FAITAGE"],
            indivision=True,
            proprietaire="Charlie",
            cadastre="CadC",
            lieu_dit="LieuC",
            altitude=345.6,
            x=5.5,
            y=6.6,
            situation_geo="SituC",
            denivelle=30.5,
            exposition=noms["EXPO"],
            pente=35.0,
            capacite=300.0,
            bat_suppr=False,
            notepatri=noms["NOTE_PAT"],
            patrimonialite="PatriC",
            ancien_index=3.45,
            conservation=noms["CONSERVATION"],
            commentaire_masque="MasqueC",
            remarque_risque="RisqueC",
            geom=Point(5, 6),
            remarque_generale="RemarqueC",
        )

        # Add ManyToMany fields
        cls.bati1.masques.add(noms["MASQUE"])
        cls.bati2.masques.add(noms["MASQUE"])
        cls.bati3.masques.add(noms["MASQUE"])
        cls.bati1.risques_nat.add(noms["RISQUE"])
        cls.bati2.risques_nat.add(noms["RISQUE"])
        cls.bati3.risques_nat.add(noms["RISQUE"])

        # Create related models for __str__ and property tests
        cls.demande = DemandeTravaux.objects.create(
            bati=cls.bati1,
            demande_dep=True,
            autorisation_p=True,
            date_permis="2025-01-01",
            date_demande_permis="2024-12-01",
            num_permis="12345"
        )
        cls.travaux = Travaux.objects.create(
            date="2025-02-01",
            demande=cls.demande,
            usage=noms["USAGE_TRAVAUX"],
            nature=noms["NATURE_TRAVAUX"],
            autorisation=True,
            subvention_pne=1000
        )
        cls.structure = Structure.objects.create(
            bati=cls.bati1,
            conservation=noms["CONSERVATION"],
            materiaux_principal=noms["MAT_GE"],
            type=noms["STRUCT"],
            mise_en_oeuvre=noms["MEOEUVRE"],
            info_structure="Info",
            est_remarquable=True
        )
        cls.mff_structure = MateriauxFinFinitionStructure.objects.create(
            structure=cls.structure,
            materiaux_fin=noms["MAT_FIN"],
            finition=noms["FIN"]
        )
        cls.second_oeuvre = SecondOeuvre.objects.create(
            bati=cls.bati1,
            type=noms["SO"],
            conservation=noms["CONSERVATION"],
            commentaire="Commentaire",
            est_remarquable=True
        )
        cls.mff_second_oeuvre = MateriauxFinFinitionSecondOeuvre.objects.create(
            second_oeuvre=cls.second_oeuvre,
            materiaux_fin=noms["MAT_FIN"],
            finition=noms["FIN"]
        )
        cls.equipement = Equipement.objects.create(
            bati=cls.bati1,
            type=noms["EQUIP"],
            conservation=noms["CONSERVATION"],
            commentaire="Equipement",
            est_remarquable=True
        )
        cls.element_paysager = ElementPaysager.objects.create(
            bati=cls.bati1,
            conservation=noms["CONSERVATION"],
            type=noms["ELEM_PAYS"],
            commentaire="Paysager",
            est_remarquable=True
        )
        cls.perspective = Perspective.objects.create(
            perspective=noms["PERSP"],
            date="2025-03-01",
            bati=cls.bati1
        )
        cls.enquete = Enquetes.objects.create(
            personne=noms["PERSONNES"],
            bati=cls.bati1,
            date_enquete=datetime.datetime(2025, 4, 1),
            date_redaction=datetime.datetime(2025, 4, 2)
        )

    def test_bati_count(self):
        self.assertEqual(Bati.objects.count(), 3)

    def test_bati1_fields(self):
        b = Bati.objects.get(appelation="Bâtiment A")
        self.assertEqual(b.proprietaire, "Alice")
        self.assertEqual(b.cadastre, "CadA")
        self.assertEqual(b.lieu_dit, "LieuA")
        self.assertEqual(b.altitude, 123.4)
        self.assertEqual(b.x, 1.1)
        self.assertEqual(b.y, 2.2)
        self.assertEqual(b.situation_geo, "SituA")
        self.assertEqual(b.denivelle, 10.5)
        self.assertEqual(b.pente, 15.0)
        self.assertEqual(b.capacite, 100.0)
        self.assertFalse(b.bat_suppr)
        self.assertEqual(b.patrimonialite, "PatriA")
        self.assertEqual(b.ancien_index, 1.23)
        self.assertEqual(b.commentaire_masque, "MasqueA")
        self.assertEqual(b.remarque_risque, "RisqueA")
        self.assertEqual(b.remarque_generale, "RemarqueA")
        self.assertEqual(b.geom.wkt, "POINT (1 2)")
        self.assertEqual(b.masques.count(), 1)
        self.assertEqual(b.risques_nat.count(), 1)

    def test_bati2_fields(self):
        b = Bati.objects.get(appelation="Bâtiment B")
        self.assertEqual(b.proprietaire, "Bob")
        self.assertEqual(b.cadastre, "CadB")
        self.assertEqual(b.lieu_dit, "LieuB")
        self.assertEqual(b.altitude, 234.5)
        self.assertEqual(b.x, 3.3)
        self.assertEqual(b.y, 4.4)
        self.assertEqual(b.situation_geo, "SituB")
        self.assertEqual(b.denivelle, 20.5)
        self.assertEqual(b.pente, 25.0)
        self.assertEqual(b.capacite, 200.0)
        self.assertTrue(b.bat_suppr)
        self.assertEqual(b.patrimonialite, "PatriB")
        self.assertEqual(b.ancien_index, 2.34)
        self.assertEqual(b.commentaire_masque, "MasqueB")
        self.assertEqual(b.remarque_risque, "RisqueB")
        self.assertEqual(b.remarque_generale, "RemarqueB")
        self.assertEqual(b.geom.wkt, "POINT (3 4)")
        self.assertEqual(b.masques.count(), 1)
        self.assertEqual(b.risques_nat.count(), 1)

    def test_bati3_fields(self):
        b = Bati.objects.get(appelation="Bâtiment C")
        self.assertEqual(b.proprietaire, "Charlie")
        self.assertEqual(b.cadastre, "CadC")
        self.assertEqual(b.lieu_dit, "LieuC")
        self.assertEqual(b.altitude, 345.6)
        self.assertEqual(b.x, 5.5)
        self.assertEqual(b.y, 6.6)
        self.assertEqual(b.situation_geo, "SituC")
        self.assertEqual(b.denivelle, 30.5)
        self.assertEqual(b.pente, 35.0)
        self.assertEqual(b.capacite, 300.0)
        self.assertFalse(b.bat_suppr)
        self.assertEqual(b.patrimonialite, "PatriC")
        self.assertEqual(b.ancien_index, 3.45)
        self.assertEqual(b.commentaire_masque, "MasqueC")
        self.assertEqual(b.remarque_risque, "RisqueC")
        self.assertEqual(b.remarque_generale, "RemarqueC")
        self.assertEqual(b.geom.wkt, "POINT (5 6)")
        self.assertEqual(b.masques.count(), 1)
        self.assertEqual(b.risques_nat.count(), 1)

    # __str__ methods
    def test_bati_str(self):
        b = Bati.objects.get(appelation="Bâtiment A")
        self.assertEqual(str(b), "Bâtiment A")

    def test_nomenclaturetype_str(self):
        ntype = NomenclatureType.objects.first()
        self.assertEqual(str(ntype), ntype.label)

    def test_nomenclature_str(self):
        nom = Nomenclature.objects.first()
        self.assertEqual(str(nom), nom.label)

    # enquetes
    def test_enquetes_str(self):
        self.assertIn("Enquête", str(self.enquete))

    def test_enquetes_get_list_url(self):
        url = Enquetes.get_list_url(Enquetes)
        self.assertEqual(url, reverse("bati:bati_list"))

    def test_enquetes_get_detail_url(self):
        enquete = self.enquete
        self.assertEqual(enquete.get_detail_url(), enquete.bati.get_detail_url())

    def test_demande_travaux_str(self):
        self.assertIn("Demande de travaux", str(self.demande))

    def test_travaux_str(self):
        self.assertIn("Travaux du", str(self.travaux))

    def test_structure_str(self):
        self.assertIn("Structure de", str(self.structure))

    def test_mff_structure_str(self):
        self.assertIn("Finition de structure", str(self.mff_structure))

    def test_mff_structure_get_detail_url(self):
        mff = self.mff_structure
        self.assertEqual(mff.get_detail_url(), mff.structure.get_detail_url())

    def test_second_oeuvre_str(self):
        self.assertIn("Structure de", str(self.second_oeuvre))

    def test_mff_second_oeuvre_str(self):
        self.assertIn("Finition de second oeuvre", str(self.mff_second_oeuvre))

    def test_mff_second_oeuvre_get_detail_url(self):
        mff_so = self.mff_second_oeuvre
        self.assertEqual(mff_so.get_detail_url(), mff_so.second_oeuvre.get_detail_url())

    def test_equipement_str(self):
        self.assertIn("Equipement de", str(self.equipement))

    def test_element_paysager_str(self):
        self.assertIn("Élément paysager de", str(self.element_paysager))

    def test_perspective_str(self):
        self.assertIn("Perspective", str(self.perspective))

    def test_bati_type_bat_label_property(self):
        b = self.bati1
        self.assertEqual(b.type_bat_label, "TYPE_BAT_label")

    def test_bati_secteurs_verbose_name_classproperty(self):
        self.assertEqual(Bati.secteurs_verbose_name, "Secteur")

    def test_bati_dernier_travaux_property(self):
        b = self.bati1
        self.assertEqual(b.dernier_travaux, self.travaux)

    def test_bati_get_structures_with_materials_property(self):
        b = self.bati1
        self.assertIn("STRUCT_label", b.get_structures_with_materials)
        self.assertIn("MAT_GE_label", b.get_structures_with_materials["STRUCT_label"])

    def test_bati_appelation_link(self):
        b = self.bati1
        self.assertIn("href", b.appelation_link())
        self.assertIn(b.appelation, b.appelation_link())