from django.test import TestCase
from bs4 import BeautifulSoup
import datetime

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from patbati.bati.models import (
    Bati, Nomenclature, NomenclatureType,
)


class BatiDetailAttributesHTMLTest(TestCase):

    with open("patbati/bati/templates/bati/bati_detail_attributes.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    def test_renseignements_card_exists(self):
        card = self.soup.find("div", {"id": "collapseRenseignements"})
        self.assertIsNotNone(card)

    def test_geo_card_exists(self):
        card = self.soup.find("div", {"id": "collapseGeo"})
        self.assertIsNotNone(card)

    def test_situation_card_exists(self):
        card = self.soup.find("div", {"id": "collapseSituation"})
        self.assertIsNotNone(card)

    def test_naturel_card_exists(self):
        card = self.soup.find("div", {"id": "collapseNaturel"})
        self.assertIsNotNone(card)

    def test_equipements_card_exists(self):
        card = self.soup.find("div", {"id": "collapseEquipements"})
        self.assertIsNotNone(card)

    def test_elements_paysager_card_exists(self):
        card = self.soup.find("div", {"id": "collapseElementsPaysager"})
        self.assertIsNotNone(card)

    def test_all_table_headers_present(self):
        headers = [th.text.strip() for th in self.soup.find_all("th")]
        expected_headers = [
            "Nom",
            "Nouveau numéro",
            "Ancien numéro",
            "Valeur patrimoniale",
            "Patrimonialité",
            "Classe d'architecture",
            "Propriétaire",
            "Bâtiment en indivision",
            "Type de batiment",
            "Règlementation",
            "Capacité",
            "Date d'insertion",
            "Date de mise à jour",
            "Bâtiment supprimé",
            "Etat général",
            "Secteur",
            "Lieu-dit",
            "Cadastre",
            "Coordonnée X",
            "Coordonnée Y",
            "Altitude",
            "Dénivelé",
            "Implantation",
            "Faitage",
            "Situation géographique",
            "Exposition",
            "Pente",
            "Risques naturels",
            "Remarque risque naturel",
            "Masques",
            "Commentaire Masque",
            "Remarque générale",
            "Type",
            "Conservation",
            "Commentaire",
            "Est remarquable",
        ]
        for header in expected_headers:
            self.assertIn(header, headers, f"Header '{header}' not found in HTML")

    def test_all_collapsible_cards_present(self):
        collapse_ids = [
            "collapseRenseignements",
            "collapseGeo",
            "collapseSituation",
            "collapseNaturel",
            "collapseEquipements",
            "collapseElementsPaysager",
        ]
        for cid in collapse_ids:
            self.assertIsNotNone(
                self.soup.find("div", {"id": cid}),
                f"Collapsible card '{cid}' not found in HTML"
            )

    def test_empty_state_equipements(self):
        equip_div = self.soup.find("div", {"id": "collapseEquipements"})
        self.assertIsNotNone(equip_div)
        table = equip_div.find("table")
        self.assertIn("Aucun équipement associé", table.text)

    def test_empty_state_elements_paysager(self):
        elem_div = self.soup.find("div", {"id": "collapseElementsPaysager"})
        self.assertIsNotNone(elem_div)
        table = elem_div.find("table")
        self.assertIn("Aucun élément paysager associé", table.text)

    def test_boolean_formatting(self):
        elem_div = self.soup.find("div", {"id": "collapseElementsPaysager"})
        self.assertIsNotNone(elem_div)
        table = elem_div.find("table")
        headers = [th.text.strip() for th in table.find_all("th")]
        self.assertIn("Est remarquable", headers)
        self.assertTrue("Oui" in table.text or "Non" in table.text)

    def test_default_dash_formatting(self):
        elem_div = self.soup.find("div", {"id": "collapseElementsPaysager"})
        self.assertIsNotNone(elem_div)
        table = elem_div.find("table")
        self.assertIn("-", table.text)

User = get_user_model()

class BatiListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        # Create needed NomenclatureTypes and Nomenclatures
        ntype = NomenclatureType.objects.create(label="NOTE_PAT", code="NOTE_PAT")
        note_nomenclature = Nomenclature.objects.create(id_type=ntype, label="5")
        typebat_type = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        typebat_nom = Nomenclature.objects.create(id_type=typebat_type, label="TYPE_BAT_label")
        class_type = NomenclatureType.objects.create(label="CL_ARCHI", code="CL_ARCHI")
        class_nom = Nomenclature.objects.create(id_type=class_type, label="CL_ARCHI_label")

        # filled bati
        self.bati1 = Bati.objects.create(
            appelation="TestBati",  # str
            type_bat=typebat_nom,   # FK
            classe=class_nom,       # FK
            notepatri=note_nomenclature,  # int
            indivision=True,        # bool
            date_insert=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),  # date
            geom=Point(1.23, 4.56), # point
        )        

        # empty bati
        self.bati2 = Bati.objects.create(
            appelation="",  # empty string
            type_bat=typebat_nom,
            classe=class_nom,
            notepatri=None,  # empty int/float (FK)
            indivision=None,  # empty bool
            date_insert=None,  # empty date
            geom=Point(0, 0),
        )

    def test_bati_detail_attributes_fields(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{self.bati1.pk}/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)

        # String field
        nom_td = soup.find("th", {"data-qa": "nom"}).find_next("td")
        self.assertIn("TestBati", nom_td.text)

        # Integer/float field
        valeur_patri = soup.find("th", {"data-qa": "valeurPat"}).find_next("td")
        self.assertIn("5", valeur_patri.text)

        # Boolean field
        indiv_td = soup.find("th", {"data-qa": "indiv"}).find_next("td")
        self.assertIn("Oui", indiv_td.text)

        # Date field
        date_td = soup.find("th", {"data-qa": "date"}).find_next("td")
        self.assertIn("2024", date_td.text)


    def test_bati_detail_attributes_empty_states(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{self.bati2.pk}/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)

        # empty str
        nom_td = soup.find("th", {"data-qa": "nom"}).find_next("td")
        self.assertIn(str(self.bati2), nom_td.text)

        # empty int
        valeur_patri = soup.find("th", {"data-qa": "valeurPat"}).find_next("td")
        self.assertEqual(valeur_patri.text.strip(), "-")

        # empty bool
        indivision = soup.find("th", {"data-qa": "indiv"}).find_next("td")
        self.assertEqual(indivision.text, "Non") # default for empty bool is Non

        # empty date
        date_td = soup.find("th", {"data-qa": "date"}).find_next("td")
        self.assertEqual(date_td.text.strip(), "-")