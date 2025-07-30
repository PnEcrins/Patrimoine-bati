from django.test import TestCase
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

from .factories import (
    BatiFactory,
)

User = get_user_model()

class BatiDetailHTMLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.bati = BatiFactory()

    def get_soup(self, pk):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{pk}/')
        self.assertEqual(response.status_code, 200)
        return BeautifulSoup(response.content, "html.parser")

    def test_tab_panes_exist(self):
        soup = self.get_soup(self.bati.pk)
        for pane_id in ["enq-pers", "travaux", "structure"]:
            self.assertIsNotNone(
                soup.find("div", {"id": pane_id}),
                f"Tab pane '{pane_id}' not found in HTML"
            )

    def test_nav_links(self):
        soup = self.get_soup(self.bati.pk)
        nav_links = soup.select("a.nav-link")
        self.assertTrue(any("Travaux" in link.text for link in nav_links))
        self.assertTrue(any("Gros et Second Oeuvre" in link.text for link in nav_links))
        self.assertTrue(any("Perspectives et Enquetes" in link.text for link in nav_links))
        self.assertTrue(any("Zonage" in link.text for link in nav_links))

    def test_perspectives_table_headers(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        table = pane.find("table", {"data-qa": "perspectives-table"})
        self.assertIsNotNone(table)
        headers = [th.text.strip() for th in table.find_all("th")]
        expected = ["Date", "Perspective", "Actions"]
        for h in expected:
            self.assertIn(h, headers)

    def test_enquetes_table_headers(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", {"data-qa": "enquetes-table"})
        self.assertTrue(len(tables) >= 1)
        enq_table = tables[0]
        headers = [th.text.strip() for th in enq_table.find_all("th")]
        expected = ["Personne", "Date enquête", "Date rédaction", "Actions"]
        for h in expected:
            self.assertIn(h, headers)

    def test_travaux_header_row(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        header_row = pane.find("div", class_="row font-weight-bold border-bottom pb-2 mb-2")
        self.assertIsNotNone(header_row)
        expected = [
            "Permis", "Date demande", "Autorisation", "Date permis", "Numéro", "Actions"
        ]
        for h in expected:
            self.assertIn(h, header_row.text)

    def test_travaux_table_headers(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        accordion = pane.find("div", {"id": "demandesAccordion"})
        table = accordion.find("table", class_="table table-sm table-bordered mb-0 text-center")
        if table:
            headers = [th.text.strip() for th in table.find_all("th")]
            expected = [
                "Date des travaux", "Autorisation du parc", "Subvention accordée",
                "Nature des Travaux", "Nouvel usage", "Actions"
            ]
            for h in expected:
                self.assertIn(h, headers)

    def test_structure_section_exists(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        self.assertIn("Liste des structures", pane.text)
        self.assertIn("Liste des éléments de second oeuvre", pane.text)

    def test_structure_table_headers(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-2")
        if tables:
            headers = [th.text.strip() for th in tables[0].find_all("th")]
            self.assertIn("Description de la structure", headers)
            self.assertIn("Structure", tables[0].text)
            self.assertIn("Structure remarquable", tables[0].text)
            self.assertIn("Conservation", tables[0].text)
            self.assertIn("Matériau principal", tables[0].text)
            self.assertIn("Mise en oeuvre", tables[0].text)
            self.assertIn("Commentaire", tables[0].text)

    def test_structure_finitions_table_headers(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-0")
        if tables:
            headers = [th.text.strip() for th in tables[0].find_all("th")]
            self.assertIn("Matériau fin", headers)
            self.assertIn("Finition", headers)
            self.assertIn("Actions", headers)

    def test_second_oeuvre_table_headers(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "secondOeuvreAccordion"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-2")
        if len(tables) > 1:
            headers = [th.text.strip() for th in tables[1].find_all("th")]
            self.assertIn("Description de l'élément", headers)
            self.assertIn("Catégorie", tables[1].text)
            self.assertIn("Remarquable", tables[1].text)
            self.assertIn("Conservation", tables[1].text)
            self.assertIn("Commentaire", tables[1].text)

    def test_second_oeuvre_finitions_table_headers(self):
        soup = self.get_soup(self.bati.pk)
        pane = soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-0")
        if len(tables) > 1:
            headers = [th.text.strip() for th in tables[1].find_all("th")]
            self.assertIn("Matériau fin", headers)
            self.assertIn("Finition", headers)
            self.assertIn("Actions", headers)

    def test_plus_icons_present(self):
        soup = self.get_soup(self.bati.pk)
        plus_icons = soup.select("i.bi-plus")
        self.assertTrue(len(plus_icons) > 0)

    def test_pencil_icons_present(self):
        soup = self.get_soup(self.bati.pk)
        pencil_icons = soup.select("i.bi-pencil")
        self.assertTrue(len(pencil_icons) > 0 or len(soup.select("i.bi-pencil-square")) > 0)

    def test_trash_icons_present(self):
        soup = self.get_soup(self.bati.pk)
        trash_icons = soup.select("i.bi-trash")
        self.assertTrue(len(trash_icons) > 0)

    def test_chevron_icons_present(self):
        soup = self.get_soup(self.bati.pk)
        chevron_icons = soup.select("i.bi-chevron-down")
        self.assertTrue(len(chevron_icons) > 0)

    def test_traverse_dom(self):
        soup = self.get_soup(self.bati.pk)
        tables = soup.find_all("table", class_="table-striped")
        found = False
        for table in tables:
            if table.find_parent("div", class_="mb-3") or table.find_parent("div", class_="card-body"):
                found = True
                break
        self.assertTrue(found)