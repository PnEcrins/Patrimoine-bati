from django.test import TestCase
from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from .factories import (
    BatiFactory,
)

User = get_user_model()

class BatiDetailAttributesHTMLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')

        # Create a filled Bati using the factory
        cls.bati_full = BatiFactory()
        
    def get_soup(self, pk):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{pk}/')
        self.assertEqual(response.status_code, 200)
        return BeautifulSoup(response.content)

    def test_renseignements_card_exists(self):
        soup = self.get_soup(self.bati_full.pk)
        card = soup.find("div", {"id": "collapseRenseignements"})
        self.assertIsNotNone(card)

    def test_geo_card_exists(self):
        soup = self.get_soup(self.bati_full.pk)
        card = soup.find("div", {"id": "collapseGeo"})
        self.assertIsNotNone(card)

    def test_situation_card_exists(self):
        soup = self.get_soup(self.bati_full.pk)
        card = soup.find("div", {"id": "collapseSituation"})
        self.assertIsNotNone(card)

    def test_naturel_card_exists(self):
        soup = self.get_soup(self.bati_full.pk)
        card = soup.find("div", {"id": "collapseNaturel"})
        self.assertIsNotNone(card)

    def test_equipements_card_exists(self):
        soup = self.get_soup(self.bati_full.pk)
        card = soup.find("div", {"id": "collapseEquipements"})
        self.assertIsNotNone(card)

    def test_elements_paysager_card_exists(self):
        soup = self.get_soup(self.bati_full.pk)
        card = soup.find("div", {"id": "collapseElementsPaysager"})
        self.assertIsNotNone(card)

    def test_all_table_headers_present(self):
        soup = self.get_soup(self.bati_full.pk)
        headers = [th.text.strip() for th in soup.find_all("th")]
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
        soup = self.get_soup(self.bati_full.pk)
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
                soup.find("div", {"id": cid}),
                f"Collapsible card '{cid}' not found in HTML"
            )

    def test_boolean_formatting(self):
        soup = self.get_soup(self.bati_full.pk)
        equip_div = soup.find("div", {"id": "collapseEquipements"})
        self.assertIsNotNone(equip_div)
        table = equip_div.find("table")
        headers = [th.text.strip() for th in table.find_all("th")]
        self.assertIn("Est remarquable", headers)
        self.assertTrue("Oui" in table.text or "Non" in table.text)

    def test_bati_detail_attributes_fields(self):
        soup = self.get_soup(self.bati_full.pk)
        # String field
        nom_td = soup.find("th", {"data-qa": "nom"}).find_next("td")
        self.assertIn("Bâtiment", nom_td.text)
        # Integer/float field
        valeur_patri = soup.find("th", {"data-qa": "valeurPat"}).find_next("td")
        self.assertTrue(valeur_patri.text.strip() != "-")
        # Boolean field
        indiv_td = soup.find("th", {"data-qa": "indiv"}).find_next("td")
        self.assertIn(indiv_td.text.strip(), ["Oui", "Non"])
        # Date field
        date_td = soup.find("th", {"data-qa": "date"}).find_next("td")
        self.assertTrue(date_td.text.strip() != "-")