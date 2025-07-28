from django.test import TestCase
from bs4 import BeautifulSoup


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
